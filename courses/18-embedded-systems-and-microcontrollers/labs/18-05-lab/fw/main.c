/* Lab 18-05 firmware: a register-level driver for the CMSDK APB UART on QEMU's mps2-an386 board. */
#include <stdint.h>
#include "semihost.h"

typedef struct {
    volatile uint32_t DATA;      /* 0x00: write to send, read to receive */
    volatile uint32_t STATE;     /* 0x04: bit 0 TX buffer full, bit 1 RX buffer full; write 1 to clear overruns */
    volatile uint32_t CTRL;      /* 0x08: bit 0 TX enable, bit 1 RX enable */
    volatile uint32_t INTSTATUS; /* 0x0C */
    volatile uint32_t BAUDDIV;   /* 0x10: baud rate = PCLK / BAUDDIV, at least 16 */
} cmsdk_uart_t;

#define UART0 ((cmsdk_uart_t *)0x40004000u)
#define PCLK_HZ 25000000u        /* the UART clock QEMU gives this board (SYSCLK_FRQ, hw/arm/mps2.c) */

static void uart_init(uint32_t baud)
{
    UART0->CTRL = 0u;
    UART0->BAUDDIV = (PCLK_HZ + baud / 2u) / baud;   /* nearest integer divisor */
    UART0->CTRL = 1u;                                 /* TX enable */
}

static void uart_putc(char c)
{
    while (UART0->STATE & 1u) {                       /* wait while the TX buffer is full */
    }
    UART0->DATA = (uint8_t)c;
}

static void uart_puts(const char *s)
{
    while (*s)
        uart_putc(*s++);
}

static void uart_put_u32(uint32_t v)
{
    char buf[11];
    int i = 10;
    buf[i] = 0;
    do {
        buf[--i] = (char)('0' + v % 10u);
        v /= 10u;
    } while (v);
    uart_puts(&buf[i]);
}

int main(void)
{
    uart_init(115200u);
    uint32_t div = UART0->BAUDDIV;
    uart_puts("UART0 BAUDDIV ");
    uart_put_u32(div);
    uart_puts("\r\nUART0 actual baud ");
    uart_put_u32(PCLK_HZ / div);
    uart_puts("\r\nhello from the CMSDK UART\r\n");
    int ok = (div == 217u) && (UART0->CTRL == 1u);
    sh_puts(ok ? "TEST PASSED\n" : "TEST FAILED\n");
    return ok ? 0 : 1;
}
