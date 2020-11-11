from nmigen import *
from nmigen.build import *

from nmigen_boards.tang_nano import TangNanoPlatform

class Blinky(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        led = platform.request("rgb_led")

        clk_freq = platform.default_clk_frequency
        led_counter = Signal(range(int(clk_freq//2)), reset=int(clk_freq//2) - 1)

        with m.If(led_counter == 0):
            m.d.sync += led_counter.eq(led_counter.reset)
            m.d.sync += led.r.o.eq(~led.r.o)
        with m.Else():
            m.d.sync += led_counter.eq(led_counter - 1)

        return m

if __name__ == "__main__":
    p = TangNanoPlatform()
    p.build(Blinky(), do_program=True)
