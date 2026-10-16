#!/usr/bin/env python3
"""Check local package links and the explicitly approved public PNG inventory."""
import hashlib
import json
import re
import struct
import sys
import zlib
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
APPROVED = {
    "01-kindergarten.png", "02-station-night.png", "03-street-day.png",
    "04-street-night.png", "05-park.png", "06-family.png", "07-eyewear-shop.png",
}
TEXT_SUFFIXES = {".md", ".yaml", ".json", ".py"}
ROOT_DOTFILES = {".gitignore", ".gitattributes"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def inspect_png(data):
    require(data.startswith(b"\x89PNG\r\n\x1a\n"), "Invalid PNG signature")
    offset, kinds, dimensions = 8, [], None
    while offset < len(data):
        require(offset + 12 <= len(data), "Truncated PNG chunk")
        size = struct.unpack(">I", data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        end = offset + 12 + size
        require(end <= len(data), "Truncated PNG payload")
        payload = data[offset + 8:end - 4]
        crc = struct.unpack(">I", data[end - 4:end])[0]
        require(zlib.crc32(kind + payload) & 0xFFFFFFFF == crc, "PNG CRC mismatch")
        require(kind in {b"IHDR", b"IDAT", b"IEND"}, "Unexpected PNG metadata chunk")
        if kind == b"IHDR":
            require(size == 13 and not kinds, "Invalid PNG image header")
            dimensions = struct.unpack(">II", payload[:8])
        kinds.append(kind)
        offset = end
        if kind == b"IEND":
            require(size == 0 and offset == len(data), "PNG trailing data")
            break
    require(kinds and kinds[0] == b"IHDR" and kinds[-1] == b"IEND"
            and b"IDAT" in kinds and dimensions, "Incomplete PNG")
    return dimensions


def main():
    files = [p for p in ROOT.rglob("*") if p.is_file()
             and ".git" not in p.relative_to(ROOT).parts
             and "__pycache__" not in p.relative_to(ROOT).parts]
    require(not any(p.is_symlink() for p in ROOT.rglob("*")
                    if ".git" not in p.relative_to(ROOT).parts), "Symlinks are not package assets")
    actual_pngs = {p.relative_to(ROOT).as_posix() for p in files if p.suffix.lower() == ".png"}
    expected_pngs = {f"assets/positive/{name}" for name in APPROVED}
    require(actual_pngs == expected_pngs, "Public image inventory differs from the seven-file allowlist")
    for p in files:
        relative = p.relative_to(ROOT).as_posix()
        require(relative in expected_pngs or p.suffix in TEXT_SUFFIXES or relative in ROOT_DOTFILES,
                f"Unreviewed package file: {relative}")
    manifest = json.loads((ROOT / "assets/positive/manifest.json").read_text())
    entries = manifest["examples"]
    require(len(entries) == 7 and {e["file"] for e in entries} == APPROVED, "Invalid asset manifest")
    for entry in entries:
        require(entry["classification"] == "authorized_positive_finished_illustration", "Unapproved image class")
        data = (ROOT / "assets/positive" / entry["file"]).read_bytes()
        require(len(data) == entry["bytes"], f"Size mismatch: {entry['file']}")
        require(hashlib.sha256(data).hexdigest() == entry["sha256"], f"Hash mismatch: {entry['file']}")
        require(inspect_png(data) == (entry["width"], entry["height"]), f"Dimensions mismatch: {entry['file']}")
    for p in files:
        if p.suffix != ".md":
            continue
        for link in re.findall(r"!?\[[^\]]*\]\(([^\s)]+)\)", p.read_text()):
            if re.match(r"[a-z][a-z0-9+.-]*:", link, re.I) or link.startswith("#"):
                continue
            target = (p.parent / unquote(link.split("#", 1)[0])).resolve()
            require(target.is_relative_to(ROOT) and target.exists(),
                    f"Broken or external local link in {p.relative_to(ROOT)}: {link}")
    print(f"PASS: {len(files)} package files; 7 approved PNGs, hashes, dimensions, metadata and local links")
    print("Scope: package integrity only; this does not prove image quality or future public authorization.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, json.JSONDecodeError, struct.error) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
