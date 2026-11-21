/* Linker script for the Lab 18-02 firmware on QEMU's mps2-an386 (Cortex-M4).
 * The board's code memory at 0x0000 0000 stands in for flash; its SRAM is at 0x2000 0000.
 * Lengths are cut down to the sizes of a small MCU so the map is easy to read. */
ENTRY(Reset_Handler)

MEMORY
{
  FLASH (rx)  : ORIGIN = 0x00000000, LENGTH = 256K
  RAM   (rwx) : ORIGIN = 0x20000000, LENGTH = 64K
}

_stack_size = 0x1000;                       /* 4 KiB reserved for the main stack */
_estack     = ORIGIN(RAM) + LENGTH(RAM);    /* the stack grows down from the top of SRAM */

SECTIONS
{
  .isr_vector : ALIGN(4)
  {
    KEEP(*(.isr_vector))                    /* must be first: the core reads words 0 and 1 at reset */
  } > FLASH

  .text : ALIGN(4)
  {
    *(.text .text.*)
    *(.rodata .rodata.*)
    . = ALIGN(4);
    _etext = .;
  } > FLASH

  .ARM.exidx : { *(.ARM.exidx*) } > FLASH   /* unwind tables, if the compiler emits any */

  .data : ALIGN(4)
  {
    _sdata = .;                             /* run-time (VMA) start in SRAM */
    *(.data .data.*)
    . = ALIGN(4);
    _edata = .;
  } > RAM AT > FLASH
  _sidata = LOADADDR(.data);                /* load (LMA) address of the initial values in flash */

  .bss (NOLOAD) : ALIGN(4)
  {
    _sbss = .;
    *(.bss .bss.* COMMON)
    . = ALIGN(4);
    _ebss = .;
  } > RAM

  ASSERT(_ebss + _stack_size <= _estack, "SRAM overflow: .data + .bss + stack do not fit")
}
