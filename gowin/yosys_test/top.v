module top(
    clk24,
    led_r,
    led_g,
    led_b,
);
    input  clk24;
    output led_r;
    output led_g;
    output led_b;

    reg [22:0] counter;
    reg [2:0] leds = 3'b110;

    assign led_r = leds[0];
    assign led_g = leds[1];
    assign led_b = leds[2];

    wire [2:0] leds_next = {leds[0], leds[2:1]};

    always @(posedge clk24) begin
        if (counter == 22'b0)
            leds <= leds_next;
    end

    always @(posedge clk24) begin
       counter <= counter + 1'b1; 
    end

endmodule