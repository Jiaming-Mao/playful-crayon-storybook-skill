"""Portable negative tests for the public package inventory checker (stdlib only)."""
import hashlib
import json
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


class PackageValidationTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="crayon-package-test-")
        self.addCleanup(self.scratch.cleanup)
        self.copy = Path(self.scratch.name) / "package"
        shutil.copytree(PACKAGE, self.copy, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def validate(self):
        return subprocess.run(
            [sys.executable, str(self.copy / "scripts/validate_package.py")],
            capture_output=True, text=True, check=False,
        )

    def test_reviewed_package_is_accepted(self):
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_changed_image_is_rejected(self):
        image = self.copy / "assets/positive/01-kindergarten.png"
        data = bytearray(image.read_bytes())
        data[100] ^= 1
        image.write_bytes(data)
        self.assertNotEqual(self.validate().returncode, 0)

    def test_extra_image_is_rejected(self):
        shutil.copyfile(self.copy / "assets/positive/01-kindergarten.png", self.copy / "unreviewed.png")
        self.assertNotEqual(self.validate().returncode, 0)

    def test_broken_document_link_is_rejected(self):
        with (self.copy / "README.md").open("a") as stream:
            stream.write("\n[Missing file](references/missing.md)\n")
        self.assertNotEqual(self.validate().returncode, 0)

    def test_embedded_metadata_is_rejected_even_with_updated_hash(self):
        image = self.copy / "assets/positive/01-kindergarten.png"
        data = image.read_bytes()
        kind, payload = b"tEXt", b"Comment\x00Synthetic test metadata"
        chunk = struct.pack(">I", len(payload)) + kind + payload
        chunk += struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)
        data = data[:-12] + chunk + data[-12:]
        image.write_bytes(data)
        manifest_path = self.copy / "assets/positive/manifest.json"
        manifest = json.loads(manifest_path.read_text())
        entry = next(e for e in manifest["examples"] if e["file"] == image.name)
        entry.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        manifest_path.write_text(json.dumps(manifest))
        self.assertNotEqual(self.validate().returncode, 0)

    def test_local_link_outside_package_is_rejected(self):
        outside = self.copy.parent / "outside.md"
        outside.write_text("Synthetic test fixture")
        with (self.copy / "README.md").open("a") as stream:
            stream.write("\n[Outside file](../outside.md)\n")
        self.assertNotEqual(self.validate().returncode, 0)


if __name__ == "__main__":
    unittest.main()
