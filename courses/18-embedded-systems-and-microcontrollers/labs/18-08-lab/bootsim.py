"""Lab 18-08: a flash and bootloader model for firmware updates, with power cuts injected at every step.

Flash is a list of sectors holding bytes; a sector being erased or written when power fails is left corrupt.
Images carry a small header (magic, version, security counter, length) and a SHA-256 digest of header and payload,
checked by the bootloader before it boots a slot. A one-record status area is written atomically (as a real
bootloader achieves with a CRC-protected record written to alternate locations).

Update schemes, each a sequence of flash operations plus a recovery rule the bootloader applies at every boot:
- "inplace": the new image is written directly over the only slot (no second slot); unsafe by design;
- "overwrite": the new image is downloaded to a secondary slot, then copied over the primary; resumable, no rollback;
- "swap": primary and secondary are exchanged sector by sector through a scratch sector, with progress recorded;
  resumable, and the old image remains available for rollback (swap back) if the new one is never confirmed.

`campaign(scheme)` cuts power before and during every operation and reports how many cuts end with the new image
booting, the old image booting, or no bootable image (bricked).
"""
from __future__ import annotations

import hashlib
import random
import struct

MAGIC = 0x96F3B83D
HDR = struct.Struct("<IIII")   # magic, version, security counter, payload length
SECTOR = 64                   # bytes per sector in the model (real parts: 512 B to 128 KiB)
CORRUPT = b"\xA5" * SECTOR


def make_image(version: int, n_sectors: int, security_counter: int = 0, seed: int = 0) -> list[bytes]:
    """An image of n_sectors sectors: header, payload, and the SHA-256 digest in the last 32 bytes."""
    rng = random.Random(seed * 1000 + version)
    body_len = n_sectors * SECTOR - HDR.size - 32
    payload = bytes(rng.randrange(256) for _ in range(body_len))
    hdr = HDR.pack(MAGIC, version, security_counter, body_len)
    digest = hashlib.sha256(hdr + payload).digest()
    blob = hdr + payload + digest
    return [blob[i:i + SECTOR] for i in range(0, len(blob), SECTOR)]


def validate(sectors: list[bytes]) -> int | None:
    """Return the image's version if the slot holds a valid image, else None."""
    blob = b"".join(sectors)
    if len(blob) < HDR.size + 32:
        return None
    magic, version, _sc, length = HDR.unpack_from(blob)
    if magic != MAGIC or HDR.size + length + 32 > len(blob):
        return None
    body = blob[:HDR.size + length]
    if hashlib.sha256(body).digest() != blob[HDR.size + length:HDR.size + length + 32]:
        return None
    return version


class Flash:
    def __init__(self, n_sectors: int):
        self.s = [b"\xFF" * SECTOR for _ in range(n_sectors)]
        self.status = None          # atomic record
        self.ops = 0                # operations performed
        self.cut_at = None          # power fails during operation number cut_at (0-based)

    class PowerCut(Exception):
        pass

    def _tick(self, sector: int | None):
        if self.cut_at is not None and self.ops == self.cut_at:
            if sector is not None:
                self.s[sector] = CORRUPT
            raise Flash.PowerCut
        self.ops += 1

    def erase(self, i: int):
        self._tick(i)
        self.s[i] = b"\xFF" * SECTOR

    def write(self, i: int, data: bytes):
        self._tick(i)
        self.s[i] = data

    def set_status(self, value):
        self._tick(None)            # a cut during a status write leaves the old record
        self.status = value


