# Vetgo releases

Downloads for Vetgo's phone tools. The source is private; this repository only
holds the published builds (see **Releases**).

| What | File | For |
| --- | --- | --- |
| **Vetgo Phone Desktop** | `Vetgo.Phone.Desktop_<ver>_x64-setup.exe` | Windows 10/11: texts, calls and chat messages of an Android phone on the computer, no other software needed |
| **vglink plugin** | `vglink-<ver>.tar.gz` | Shipyard / Vetgo: Settings → Plugins → *Install from URL…* with the file's link |
| **berth-vglink** | `berth-vglink-<ver>-<platform>` | The plugin's helper; Shipyard downloads the right one by itself |
| **Vetgo Phone** | `vetgo-phone-<ver>.apk` | The Android app; the computer installs it over the USB cable by itself |

Each release is tagged `vglink-v<version>` and lists the SHA-256 of every file.

## Plugin listing

The Vetgo app's **Settings → Plugins** reads `index.json` from the `registry`
release. A plugin is listed by its newest published release tagged
`<id>-v<version>` that has `<id>-<version>.tar.gz` (its `<id>/` folder, with
`berth-plugin.json` giving that version) and, ideally, a `.sha256` beside it.
`.github/workflows/plugin-registry.yml` writes the listing again whenever such a
release is published (or by hand: Actions → Plugin listing → Run workflow).

## Vetgo Phone Desktop, in short

1. Run the installer (Windows SmartScreen may warn: *More info* → *Run anyway*; the
   installer isn't signed yet).
2. On the phone: turn on **Developer options → USB debugging**, plug it into the
   computer, tap **Allow**.
3. The app fetches adb, installs Vetgo Phone on the phone, grants it what it needs
   and connects. Texts, calls, app chats and the journal are then in the app; it keeps
   running in the tray and starts with Windows.
