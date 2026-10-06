#!/usr/bin/env python3
"""Rewrite the block between the shipped markers in README.md with the latest version of each project."""
import json
import os
import re
import urllib.request
from pathlib import Path

OWNER = "andresgarcia29"
REPOS = ["ark-cli", "harness-creator", "harness-daemon", "harness-ui"]
README = Path(__file__).resolve().parent.parent / "README.md"
START, END = "<!-- shipped:start -->", "<!-- shipped:end -->"


def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}", headers={"Accept": "application/vnd.github+json"})
    if token := os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def latest(repo):
    if rel := api(f"/repos/{OWNER}/{repo}/releases/latest"):
        return rel["tag_name"], rel["published_at"][:10], rel["html_url"]
    if tags := api(f"/repos/{OWNER}/{repo}/tags?per_page=1"):
        tag = tags[0]
        commit = api(f"/repos/{OWNER}/{repo}/commits/{tag['commit']['sha']}")
        return tag["name"], commit["commit"]["committer"]["date"][:10], f"https://github.com/{OWNER}/{repo}/tree/{tag['name']}"
    return None


def main():
    shipped = [(repo, *v) for repo in REPOS if (v := latest(repo))]
    shipped.sort(key=lambda s: s[2], reverse=True)
    lines = [f"- **[{repo}](https://github.com/{OWNER}/{repo})** [`{tag}`]({url}) · {day}" for repo, tag, day, url in shipped]
    readme = README.read_text(encoding="utf-8")
    block = f"{START}\n" + "\n".join(lines) + f"\n{END}"
    README.write_text(re.sub(f"{re.escape(START)}.*?{re.escape(END)}", lambda _: block, readme, flags=re.S), encoding="utf-8")


if __name__ == "__main__":
    main()
