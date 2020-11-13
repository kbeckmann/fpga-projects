from nmigen import *
from nmigen.build import *

from nmigen_boards.tang_nano import TangNanoPlatform

class BlinkyXDROut(Elaboratable):
    def __init__(self, xdr):
        self.xdr = xdr

    def elaborate(self, platform):
        m = Module()

        # io_dir = "oe"
        # io_dir = "io"
        io_dir = "o"

        platform.add_resources([
            Resource("led", 0, Pins("17"),
                        Attrs(IO_TYPE="LVCMOS33")),
        ])
        
        xdr = self.xdr
        led = platform.request("led", xdr=xdr, dir=io_dir)

        clk_freq = platform.default_clk_frequency
        led_counter = Signal(range(int(clk_freq//2)), reset=int(clk_freq//2) - 1)

        xdr_clk = Signal(1)
        m.domains += ClockDomain("xdr")
        m.d.comb += ClockSignal(domain="xdr").eq(xdr_clk)

        # Illustrates the issue with DFF INIT when xdr=1
        # m.d.comb += led.oe.eq(0)

        if io_dir in ("oe", "io"):
            m.d.comb += led.oe.eq(1)

        if xdr <= 1:
            m.d.xdr += led.o.eq(~led.o)
        elif xdr == 2:
            m.d.comb += led.o0.eq(1)
            m.d.comb += led.o1.eq(0)

        if xdr > 0:
            m.d.comb += led.o_clk.eq(xdr_clk)

        with m.If(led_counter == 0):
            m.d.sync += led_counter.eq(led_counter.reset)
            m.d.sync += xdr_clk.eq(~xdr_clk)
        with m.Else():
            m.d.sync += led_counter.eq(led_counter - 1)


        return m

# Needs some manual hacks in the .vg file, but it works!
class BlinkyXDR10Out(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        platform.add_resources([
            Resource("led", 0, Pins("17"),
                        Attrs(IO_TYPE="LVCMOS33")),
        ])
        
        led = platform.request("led", dir="o")

        clk_freq = platform.default_clk_frequency
        led_counter = Signal(range(int(clk_freq//2)), reset=int(clk_freq//2) - 1)

        fclk = Signal(1)
        m.domains += ClockDomain("fclk")
        m.d.comb += ClockSignal(domain="fclk").eq(fclk)

        pclk = Signal(1)
        pclk_cnt = Signal(3)
        m.domains += ClockDomain("pclk")
        m.d.comb += ClockSignal(domain="pclk").eq(pclk)

        with m.If(led_counter == 0):
            m.d.sync += led_counter.eq(led_counter.reset)
            m.d.sync += fclk.eq(~fclk)
        with m.Else():
            m.d.sync += led_counter.eq(led_counter - 1)

        with m.If(pclk_cnt == 0):
            m.d.fclk += pclk.eq(~pclk)
            m.d.fclk += pclk_cnt.eq(5)
        with m.Else():
            m.d.fclk += pclk_cnt.eq(pclk_cnt - 1)

        serdes_data = Signal()

        m.submodules.lvds = Instance("ELVDS_OBUF",
            i_I=serdes_data,
            o_O=led_p.o,
            o_OB=led_n.o,
        )

        m.submodules.oser = Instance("OSER10",
            i_D0=Const(1),
            i_D1=Const(0),
            i_D2=Const(0),
            i_D3=Const(0),
            i_D4=Const(0),
            i_D5=Const(0),
            i_D6=Const(0),
            i_D7=Const(0),
            i_D8=Const(0),
            i_D9=Const(0),
            o_Q=serdes_data,
            i_PCLK=ClockSignal("pclk"),
            i_FCLK=ClockSignal("fclk"),
            i_RESET=Const(0),
        )

        return m

class BlinkyXDRIn(Elaboratable):
    def __init__(self, xdr):
        self.xdr = xdr

    def elaborate(self, platform):
        m = Module()

        # io_dir = "oe"
        # io_dir = "io"
        io_dir = "i"

        platform.add_resources([
            Resource("btn", 0, Pins("14"),
                        Attrs(IO_TYPE="LVCMOS33")),
        ])

        xdr = self.xdr
        rgb_led = platform.request("rgb_led")
        
        btn = platform.request("button", xdr=xdr, dir=io_dir)

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

        if io_dir in ("oe", "io"):
            m.d.comb += led.oe.eq(0)

        if xdr == 0 or xdr == 1:
            # Connect button input straight to the green led
            m.d.comb += rgb_led.g.o.eq(btn.i)
        elif xdr == 2:
            # Rising edge  => green
            # Falling edge => blue
            m.d.comb += rgb_led.g.o.eq(btn.i0)
            m.d.comb += rgb_led.b.o.eq(btn.i1)

        return m

if __name__ == "__main__":
    p = TangNanoPlatform()
    # p.build(BlinkyXDROut(xdr=0), do_program=True)
    # p.build(BlinkyXDROut(xdr=1), do_program=True)
    # p.build(BlinkyXDROut(xdr=2), do_program=True)

    # p.build(BlinkyXDR10Out(), do_program=True)

    # p.build(BlinkyXDRIn(xdr=0), do_program=True)
    # p.build(BlinkyXDRIn(xdr=1), do_program=True)
    p.build(BlinkyXDRIn(xdr=2), do_program=True)

