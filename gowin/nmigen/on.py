from nmigen import *
from nmigen.build import *

import itertools

from nmigen_boards.tang_nano import TangNanoPlatform

class Blinky(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        rgb_leds = platform.request("rgb_led")
        m.d.sync += rgb_leds.eq(0b111)

        return m

if __name__ == "__main__":
    p = TangNanoPlatform()
    p.build(Blinky(), do_program=True)
