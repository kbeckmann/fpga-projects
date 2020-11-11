from nmigen import *
from nmigen.build import *

import itertools

from nmigen_boards.tang_nano import TangNanoPlatform

class Blinky(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        platform.add_resources([
            Resource("led_io", 0, Pins("18", invert=True),
                     Attrs(IO_TYPE="LVCMOS33")),
        ])

        # Pick one:
        io_dir = "io"
        # io_dir = "oe"
        # io_dir = "o"

        led = platform.request("led_io", 0, dir=io_dir)
        m.d.comb += led.o.eq(1)
        if io_dir == "io" or io_dir == "oe":
            m.d.comb += led.oe.eq(1)

        return m

if __name__ == "__main__":
    p = TangNanoPlatform()
    p.build(Blinky(), do_program=True)
