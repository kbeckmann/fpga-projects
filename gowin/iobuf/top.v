
// The vendor tool generates weird synthesized code with this

// module pin_led_io_0(led_io_0__oe, led_io_0__io, led_io_0__o);
//   wire \$1 ;
//   wire led_io_0__i;
//   inout led_io_0__io;
//   input led_io_0__o;
//   input led_io_0__oe;
//   assign \$1  = ~ led_io_0__oe;
//   IOBUF led_io_0_0 (
//     .I(led_io_0__o),
//     .IO(led_io_0__io),
//     .O(led_io_0__i),
//     .OEN(\$1 )
//   );
// endmodule


// module top(rgb_r);
//   inout rgb_r;
//   wire pin_led_io_0_led_io_0__o;
//   wire pin_led_io_0_led_io_0__oe;
//   pin_led_io_0 pin_led_io_0 (
//     .led_io_0__io(rgb_r),
//     .led_io_0__o(pin_led_io_0_led_io_0__o),
//     .led_io_0__oe(pin_led_io_0_led_io_0__oe)
//   );
//   assign pin_led_io_0_led_io_0__oe = 1'h1;
//   assign pin_led_io_0_led_io_0__o = 1'h1;
// endmodule

// However this works

module iobuf_wrapper(iobuf_o, iobuf_io, iobuf_oe);
    wire iobuf_i ;
    inout iobuf_io ;
    input iobuf_o ;
    input iobuf_oe ;

    IOBUF led_io_0_0 (
        .O(iobuf_o),
        .IO(iobuf_io),
        .I(iobuf_i),
        .OEN(iobuf_oe)
    );

endmodule

module top(
    led_r
);
    inout led_r;

    wire led_io_0__o;  //  = 1'b0;
    wire led_io_0__oe; //  = 1'b0;

    iobuf_wrapper wrapper (
        .iobuf_o(led_io_0__o),
        .iobuf_io(led_r),
        .iobuf_oe(led_io_0__oe)
    );

    assign led_io_0__o  = 1'h1;
    assign led_io_0__oe = 1'h1;

endmodule
