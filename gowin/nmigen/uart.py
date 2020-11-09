from nmigen import *
from nmigen.build import *
from nmigen_boards.resources import *

import itertools

from nmigen_boards.tang_nano import TangNanoPlatform

from pergola.gateware.uart import *


class UARTExample(Elaboratable):
    def __init__(self, baudrate, stopbits):
        self.baudrate = baudrate
        self.stopbits = stopbits

    def elaborate(self, platform):
        led = platform.request("rgb_led", 0).r.o

        uart_pins = platform.request("uart", 0)

        m = Module()

        m.submodules.uart = uart = UART(
            divisor=round(platform.default_clk_frequency / self.baudrate),
            stopbits=self.stopbits
        )

        m.d.comb += uart.rx_i.eq(uart_pins.rx)
        m.d.comb += uart_pins.tx.eq(uart.tx_o)

        m.d.comb += led.eq(uart.rx_data[0])

        with m.If(~uart.rx_err & uart.rx_rdy & ~uart.rx_ack):
            m.d.sync += [
                uart.tx_rdy.eq(1),
                uart.tx_data.eq(uart.rx_data),
                uart.rx_ack.eq(1)
            ]
        with m.Elif(uart.tx_ack):
            m.d.sync += uart.tx_rdy.eq(0)
            m.d.sync += uart.rx_rdy.eq(0)
            m.d.sync += uart.rx_ack.eq(0)

        return m


if __name__ == "__main__":
    p = TangNanoPlatform()
    p.build(UARTExample(115200, 1), do_program=True)
