#!/usr/bin/env python3
"""Install the allowlisted CpUnk configuration, with per-file backups."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
from datetime import datetime
from urllib.request import urlopen

REPO = Path(__file__).resolve().parent
MANIFEST = json.loads((REPO / 'upstream.json').read_text())
PACKAGES = [
    'git', 'hyprland', 'waybar', 'wofi', 'kitty', 'hyprpaper', 'hyprlock',
    'mako-notifier', 'swayidle', 'xdg-desktop-portal-hyprland',
    'xdg-desktop-portal-gtk', 'fonts-jetbrains-mono', 'grim', 'slurp',
    'wl-clipboard', 'policykit-1-gnome', 'libgtk4-layer-shell0',
    'libpoppler-glib8t64', 'tmux', 'ptyxis', 'nautilus',
    'gnome-control-center', 'yaru-theme-gtk', 'yaru-theme-icon', 'libnotify-bin',
]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target-home', type=Path, default=Path.home(),
                        help='Alternate home for staging/testing; default: your home')
    parser.add_argument('--upstream', type=Path,
                        help='Use an existing checkout at the pinned upstream commit')
    parser.add_argument('--skip-runtime', action='store_true',
                        help='Skip Walker/Elephant downloads, useful for staging')
    parser.add_argument('--install-deps', action='store_true',
                        help='Install Ubuntu packages using sudo apt-get')
    parser.add_argument('--install-session', action='store_true',
                        help='Register CpUnk with the login manager using sudo')
    args = parser.parse_args()
    home = args.target_home.expanduser().resolve()
    if (args.install_deps or args.install_session) and home != Path.home().resolve():
        parser.error('System installation options cannot be used with an alternate home')
    home.mkdir(parents=True, exist_ok=True)
    if args.install_deps:
        subprocess.run(['sudo', 'apt-get', 'install', '-y', *PACKAGES], check=True)
    source = args.upstream.expanduser().resolve() if args.upstream else home / '.local/share/cpunk/source'
    if source.exists():
        rev = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
        if rev != MANIFEST['theme']['commit']:
            raise SystemExit('Upstream checkout differs from the pinned commit. Use a fresh checkout or --upstream.')
    else:
        source.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['git', 'init', str(source)], check=True)
        subprocess.run(['git', '-C', str(source), 'remote', 'add', 'origin', MANIFEST['theme']['url']], check=True)
        subprocess.run(['git', '-C', str(source), 'fetch', '--depth', '1', 'origin', MANIFEST['theme']['commit']], check=True)
        subprocess.run(['git', '-C', str(source), 'checkout', '--detach', 'FETCH_HEAD'], check=True)
    # Resolve all source assets and validate downloads before replacing configuration.
    writes = {}
    for p in (REPO / 'config').rglob('*'):
        if p.is_file():
            relative = p.relative_to(REPO / 'config').as_posix()
            destination = '.local/share/' + relative if relative.startswith('applications/') else '.config/' + relative
            writes[destination] = (
                p.read_text().replace('@HOME@', str(home)).encode(), 0o644)
    for p in (REPO / 'bin').iterdir():
        if p.is_file():
            writes['.local/bin/' + p.name] = (p.read_bytes(), 0o755)
    for original, override, dest in [
        ('walker.css', 'walker.css', '.config/walker/themes/cpunk/style.css'),
        ('kitty.conf', 'kitty.conf', '.config/cpunk/kitty.conf'),
        ('wofi.css', 'wofi.css', '.config/cpunk/wofi.css'),
    ]:
        text = (source / original).read_text()
        if original == 'walker.css':
            text = text.replace('-gtk-icon-size: 0;', '-gtk-icon-size: 16px;')
        text += '\n' + (REPO / 'adapters' / override).read_text()
        writes[dest] = (text.encode(), 0o644)
    text = (source / 'mako.ini').read_text().replace('font=Liberation Sans 11', 'font=JetBrains Mono 10')
    writes['.config/cpunk/mako.conf'] = (text.encode(), 0o644)
    # A supplied upstream may be elsewhere: reference its actual wallpaper directory.
    for name in ['.config/cpunk/hyprpaper.conf', '.config/cpunk/hyprlock.conf']:
        data, mode = writes[name]
        data = data.replace(str(home / '.local/share/cpunk/source').encode(), str(source).encode())
        writes[name] = (data, mode)
    if source != home / '.local/share/cpunk/source':
        data, mode = writes['.local/bin/cpunk-menu']
        data = data.decode().replace(
            "Path.home()/'.local/share/cpunk/source/backgrounds'/w",
            "Path(" + repr(str(source)) + ")/'backgrounds'/w")
        writes['.local/bin/cpunk-menu'] = (data.encode(), mode)
    writes['.local/share/cpunk/handbook.html'] = ((REPO / 'docs/handbook.html').read_bytes(), 0o644)
    writes['.local/share/cpunk/HANDBOOK.md'] = ((REPO / 'docs/HANDBOOK.md').read_bytes(), 0o644)
    writes['.local/share/cpunk/cpunk.desktop'] = (
        (REPO / 'session/cpunk.desktop.in').read_text().replace('@HOME@', str(home)).encode(), 0o644)
    if not args.skip_runtime:
        if os.uname().machine != 'x86_64':
            raise SystemExit('Pinned runtime binaries target x86_64. Build Walker/Elephant for your architecture.')
        for asset in MANIFEST['runtime']:
            with urlopen(asset['url'], timeout=120) as response:
                data = response.read()
            if hashlib.sha256(data).hexdigest() != asset['sha256']:
                raise SystemExit('Release archive checksum mismatch: ' + asset['url'])
            with tempfile.TemporaryFile() as archive:
                archive.write(data)
                archive.seek(0)
                with tarfile.open(fileobj=archive, mode='r:gz') as tar:
                    member = tar.getmember(asset['member'])
                    if not member.isfile():
                        raise SystemExit('Expected release member is not a file')
                    payload = tar.extractfile(member).read()
            writes[asset['target']] = (payload, 0o755)
    backup = home / '.local/share/cpunk/backups' / datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    backup.mkdir(parents=True)
    records = []
    def save_existing(relative):
        target = home / relative
        record = {'path': relative, 'existed': target.exists() or target.is_symlink()}
        if record['existed']:
            if target.is_dir() and not target.is_symlink():
                raise SystemExit('Refusing to replace directory: ' + str(target))
            saved = backup / relative
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, saved, follow_symlinks=False)
        records.append(record)
        (backup / 'manifest.json').write_text(json.dumps(records, indent=2) + '\n')
        return target
    for relative, (data, mode) in writes.items():
        target = save_existing(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        # Replace a symlink itself, never write through it to another location.
        temporary = target.with_name(target.name + '.cpunk-new')
        temporary.write_bytes(data)
        temporary.chmod(mode)
        temporary.replace(target)
    for name in ['waybar.service', 'hyprpaper.service']:
        target = save_existing('.config/systemd/user/' + name)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() or target.is_symlink():
            target.unlink()
        target.symlink_to('/dev/null')
    if args.install_session:
        subprocess.run(['sudo', 'install', '-m', '0644',
                        str(home / '.local/share/cpunk/cpunk.desktop'),
                        '/usr/share/wayland-sessions/cpunk.desktop'], check=True)
    print('Configuration installed. Backup:', backup)
    if not args.install_session:
        print('To add the login entry, run:')
        print('sudo install -m 0644 "$HOME/.local/share/cpunk/cpunk.desktop" /usr/share/wayland-sessions/cpunk.desktop')
    print('Save your work, log out, then select CpUnk (Hyprland) at login.')

if __name__ == '__main__':
    main()
