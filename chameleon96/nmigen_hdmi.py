from nmigen_boards.chameleon96 import Chameleon96Platform
from nmigen import *

# Depends on pergola_projects. To install:
# python3 -m pip install --user git+https://github.com/kbeckmann/pergola_projects
from pergola.gateware.vga import VGAOutput, VGAOutputSubtarget, VGAParameters
from pergola.gateware.vga_testimage import *

class HDMITest(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        led = platform.request("led")

        clk_freq = platform.default_clk_frequency
        timer = Signal(range(int(clk_freq//2)), reset=int(clk_freq//2) - 1)
        m.d.sync += timer.eq(timer + 1)

        m.d.comb += led.o.eq(timer[-1])

        vga_parameters = VGAParameters(
            h_front=110,
            h_sync=40,
            h_back=220,
            h_active=1280,
            v_front=5,
            v_sync=5,
            v_back=20,
            v_active=720,
        )

        tda19988 = platform.request("tda19988")
        bt = platform.request("bt")

        vga_output = Record([
            ('hs', 1),
            ('vs', 1),
            ('blank', 1),
        ])

        r = Signal(8)
        g = Signal(8)
        b = Signal(8)

        m.submodules.vga = VGAOutputSubtarget(
            output=vga_output,
            vga_parameters=vga_parameters,
        )

        m.submodules += TestImageGenerator(
        # m.submodules += StaticTestImageGenerator(
            vsync=vga_output.vs,
            h_ctr=m.submodules.vga.h_ctr,
            v_ctr=m.submodules.vga.v_ctr,
            r=r,
            g=g,
            b=b)


        m.d.comb += [
            # The muxes are there to illustrate the blanking areas
            tda19988.vpc.eq(Mux(vga_output.blank, Mux(vga_output.hs,    ~0, 0), r[-5:])),
            tda19988.vpa.eq(Mux(vga_output.blank, Mux(vga_output.vs,    ~0, 0), g[-5:])),
            tda19988.vpb.eq(Mux(vga_output.blank, Mux(vga_output.blank, ~0, 0), b[-6:])),

            # Data should be valid and settled on rising clock
            tda19988.pclk.eq(~ClockSignal()),

            # For some reason it seems the sync signals are not being recognized by the chip. Why?
            tda19988.hsync.eq(vga_output.hs),
            tda19988.vsync.eq(vga_output.vs),
            tda19988.de.eq(~vga_output.blank),
        ]

        return m

if __name__ == '__main__':
    plat = Chameleon96Platform()
    plat.build(HDMITest(), do_program=True)
