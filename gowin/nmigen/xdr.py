from nmigen import *
from nmigen.build import *

from nmigen_boards.tang_nano import TangNanoPlatform

class BlinkyXDROut(Elaboratable):
    def __init__(self, xdr):
        self.xdr = xdr

    def elaborate(self, platform):
        m = Module()

        platform.add_resources([
            Resource("led", 0, Pins("17", dir="oe"),
                        Attrs(IO_TYPE="LVCMOS33")),
        ])
        
        xdr = self.xdr
        led = platform.request("led", xdr=xdr)

        clk_freq = platform.default_clk_frequency
        led_counter = Signal(range(int(clk_freq//2)), reset=int(clk_freq//2) - 1)

        xdr_clk = Signal(1)
        m.domains += ClockDomain("xdr")
        m.d.comb += ClockSignal(domain="xdr").eq(xdr_clk)

        # Set to True to show the issue with DFF INIT when xdr=1
        if False:
            m.d.comb += led.oe.eq(0)
        else:
            m.d.comb += led.oe.eq(1)
            m.d.xdr += led.o.eq(~led.o)

        if xdr > 0:
            m.d.comb += led.o_clk.eq(xdr_clk)

        with m.If(led_counter == 0):
            m.d.sync += led_counter.eq(led_counter.reset)
            m.d.sync += xdr_clk.eq(~xdr_clk)
        with m.Else():
            m.d.sync += led_counter.eq(led_counter - 1)

        # m.submodules += Instance("DFFR",
        #     i_D=Const(1),
        #     o_Q=led.o,
        #     i_CLK=Const(1),
        #     i_RESET=Const(1),
        #     p_INIT=1
        # )

        return m

class BlinkyXDRIn(Elaboratable):
    def __init__(self, xdr):
        self.xdr = xdr

    def elaborate(self, platform):
        m = Module()

        xdr = self.xdr
        rgb_led = platform.request("rgb_led")
        
        btn = platform.request("button", xdr=xdr)

        clk_freq = platform.default_clk_frequency
        led_counter = Signal(range(int(clk_freq//2)), reset=int(clk_freq//2) - 1)

        xdr_clk = Signal(1)
        m.domains += ClockDomain("xdr")
        m.d.comb += ClockSignal(domain="xdr").eq(xdr_clk)

        if xdr > 0:
            m.d.comb += btn.i_clk.eq(xdr_clk)

        with m.If(led_counter == 0):
            m.d.sync += led_counter.eq(led_counter.reset)
            m.d.sync += xdr_clk.eq(~xdr_clk)
        with m.Else():
            m.d.sync += led_counter.eq(led_counter - 1)

        # xdr clock high => red led on
        m.d.comb += rgb_led.r.o.eq(ClockSignal("xdr"))

        # Connect button input straight to the green led
        m.d.comb += rgb_led.g.o.eq(btn.i)

        return m

if __name__ == "__main__":
    p = TangNanoPlatform()
    # p.build(BlinkyXDROut(xdr=0), do_program=True)
    p.build(BlinkyXDROut(xdr=1), do_program=True)
    # p.build(BlinkyXDROut(xdr=2), do_program=True)

    # p.build(BlinkyXDRIn(xdr=0), do_program=True)
    # p.build(BlinkyXDRIn(xdr=1), do_program=True)
    # p.build(BlinkyXDRIn(xdr=2), do_program=True)

