from nmigen_boards.chameleon96 import Chameleon96Platform
from nmigen import *

class Blinky(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        led = platform.request("led")

        clk_freq = platform.default_clk_frequency
        timer = Signal(range(int(clk_freq//2)), reset=int(clk_freq//2) - 1)
        m.d.sync += timer.eq(timer + 1)

        m.d.comb += led.o.eq(timer[-1])

        return m

if __name__ == '__main__':
    plat = Chameleon96Platform()
    plat.build(Blinky(), do_program=True)
