
module top(
`ifdef VERILATOR
    input logic clk
`endif // VERILATOR
);
  logic [9:0]   pc;
  logic [1023:0] hex_file = "../hello.hex";
  logic [7:0]    imem [0:1023];

  initial begin
    $display(hex_file);
    $display("Hello");
    $readmemh(hex_file, imem);
    pc = 0;
    //$finish();
  end
  always @(posedge clk) begin
    pc <= pc + 1;
    $display("pc: %08x inst: %08x", pc, inst);
  end

  logic [7:0] inst;
  assign inst = imem[pc];

endmodule

