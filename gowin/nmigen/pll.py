from nmigen import *
from nmigen.build import *

from nmigen_boards.tang_nano import TangNanoPlatform

class Blinky(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        platform.add_resources([
            Resource("led", 0, Pins("18", dir="o"),
                     Attrs(IOSTANDARD="LVCMOS33")),
        ])

        cd_name = "pll"

        lock_o = Signal()
        clkoutp_o = Signal()
        clkoutd_o = Signal()
        clkoutd3_o = Signal()

        m.domains += ClockDomain(cd_name)
        m.d.comb += ResetSignal(cd_name).eq(~lock_o),

        clock_name = platform.default_clk
        clkin_frequency = platform.lookup(clock_name).clock.frequency / 1e6
        clkin = platform.request(clock_name)
        clkout = Signal()

        m.d.comb += ClockSignal(domain=cd_name).eq(clkout)

        # The parameters are hard-coded to pll 24MHz => 48 MHz
        clkout_freq = 48e6

        m.submodules.pll = Instance("rPLL",
            o_CLKOUT=clkout,
            o_LOCK=lock_o,
            o_CLKOUTP=clkoutp_o,
            o_CLKOUTD=clkoutd_o,
            o_CLKOUTD3=clkoutd3_o,
            i_RESET=0,
            i_RESET_P=0,
            i_CLKIN=clkin,
            i_CLKFB=0,
            i_FBDSEL=0,
            i_IDSEL=0,
            i_ODSEL=0,
            i_PSDA=0,
            i_DUTYDA=0,
            i_FDLY=0,

            # 24MHz in => 48 MHz out
            p_FCLKIN="24",
            p_DYN_IDIV_SEL="false",
            p_IDIV_SEL=2,
            p_DYN_FBDIV_SEL="false",
            p_FBDIV_SEL=7,
            p_DYN_ODIV_SEL="false",
            p_ODIV_SEL=8,
            p_PSDA_SEL="0000",
            p_DYN_DA_EN="true",
            p_DUTYDA_SEL="1000",
            p_CLKOUT_FT_DIR=1,
            p_CLKOUTP_FT_DIR=1,
            p_CLKOUT_DLY_STEP=0,
            p_CLKOUTP_DLY_STEP=0,
            p_CLKFB_SEL="internal",
            p_CLKOUT_BYPASS="false",
            p_CLKOUTP_BYPASS="false",
            p_CLKOUTD_BYPASS="false",
            p_DYN_SDIV_SEL=2,
            p_CLKOUTD_SRC="CLKOUT",
            p_CLKOUTD3_SRC="CLKOUT",
            p_DEVICE="GW1N-1",
        )

        led = platform.request("rgb_led")

        led_counter = Signal(range(int(clkout_freq//2)), reset=int(clkout_freq//2) - 1)

        platform.add_clock_constraint(clkout, clkout_freq)

        with m.If(led_counter == 0):
            m.d.pll += led_counter.eq(led_counter.reset)
            m.d.pll += Cat(led.r.o, led.g.o, led.b.o).eq(~led.r.o)
        with m.Else():
            m.d.pll += led_counter.eq(led_counter - 1)

        return m

if __name__ == "__main__":
    p = TangNanoPlatform()
    p.build(Blinky(), do_program=True)
