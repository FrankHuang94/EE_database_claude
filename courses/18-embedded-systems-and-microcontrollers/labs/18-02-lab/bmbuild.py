"""Lab 18-02: build, inspect and run bare-metal Cortex-M4 firmware with LLVM and QEMU.

The firmware in fw/ is cross-compiled with clang for thumbv7em (Cortex-M4), linked by ld.lld with
fw/link.ld, inspected with llvm-size, llvm-nm and llvm-objdump, and run on QEMU's mps2-an386 board
(a Cortex-M4 FPGA image) with Arm semihosting for output and exit status.

Tools: clang, ld.lld, llvm-size, llvm-nm, llvm-objdump (package `llvm`, `clang`, `lld`) and
qemu-system-arm (package `qemu-system-arm`). The published numbers were produced with clang 18.1
and QEMU 8.2; other versions may lay code out differently.
"""
from __future__ import annotations

import glob
import math
import re
import shutil
import struct
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
FW = HERE / "fw"
TARGET = ["--target=thumbv7em-none-eabi", "-mcpu=cortex-m4", "-mthumb", "-mfloat-abi=soft"]
CFLAGS = ["-ffreestanding", "-nostdlib", "-fno-unwind-tables", "-fno-asynchronous-unwind-tables",
          "-std=c17", "-Wall", "-Wextra", "-Werror", "-g"]


def tool(name: str) -> str:
    """Path of an LLVM or QEMU tool, searching versioned LLVM directories too."""
    found = [g for pat in ("/usr/lib/llvm-*/bin/", "/opt/homebrew/opt/llvm/bin/", "/usr/local/opt/llvm/bin/")
             for g in sorted(glob.glob(pat + name))]
    path = shutil.which(name) or next(iter(found), None)
    if path is None:
        raise FileNotFoundError(f"{name} not found: install LLVM (clang, lld, llvm) and qemu-system-arm")
    return path


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


# ------------------------------------------------------------------ build
def build(out: Path, sources=("startup.c", "main.c"), opt="-O2", defines=(), mapfile: Path | None = None,
          fw_dir: Path = FW) -> Path:
    """Compile and link the firmware in `fw_dir` (default: this lab's fw/); return the ELF path.
    Raises on any compiler or linker error."""
    out = Path(out)
    fw_dir = Path(fw_dir)
    cmd = [tool("clang"), *TARGET, opt, *CFLAGS, *[f"-D{d}" for d in defines], "-fuse-ld=lld",
           "-Wl,-T," + str(fw_dir / "link.ld"), "-o", str(out), *[str(fw_dir / s) for s in sources]]
    if mapfile:
        cmd.insert(-len(sources), f"-Wl,-Map,{mapfile}")
    r = run(cmd)
    if r.returncode:
        raise RuntimeError("build failed:\n" + r.stderr)
    return out


def compile_object(src: str, out: Path, opt="-O2") -> Path:
    r = run([tool("clang"), *TARGET, opt, *CFLAGS, "-c", str(FW / src), "-o", str(out)])
    if r.returncode:
        raise RuntimeError("compile failed:\n" + r.stderr)
    return Path(out)


