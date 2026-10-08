# CpUnk on Ubuntu

A CpUnk-inspired Hyprland session for Ubuntu 26.04, with a Rofi launcher with an application icon grid, black Waybar panel, square tiled windows, a matching Kitty terminal, and the original CpUnk wallpaper. GNOME remains available as a separate login option.

Rofi 2.0 or newer with Wayland support is required; `--install-deps` installs Ubuntu’s package.

This repository contains the configuration and integration scripts from my desktop. It is an Ubuntu adaptation, rather than a full Omarchy installation.

## Install

Tested on Ubuntu 26.04, Hyprland 0.53.3, and an x86_64 NVIDIA desktop. Review the scripts before running them.

```bash
git clone https://github.com/yosefther/cpunk-ubuntu-dotfiles.git
cd cpunk-ubuntu-dotfiles
python3 install.py --install-deps --install-session
```

The installer:

- Installs Ubuntu dependencies through `sudo apt-get` when `--install-deps` is supplied.
- Fetches the original CpUnk theme at the commit pinned in `upstream.json`.
- Downloads pinned official Walker and Elephant release archives and checks their SHA-256 hashes.
- Backs up each existing managed file under `~/.local/share/cpunk/backups/` before replacing it.
- Writes paths for your username, instead of assuming `/home/user`.
- Adds **CpUnk (Hyprland)** to the login screen with `--install-session`.
- Masks the package Waybar/Hyprpaper services for this user; the CpUnk session starts them directly, keeping them out of GNOME.

Save your work and log out. Select your username, open the login screen's gear/session selector, choose **CpUnk (Hyprland)**, and sign in. Choose **Ubuntu** instead when you want GNOME back. The generic **Hyprland** entry does not use this repository's configuration.

Already have the packages? Run `python3 install.py --install-session`. To install only the user files and register the login entry later, run `python3 install.py`.

The installer requires Python 3, Git, internet access, and an x86_64 machine for the pinned release binaries. A separate GNOME login is recommended while checking your first full session.

## Start using it

**Super** is the Windows-logo key. New windows tile automatically. Click a window to focus it, or use Super + an arrow. A workspace is a separate group of windows; switching workspaces does not close applications.

| Shortcut | Action |
|---|---|
| Super + Space | Apps menu: icon grid, search, Windows, System, and Wallpapers tabs |
| Super + Alt + Space | Open the same Apps menu |
| Ctrl + Alt + T / Super + Enter | Kitty terminal, attached to the main tmux session |
| Super + E / Super + B | Files / Brave browser |
| Super + arrow | Focus another window |
| Super + Shift + arrow | Move the focused window |
| Super + Ctrl + arrow | Resize in 40-pixel steps |
| Super + F / Super + V | Fullscreen / floating mode |
| Super + left/right mouse drag | Move / resize a window |
| Super + 1–9 | Switch workspace |
| Super + Shift + 1–9 | Move a window to that workspace and follow it |
| Super + Q | Close the focused application |
| Super + L | Lock with Hyprlock |
| Super + K | Open the handbook |
| Super + Shift + R | Reload configuration |
| Super + Shift + E | Open the menu containing logout |
| Super + Shift + V | Search clipboard history and copy an item again |
| Print Screen | Select an area; copy the screenshot and save it under `~/Pictures/Screenshots` |
| Ctrl + Alt + Shift + T | Cairo/Ptyxis fallback terminal |

Use **Esc** to dismiss menus. The idle timer locks after ten minutes. Test locking/unlocking on your first login. Rebooting ends running tmux sessions; Ctrl+B, then D detaches without ending them.

The full [handbook](docs/HANDBOOK.md) is included, along with a browser-readable version installed at `~/.local/share/cpunk/handbook.html`.

Click **Apps** at the top-left of the panel, or press **Super + Space**. Switch tabs with **Ctrl + Left/Right** or **Ctrl + Tab/Shift + Ctrl + Tab**. Use the arrow keys to select an item and **Enter** to open it. Click **Windows** to find a running app and jump to its workspace. **System** contains settings and session controls. **Wallpapers** shows previews of the built-in and personal images. Use **Esc** to close the menu. Log out, restart, and shutdown require confirmation.

