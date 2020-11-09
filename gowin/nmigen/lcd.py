from nmigen import *
from nmigen.build import *

import os
import subprocess
import itertools

# Depends on pergola_projects. To install:
# python3 -m pip install --user git+https://github.com/kbeckmann/pergola_projects
from pergola.gateware.vga import *
from pergola.gateware.vga_testimage import *

from nmigen_boards.tang_nano import TangNanoPlatform

class LCDExample(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        rgb_leds = platform.request("rgb_led")

        clk_freq = platform.default_clk_frequency
        timer = Signal(range(int(clk_freq//2)), reset=int(clk_freq//2) - 1)
        flops = Signal()

        m.d.comb += rgb_leds.r.o.eq(flops)
        with m.If(timer == 0):
            m.d.sync += timer.eq(timer.reset)
            m.d.sync += flops.eq(~flops)
        with m.Else():
            m.d.sync += timer.eq(timer - 1)

        lcd = platform.request("lcd", 0)

        vga_output = Record([
            ('hs', 1),
            ('vs', 1),
            ('blank', 1),
        ])
        vga_parameters = VGAParameters(
                h_front=24,
                h_sync=72,
                h_back=96,
                h_active=800,
                v_front=3,
                v_sync=7,
                v_back=10,
                v_active=480,
            )
        m.submodules.vga = VGAOutputSubtarget(vga_output, vga_parameters)

        r = Signal(8)
        g = Signal(8)
        b = Signal(8)
        m.submodules.imagegen = TestImageGenerator(
                vsync=vga_output.vs,
                h_ctr=m.submodules.vga.h_ctr,
                v_ctr=m.submodules.vga.v_ctr,
                r=r,
                g=g,
                b=b,
                speed=0
            )

        m.d.comb += [
            lcd.den.eq(~vga_output.blank),
            lcd.pclk.eq(ClockSignal()),
            lcd.hs.eq(vga_output.hs),
            lcd.vs.eq(vga_output.vs),
            lcd.r.eq(r[-5:]),
            lcd.g.eq(g[-6:]),
            lcd.b.eq(b[-5:]),
        ]

        return m

if __name__ == "__main__":
    p = TangNanoPlatform()
    p.build(LCDExample(), do_program=True)
