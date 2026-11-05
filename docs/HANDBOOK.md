# CpUnk Handbook

Ubuntu / Hyprland. Super means the Windows-logo key.

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

This handbook is also available from Super + K or the CpUnk menu.

Click **Apps** at the top-left of the panel, or press **Super + Space**. Switch tabs with **Ctrl + Left/Right** or **Ctrl + Tab/Shift + Ctrl + Tab**. Use the arrow keys to select an item and **Enter** to open it. Click **Windows** to find a running app and jump to its workspace. **System** contains settings and session controls. **Wallpapers** shows previews of the built-in and personal images. Use **Esc** to close the menu. Log out, restart, and shutdown require confirmation.

Clipboard history starts with the CpUnk session and keeps the 15 most recent copied text or image items locally. Open it with **Super + Shift + V**, the panel's **Clipboard** button, or **Apps → System → Clipboard history**. Selecting an item copies it again; use **Ctrl + V** to paste (**Ctrl + Shift + V** in the terminal). Highlight an item and press **Shift + Delete** to remove just that item, or choose **Clear clipboard history** to erase everything.

## Walkthrough

A first session, step by step.

1. **Log in.** At the login screen, open the gear/session selector, choose **CpUnk (Hyprland)**, and sign in. The black panel appears at the top: **Apps** on the left, workspaces in the middle, system stats and **Clipboard** / **LOCK** buttons on the right.
2. **Open a terminal.** Press **Super + Enter** (or **Ctrl + Alt + T**). Kitty opens inside the `main` tmux session. Every terminal joins that same session, so a second terminal mirrors the first; press **Ctrl + B**, then **C** for a new tmux window, or **Ctrl + B**, then **D** to detach.
3. **Launch an app.** Press **Super + Space**, type a few letters, and press **Enter**. **Ctrl + Left/Right** switches between the **Apps**, **Windows**, **System**, and **Wallpapers** tabs. **Esc** closes the menu.
4. **Arrange windows.** Open a second app; it tiles next to the first automatically. **Super + arrow** moves focus, **Super + Shift + arrow** moves the window, and **Super + Ctrl + arrow** resizes it. **Super + V** floats a window, **Super + F** makes it fullscreen, and **Super + Q** closes it.
5. **Use workspaces.** **Super + 2** jumps to workspace 2; apps on workspace 1 keep running. **Super + Shift + 2** sends the focused window there and follows it. You can also click the numbers in the panel.
6. **Copy, paste, and reuse.** Copy text as usual, then press **Super + Shift + V** to see the last 15 items. **Enter** copies an item again, **Ctrl + V** pastes it, and **Shift + Delete** removes the highlighted item.
7. **Take a screenshot.** Press **Print Screen** and drag over an area. The image is copied to the clipboard and saved under `~/Pictures/Screenshots`.
8. **Change the wallpaper.** Open **Super + Space**, go to the **Wallpapers** tab, and press **Enter** on a preview. Drop your own images into `~/.local/share/cpunk/wallpapers/` and they appear in the list.
9. **Lock or leave.** **Super + L** locks the screen. **Super + Shift + E** opens the menu; its **System** tab has log out, restart, and shutdown, each with a confirmation.

Press **Super + K** at any time to reopen this handbook.

## Customize

The Rofi menu uses a lightly glassy graphite Spotlight panel with a large search field, one vertical results list, clear application icons, signal-red selection, and persistent Apps, Windows, System, and Wallpapers tabs. Settings uses the same near-black GTK palette with red navigation and control accents. The System tab includes Settings, Network, Sound, Files, Terminal, Help, and session controls. Network and sound panel buttons use the same settings wrapper. GTK styling is saved in `~/.config/gtk-3.0/gtk.css` and `~/.config/gtk-4.0/gtk.css`.


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
