/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  reg [7:0] accum_reg;

  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      accum_reg <= 8'd0;
    end else if (ena) begin
      accum_reg <= accum_reg + ui_in;
    end
  end

  // All output pins must be assigned. If not used, assign to 0.
  assign uo_out  = accum_reg;

  assign uio_out = 8'd0;
  assign uio_oe  = 8'hFF;

  // List all unused inputs to prevent warnings
  wire _unused = &{uio_in, ena, 1'b0};

endmodule
