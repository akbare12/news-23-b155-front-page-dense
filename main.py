#!/usr/bin/env python3
"""NEWS-23 B155 front-page-dense entry runner (stdlib only, no PIL).

Reads the entry.png shipped next to this file, validates its PNG structure
strictly (signature, IHDR, chunk CRCs, IEND, size, dimensions), and writes
an exact copy to os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"),
"entry.png"). Never writes next to main.py.

Layout of a PNG chunk: 4-byte big-endian length, 4-byte type, `length`
bytes of data, 4-byte CRC. The CRC covers type + data, not the length.
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "312d4476afa397ed7c8a90817e420393f58c16ab38a26270d84554978ff7c6e3"
EXPECTED_SIZE = 180604
EXPECTED_W, EXPECTED_H = 1024, 1024
MIN_SIZE = 10000
MAX_SIZE = 1024 * 1024
PNG_SIG = b"\x89PNG\r\n\x1a\n"


def fail(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def validate_png(data):
    if len(data) < MIN_SIZE:
        fail(f"file too small: {len(data)} bytes")
    if len(data) > MAX_SIZE:
        fail(f"file too large: {len(data)} bytes")
    if len(data) != EXPECTED_SIZE:
        fail(f"unexpected size: {len(data)} != {EXPECTED_SIZE}")
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        fail("sha256 mismatch")
    if data[:8] != PNG_SIG:
        fail("bad PNG signature")
    # First chunk must be IHDR, 13 bytes, 1024x1024, bit depth 8,
    # colour type 2 (RGB) or 6 (RGBA), compression/filter/interlace 0.
    off = 8
    if len(data) < off + 8:
        fail("truncated before first chunk")
    (clen,) = struct.unpack(">I", data[off:off + 4])
    ctype = data[off + 4:off + 8]
    if ctype != b"IHDR" or clen != 13:
        fail("first chunk is not a 13-byte IHDR")
    ihdr = data[off + 8:off + 21]
    w, h, depth, ctype_b, comp, filt, inter = struct.unpack(">IIBBBBB", ihdr)
    if (w, h) != (EXPECTED_W, EXPECTED_H):
        fail(f"unexpected dimensions: {w}x{h}")
    if depth != 8 or ctype_b not in (2, 6):
        fail(f"unexpected IHDR: bit depth {depth}, colour type {ctype_b}")
    if comp != 0 or filt != 0 or inter != 0:
        fail("IHDR compression/filter/interlace must be 0")
    (crc_stored,) = struct.unpack(">I", data[off + 21:off + 25])
    crc_calc = zlib.crc32(ctype + ihdr) & 0xFFFFFFFF
    if crc_calc != crc_stored:
        fail("IHDR CRC mismatch")
    # Chunk walk: verify every chunk CRC, IDAT payloads, IEND last.
    # The walk starts at offset 8 (right after the 8-byte signature) and
    # re-checks the IHDR CRC as part of the loop; the explicit IHDR check
    # above runs first so a bad header fails fast with a clear message.
    off = 8
    seen_iend = False
    idat_total = 0
    while off < len(data):
        if len(data) - off < 12:
            fail("truncated chunk header")
        (clen,) = struct.unpack(">I", data[off:off + 4])
        ctype = data[off + 4:off + 8]
        if off + 12 + clen > len(data):
            fail(f"truncated chunk {ctype!r}")
        chunk_data = data[off + 8:off + 8 + clen]
        (crc_stored,) = struct.unpack(">I", data[off + 8 + clen:off + 12 + clen])
        crc_calc = zlib.crc32(ctype + chunk_data) & 0xFFFFFFFF
        if crc_calc != crc_stored:
            fail(f"CRC mismatch in chunk {ctype!r}")
        if ctype == b"IDAT":
            if clen == 0:
                fail("empty IDAT chunk")
            idat_total += clen
        if ctype == b"IEND":
            if clen != 0:
                fail("IEND must be 0 bytes")
            if off + 12 + clen != len(data):
                fail("trailing data after IEND")
            seen_iend = True
            break
        off += 12 + clen
    if not seen_iend:
        fail("missing IEND chunk")
    if idat_total < 1000:
        fail(f"IDAT payload too small: {idat_total} bytes")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        fail(f"source not found: {src}")
    with open(src, "rb") as f:
        data = f.read()
    validate_png(data)

    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not outdir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    outdir_abs = os.path.abspath(outdir)
    here_abs = os.path.abspath(here)
    if outdir_abs == here_abs or outdir_abs.startswith(here_abs + os.sep):
        fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    if os.path.exists(outdir_abs) and not os.path.isdir(outdir_abs):
        fail("MAKEFUN_OUTPUT_DIR is a file, not a directory")
    dst = os.path.join(outdir_abs, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(src):
        fail("output would overwrite the source")
    os.makedirs(outdir_abs, exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        written = f.read()
    if written != data:
        fail("output is not byte-identical to the source")
    print(f"wrote {dst} ({len(data)} bytes)")
    print(f"sha256 {hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