class Device:
    """Flash layout: [primary slot][secondary slot][scratch] (secondary and scratch unused by 'inplace')."""

    def __init__(self, scheme: str, n: int, old: list[bytes]):
        self.scheme, self.n = scheme, n
        self.f = Flash(2 * n + 1)
        for i, d in enumerate(old):
            self.f.s[i] = d

    def slot(self, k: int) -> list[bytes]:
        return self.f.s[k * self.n:(k + 1) * self.n]

    # ---------------------------------------------------------------- update procedures
    def download(self, new: list[bytes]):
        if self.scheme == "inplace":
            self.f.set_status(("writing",))
            for i, d in enumerate(new):
                self.f.erase(i)
                self.f.write(i, d)
            self.f.set_status(None)
        else:
            for i, d in enumerate(new):
                self.f.erase(self.n + i)
                self.f.write(self.n + i, d)
            self.f.set_status(("pending", 0, 0, "install"))

    def _swap_steps(self, start_i: int, start_step: int, mode: str = "install"):
        n, f, scr = self.n, self.f, 2 * self.n
        for i in range(start_i, n):
            first = start_step if i == start_i else 0
            if first <= 0:
                f.erase(scr)
                f.write(scr, f.s[i])
                f.set_status(("pending", i, 1, mode))
            if first <= 1:
                f.erase(i)
                f.write(i, f.s[n + i])
                f.set_status(("pending", i, 2, mode))
            if first <= 2:
                f.erase(n + i)
                f.write(n + i, f.s[scr])
                f.set_status(("pending", i + 1, 0, mode))
        # an installed image boots on trial; a reverted one is final
        f.set_status(("test",) if mode == "install" else None)

    def _overwrite_steps(self, start_i: int):
        n, f = self.n, self.f
        for i in range(start_i, n):
            f.erase(i)
            f.write(i, f.s[n + i])
            f.set_status(("pending", i + 1, 0, "install"))
        f.set_status(None)

    # ---------------------------------------------------------------- the bootloader
    def boot(self) -> int | None:
        st = self.f.status
        # resume an installation in progress: either it has started (progress recorded), or it is about to start
        # and the downloaded image is valid (an invalid download is never installed)
        if st is not None and st[0] == "pending" and (st[1] > 0 or st[2] > 0 or st[3] == "revert"
                                                      or validate(self.slot(1)) is not None):
            if self.scheme == "swap":
                self._swap_steps(st[1], st[2], st[3])
            elif self.scheme == "overwrite":
                self._overwrite_steps(st[1])
        elif st is not None and st[0] == "test" and self.scheme == "swap":
            # the new image was booted for a test but never confirmed: swap back (revert), recorded atomically
            self.f.set_status(("pending", 0, 0, "revert"))
            self._swap_steps(0, 0, "revert")
        return validate(self.slot(0))

    def confirm(self):
        if self.f.status is not None and self.f.status[0] == "test":
            self.f.set_status(None)


def run_with_cut(scheme: str, n: int, cut_at: int | None, confirm: bool = True, device_cls=None):
    """Download and install a new image (version 2 over version 1), cutting power during operation cut_at; then
    power up again (with no further cuts) and let the bootloader recover. Returns the version that boots, or None."""
    old, new = make_image(1, n), make_image(2, n)
    dev = (device_cls or Device)(scheme, n, old)
    dev.f.cut_at = cut_at
    try:
        dev.download(new)
        dev.boot()                 # first boot after the download performs the installation
        if confirm:
            dev.confirm()
    except Flash.PowerCut:
        pass
    dev.f.cut_at = None
    v = dev.boot()                 # recovery boot
    if confirm and v == 2:
        dev.confirm()
    return v


def count_ops(scheme: str, n: int) -> int:
    old, new = make_image(1, n), make_image(2, n)
    dev = Device(scheme, n, old)
    dev.download(new)
    dev.boot()
    dev.confirm()
    return dev.f.ops


def campaign(scheme: str, n: int = 6, device_cls=None) -> dict:
    """Cut power during each operation of a complete update in turn; device_cls lets a modified bootloader be tested."""
    total = count_ops(scheme, n)
    out = {"new": 0, "old": 0, "bricked": 0, "cuts": total, "bricking_cuts": []}
    for k in range(total):
        v = run_with_cut(scheme, n, k, device_cls=device_cls)
        if v is None:
            out["bricking_cuts"].append(k)
        out["new" if v == 2 else "old" if v == 1 else "bricked"] += 1
    return out


def revert_test(n: int = 6) -> int | None:
    """Swap in the new image, boot it but never confirm, reset: the bootloader must restore the old image."""
    old, new = make_image(1, n), make_image(2, n)
    dev = Device("swap", n, old)
    dev.download(new)
    first = dev.boot()
    assert first == 2
    return dev.boot()             # reset without confirm


# ------------------------------------------------------------------ budgets
def swap_time(image_bytes: int, sector_bytes: int, t_erase: float, t_write_sector: float, copies: int) -> float:
    """Time to move an image sector by sector, each sector copied `copies` times (erase plus write each time)."""
    n = -(-image_bytes // sector_bytes)
    return n * copies * (t_erase + t_write_sector)


def outage_probability(window_s: float, outages_per_month: float, month_s: float = 30 * 86400) -> float:
    """Probability that a Poisson outage process hits a window: 1 - exp(-rate * window)."""
    import math
    return 1 - math.exp(-outages_per_month / month_s * window_s)


def revert_campaign(n: int = 6) -> dict:
    """Install and test-boot the new image without confirming it, then cut power during every operation of the
    revert; the next boot must still end on a valid image (normally the old one)."""
    out = {"new": 0, "old": 0, "bricked": 0}
    k = 0
    while True:
        old, new = make_image(1, n), make_image(2, n)
        dev = Device("swap", n, old)
        dev.download(new)
        assert dev.boot() == 2
        base = dev.f.ops
        dev.f.cut_at = base + k
        try:
            dev.boot()                       # reset without confirm: revert, with a cut
            finished = True
        except Flash.PowerCut:
            finished = False
        dev.f.cut_at = None
        v = dev.boot()
        out["new" if v == 2 else "old" if v == 1 else "bricked"] += 1
        if finished:
            out["cuts"] = k
            return out
        k += 1
