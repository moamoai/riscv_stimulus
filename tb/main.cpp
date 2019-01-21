#include "Vtop.h"
#include "verilated.h"
#include "verilated_vcd_c.h"

int main(int argc, char **argv, char **env)
{
        int main_time;
	Vtop* top = new Vtop;

	Verilated::commandArgs(argc, argv);
        Verilated::traceEverOn(true);
        VerilatedVcdC* tfp = new VerilatedVcdC;
        top->trace(tfp, 99);
        tfp->open("top.vcd");

        while (!Verilated::gotFinish()) {
          if ((main_time % 10) == 1) {
              top->clk = 1;
          }
          if ((main_time % 10) == 6) {
              top->clk = 0;
          }
          top->eval(); 
          main_time++;
          tfp->dump(main_time);
          // top->flush_all();
          if(main_time > 0x100){ break;}
        }

        tfp->close();
	delete top;
	exit(0);
}