Clipboard history starts with the CpUnk session and keeps up to 200 copied text or image items locally. Open it with **Super + Shift + V**, the panel's **Clipboard** button, or **Apps → System → Clipboard history**. Selecting an item copies it again; use **Ctrl + V** to paste. Choose **Clear clipboard history** in that menu to erase the saved history.

## Customize

The Rofi menu uses opaque charcoal surfaces, visible application icons, white text, and red selection highlights. Settings uses an opaque dark GTK theme; the System tab includes Settings, Network, Sound, Files, Terminal, Help, and session controls. Network and sound panel buttons use the same settings wrapper. GTK styling is saved in `~/.config/gtk-3.0/gtk.css` and `~/.config/gtk-4.0/gtk.css`.


- **Wallpaper:** Apps menu → Wallpapers. Choices are the upstream `Arcyx.png`, `Bxry2.png`, `Cryox3.png`, and `Draxo.png` images. The selection is saved in `~/.config/cpunk/hyprpaper.conf`. Add your own PNG, JPG, JPEG, or WebP images to `~/.local/share/cpunk/wallpapers/`; they appear automatically in this menu. Personal images stay local and are not included in this repository.
- **Keyboard:** edit `input.kb_layout` in `~/.config/cpunk/hyprland.conf`. The snapshot uses `us`.
- **Monitor:** the default is preferred resolution, automatic placement, scale 1. Adjust `monitor` for your displays.
- **Browser:** Super+B expects an existing `brave-browser` installation. Edit this binding to `firefox` or another browser if necessary; Brave is not installed by this script.
- **Panel:** edit `~/.config/cpunk/waybar.json` and `waybar.css`.
- **Theme overrides:** the `adapters/` files contain only the Ubuntu-specific additions; original theme styles are fetched from upstream.

GTK applications and Walker use Cairo rendering. Walker also requests full redraws. These settings worked around NVIDIA rendering problems on the original machine, with some extra CPU cost. Kitty still uses its normal GPU renderer. Blur and animations are disabled.

`install.py` also fetches original CpUnk files. It does **not** change Discord's acceleration preference; if Discord freezes, disable Hardware Acceleration in Discord settings and restart it. Existing Discord launcher overrides, shell histories, credentials, and application profiles are not part of this repository.

## Checks and recovery

```bash
Hyprland --verify-config --config "$HOME/.config/cpunk/hyprland.conf"
hyprctl configerrors
hyprctl binds
nvidia-smi
```

Session component logs are under `~/.local/state/cpunk/`. The setup was checked in a nested preview and subsequently used in a full login on the original machine; another computer still needs its own display, audio, networking, and lock checks.

To return to GNOME, log out through the CpUnk menu and select **Ubuntu** at login. To restore an overwritten file, copy it from your timestamped backup to the same relative path under your home. `manifest.json` records which managed paths existed before installation; newly created paths have no previous file to restore. Keep the backup local.

A staging check can use the existing pinned theme checkout without touching the active desktop:

```bash
python3 install.py --target-home /tmp/cpunk-staging \
  --upstream "$HOME/.local/share/cpunk/source" --skip-runtime
Hyprland --verify-config --config /tmp/cpunk-staging/.config/cpunk/hyprland.conf
```

## Credits

Original theme and artwork: [stannorbvb-cmd/cpunk](https://github.com/stannorbvb-cmd/cpunk), pinned to `c4d726bea9e6e4b3feb477c052e25bfcb2832ea4`.

Launcher and backend: [Walker](https://github.com/abenz1267/walker) 2.17.2 and [Elephant](https://github.com/abenz1267/elephant) 2.22.1. Desktop: [Hyprland](https://hypr.land/) and [Waybar](https://github.com/Alexays/Waybar).

See [THIRD_PARTY.md](THIRD_PARTY.md) for how upstream assets are handled.
