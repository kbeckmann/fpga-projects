from nmigen import *
from nmigen.build import *

import itertools

from nmigen_boards.tang_nano import TangNanoPlatform

class Blinky(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        def get_all_resources(name):
            resources = []
            for number in itertools.count():
                try:
                    resources.append(platform.request(name, number))
                except ResourceError:
                    break
            return resources

        rgb_leds = platform.request("rgb_led")
        leds = Cat([rgb_leds.r.o, rgb_leds.g.o, rgb_leds.b.o])
        btn = Cat([res.i for res in get_all_resources("button")])

        clk_freq = platform.default_clk_frequency
        timer = Signal(range(int(clk_freq//2)), reset=int(clk_freq//2) - 1)
        flops = Signal(len(leds))

        with m.If(btn == 0b00):
            m.d.comb += Cat(leds).eq(flops)
        with m.Elif(btn == 0b01):
            m.d.comb += Cat(leds).eq(0b100)
        with m.Elif(btn == 0b10):
            m.d.comb += Cat(leds).eq(0b010)
        with m.Else():
            m.d.comb += Cat(leds).eq(0b111)

        with m.If(timer == 0):
            m.d.sync += timer.eq(timer.reset)
            m.d.sync += flops.eq(flops + 1)
        with m.Else():
            m.d.sync += timer.eq(timer - 1)

        return m

if __name__ == "__main__":
    p = TangNanoPlatform()
    p.build(Blinky(), do_program=True)