# ------------------------------------------------------------------ inspect
def sections(elf: Path) -> dict[str, tuple[int, int]]:
    """{section: (size, address)} for the allocated sections, from `llvm-size -A`."""
    out = {}
    for line in run([tool("llvm-size"), "-A", str(elf)]).stdout.splitlines():
        m = re.match(r"^(\.\S+)\s+(\d+)\s+(\d+)$", line.strip())
        if m and not m.group(1).startswith((".debug", ".comment", ".ARM.attributes")):
            out[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    return out


def berkeley(elf: Path) -> dict[str, int]:
    """The classic `size` report: text (code + constants + vectors), data, bss."""
    line = run([tool("llvm-size"), str(elf)]).stdout.splitlines()[1].split()
    return {"text": int(line[0]), "data": int(line[1]), "bss": int(line[2])}


def symbols(elf: Path) -> dict[str, int]:
    out = {}
    for line in run([tool("llvm-nm"), "-n", str(elf)]).stdout.splitlines():
        parts = line.split()
        if len(parts) == 3:
            out[parts[2]] = int(parts[0], 16)
    return out


def section_bytes(elf: Path, name: str) -> bytes:
    """Raw contents of one section, read directly from the ELF32 little-endian file."""
    data = Path(elf).read_bytes()
    assert data[:4] == b"\x7fELF" and data[4] == 1 and data[5] == 1, "expects ELF32 little-endian"
    shoff, = struct.unpack_from("<I", data, 0x20)
    shentsize, shnum, shstrndx = struct.unpack_from("<HHH", data, 0x2E)
    hdrs = [struct.unpack_from("<IIIIIIIIII", data, shoff + i * shentsize) for i in range(shnum)]
    strtab = hdrs[shstrndx]
    for h in hdrs:
        nm = data[strtab[4] + h[0]:].split(b"\0", 1)[0].decode()
        if nm == name:
            return data[h[4]:h[4] + h[5]]
    raise KeyError(name)


def vector_table(elf: Path, n=16) -> list[int]:
    raw = section_bytes(elf, ".isr_vector")
    return list(struct.unpack_from(f"<{n}I", raw, 0))


def disassemble(obj: Path, func: str) -> list[str]:
    """Mnemonic-and-operands lines of one function, without addresses, encodings or alignment nops."""
    text = run([tool("llvm-objdump"), "-d", "--no-show-raw-insn", str(obj)]).stdout
    out, inside = [], False
    for line in text.splitlines():
        if re.match(rf"^[0-9a-f]+ <{re.escape(func)}>:", line):
            inside = True
            continue
        if inside:
            if not line.strip() or re.match(r"^[0-9a-f]+ <", line):
                break
            ins = line.split(":", 1)[1].strip()
            ins = ins.split("@")[0].strip()
            if ins != "nop":
                out.append(ins)
    return out


# ------------------------------------------------------------------ run
def run_qemu(elf: Path, timeout=20) -> tuple[int, str]:
    """Run on QEMU mps2-an386 with semihosting; return (exit status, console output)."""
    r = run([tool("qemu-system-arm"), "-M", "mps2-an386", "-nographic", "-monitor", "none",
             "-semihosting-config", "enable=on,target=native", "-kernel", str(elf)], timeout=timeout)
    return r.returncode, r.stdout + r.stderr


# ------------------------------------------------------------------ models used by the chapter
def align(x: int, a: int = 4) -> int:
    return (x + a - 1) // a * a


def layout(flash_origin, ram_origin, ram_len, vectors, text, rodata, data, bss, stack):
    """Addresses the chapter's linker script assigns, for given section sizes (bytes)."""
    isr_end = flash_origin + align(vectors)
    etext = align(isr_end + text + rodata)
    sidata = etext
    sdata = ram_origin
    edata = align(sdata + data)
    sbss = edata
    ebss = align(sbss + bss)
    estack = ram_origin + ram_len
    return {"_etext": etext, "_sidata": sidata, "_sdata": sdata, "_edata": edata, "_sbss": sbss,
            "_ebss": ebss, "_estack": estack, "stack_bottom": estack - stack,
            "free_ram": estack - stack - ebss, "flash_used": sidata + (edata - sdata) - flash_origin}


def startup_cycles(data_bytes, bss_bytes, copy_cycles_per_word, zero_cycles_per_word, fixed=0):
    """Cycles spent before main(): copy .data word by word, zero .bss word by word."""
    return fixed + math.ceil(data_bytes / 4) * copy_cycles_per_word + math.ceil(bss_bytes / 4) * zero_cycles_per_word


if __name__ == "__main__":
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        elf = build(Path(d) / "fw.elf")
        print(sections(elf))
        print({k: hex(v) for k, v in symbols(elf).items() if k.startswith("_")})
        print([hex(w) for w in vector_table(elf)[:2]])
        print(run_qemu(elf))
