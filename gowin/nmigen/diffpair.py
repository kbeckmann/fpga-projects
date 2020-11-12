from nmigen import *
from nmigen.build import *

from nmigen_boards.tang_nano import TangNanoPlatform

class Blinky(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        # ---------------------
        # green: 16 = IOB7A
        # blue:  17 = IOB10A dp
        # red:   18 = IOB10B dm
        # ---------------------
        platform.add_resources([
            Resource("led_diff_blue_red", 0, DiffPairs("17", "18", dir="oe"),
                     Attrs(IO_TYPE="LVCMOS33D")),
        ])

        led = platform.request("led_diff_blue_red")

        clk_freq = platform.default_clk_frequency
        led_counter = Signal(range(int(clk_freq//2)), reset=int(clk_freq//2) - 1)

        oe_ctr = Signal(2)

        with m.If(led_counter == 0):
            m.d.sync += led_counter.eq(led_counter.reset)
            m.d.sync += oe_ctr.eq(oe_ctr + 1)
            m.d.sync += led.o.eq(~led.o)
            m.d.sync += led.oe.eq(oe_ctr[1])
        with m.Else():
            m.d.sync += led_counter.eq(led_counter - 1)

        return m

if __name__ == "__main__":
    p = TangNanoPlatform()
    p.build(Blinky(), do_program=True)

