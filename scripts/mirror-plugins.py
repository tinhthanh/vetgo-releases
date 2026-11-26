#!/usr/bin/env python3
"""Mirror plugins released in their own repositories onto this one.

    scripts/mirror-plugins.py [--config mirrors.json] [--repo OWNER/NAME] [--dry-run]

Some plugins are released where their source is (chrome in
tinhthanh/open-browser-use, computer in tinhthanh/open-codex-computer-use,
tagged <tag_prefix><version>) by a workflow or a script with no token for
this repository. mirrors.json names them; for each, the newest published
release there is copied here as <id>-v<version> (its <id>-<version>*.tar.gz
and their .sha256), unless that release is here already, so
scripts/plugin-registry.py lists it. Releases here are never replaced: a
version is published once.
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile


def gh(*args):
    return subprocess.run(["gh", *args], check=True, text=True, capture_output=True).stdout


def exists(repo, tag):
    try:
        gh("release", "view", tag, "-R", repo, "--json", "tagName")
        return True
    except subprocess.CalledProcessError:
        return False


def newest(repo, prefix):
    pages = json.loads(gh("api", "--paginate", "--slurp", f"repos/{repo}/releases?per_page=100"))
    found = [r for page in pages for r in page
             if not r.get("draft") and not r.get("prerelease") and r["tag_name"].startswith(prefix)]
    return max(found, key=lambda r: r["published_at"]) if found else None


def mirror(m, target, dry_run):
    plugin_id, repo, prefix = m["id"], m["repo"], m["tag_prefix"]
    r = newest(repo, prefix)
    if not r:
        print(f"mirror: {repo} has no {prefix}* release", file=sys.stderr)
        return
    version = r["tag_name"][len(prefix):]
    tag = f"{plugin_id}-v{version}"
    if exists(target, tag):
        print(f"mirror: {tag} is here already", file=sys.stderr)
        return
    name = re.compile(re.escape(f"{plugin_id}-{version}") + r"(-[a-z0-9]+-[a-z0-9]+)?\.tar\.gz(\.sha256)?$")
    assets = [a["name"] for a in r["assets"] if name.fullmatch(a["name"])]
    if not any(a.endswith(".tar.gz") for a in assets):
        print(f"mirror: {repo} {r['tag_name']} has no {plugin_id}-{version}*.tar.gz; skipped", file=sys.stderr)
        return
    print(f"mirror: {repo} {r['tag_name']} → {tag}: {', '.join(sorted(assets))}", file=sys.stderr)
    if dry_run:
        return
    with tempfile.TemporaryDirectory() as d:
        args = ["release", "download", r["tag_name"], "-R", repo, "-D", d]
        for a in assets:
            args += ["-p", a]
        gh(*args)
        notes = (f"Shipyard plugin \"{plugin_id}\" {version}, mirrored from {r['html_url']}. "
                 "Vetgo lists it in Settings → Plugins; or Install from URL with the .tar.gz for your computer "
                 "(the .sha256 beside it is picked up).")
        gh("release", "create", tag, "-R", target, "--title", f"{plugin_id} {version}", "--notes", notes,
           "--latest=false", *[f"{d}/{a}" for a in sorted(assets)])


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", default="mirrors.json")
    p.add_argument("--repo", default="tinhthanh/vetgo-releases")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    with open(args.config) as f:
        mirrors = json.load(f)["mirrors"]
    failed = False
    for m in mirrors:
        try:
            mirror(m, args.repo, args.dry_run)
        except subprocess.CalledProcessError as e:
            # One source that fails does not stop the others.
            print(f"mirror: {m['id']}: {e.stderr or e}", file=sys.stderr)
            failed = True
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
