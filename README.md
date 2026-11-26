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
`berth-plugin.json` giving that version), or one archive per platform,
`<id>-<version>-<os>-<arch>.tar.gz` (a Mac's may be `darwin-universal`), each
ideally with a `.sha256` beside it. A computer is offered only its own build.

| Plugin | Source | How it gets here |
| --- | --- | --- |
| vglink | tinhthanh/vglink (private) | its release workflow publishes `vglink-v*` here |
| mobile | tinhthanh/mobile-mcp | its `berth-mobile` workflow publishes `mobile-v*` here |
| chrome | tinhthanh/open-browser-use | released there as `shipyard-plugin-v*`; mirrored here hourly (`mirrors.json`) |
| computer | tinhthanh/open-codex-computer-use | released there from a Mac (`scripts/release-shipyard-plugin.sh`, signed); mirrored here hourly |

`.github/workflows/plugin-registry.yml` mirrors and writes the listing again
every hour, whenever a release here is published, and by hand (Actions →
Plugin listing → Run workflow).
