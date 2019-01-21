
default: comp
comp:
	verilator -Wall --trace --cc top.sv --exe main.cpp
	make -C obj_dir -f Vtop.mk
	obj_dir/Vtop
comp_moto:
	verilator -Wall --cc tvmix_calc.v --exe tvmix_calc.cpp
	make -C obj_dir -f Vtvmix_calc.mk
	obj_dir/Vtvmix_calc

clean:
	rm -rf obj_dir/ top.vcd
