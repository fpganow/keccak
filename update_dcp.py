#!/usr/bin/env python3


import os
from pathlib import Path
import platform
import re
import shutil
from typing import Tuple


def get_testbench_code(vhd_path: Path) -> str:
	code_str = ''

	# entity name (NiFpgaIPWrapper_keccak_ip_fifo_control_export_ip
	entity_name = ''

	in_vars = []
	out_vars = []

	reading = False
	for line in vhd_path.read_text().split('\n'):
		if line.strip().startswith('entity'):
			reading = True
			entity_name = line.split()[1]
		elif line.strip().startswith('end'):
			break
		elif reading and 'ctrlind' in line:
			# ctrl_idx
			# direction
			# ctrl_size
			print(f'examining: {line}')
			# ctrlind_00_TS_Valid : in std_logic_vector(0 downto 0);
			ip_var = re.compile(f'ctrlind_(\d\d)_(\w+) : (\w+) std_logic_vector\((\d+) downto (\d+)\);')
			res = ip_var.findall(line)
			print(f'res: {res}')
			ctrl_idx = res[0][0]
			var_name = res[0][1]
			direction = res[0][2]
			ctrl_size = res[0][3]
			print(f'Control #: {ctrl_idx}')
			print(f'Variable Name: {var_name}')
			print(f'Direction: {direction}')
			print(f'Size: {ctrl_size}')
			print('\n')
			if direction == 'in':
				in_vars.append( (ctrl_idx, var_name, ctrl_size) )
			elif direction == 'out':
				out_vars.append( (ctrl_idx, var_name, ctrl_size) )

#		print(f'line:{line}')

	code_str = '    // Input Controls\n'
	for in_var in in_vars:
		(ctrl_idx, var_name, ctrl_size) = in_var
		code_str += f'    reg  [{ctrl_size:>2}:0] in_{var_name.lower()};\n'

	code_str += '\n'
	code_str += '    // Output Indicators\n'
	for out_var in out_vars:
		(ctrl_idx, var_name, ctrl_size) = out_var
		code_str += f'    wire  [{ctrl_size:>2}:0] out_{var_name.lower()};\n'

	code_str += f"""\
    {entity_name} UUT (
        .reset(0),
        .enable_in(1),
        .enable_out(),
        .enable_clr(0),
"""
	for in_var in in_vars:
		(ctrl_idx, var_name, ctrl_size) = in_var
		code_str += f'        .ctrlind_{ctrl_idx}_{var_name}(in_{var_name.lower()}),\n'
	for out_var in out_vars:
		(ctrl_idx, var_name, ctrl_size) = out_var
		code_str += f'        .ctrlind_{ctrl_idx}_{var_name}(out_{var_name.lower()}),\n'

	code_str += '        .Clk40(clk)\n'
	code_str += '    );\n'
	return code_str


def get_compilation_files() -> Tuple[Path, Path]:
	base_path = ''
	if platform.system() == 'Windows':
		base_path = 'C:/'
	elif platform.system() == 'Linux':
		base_path = '/mnt/c/'

	# NI Compilation path
	ni_comp_path = Path(base_path + 'NIFPGA/compilation')

	latest_dir = max(list(x for x in ni_comp_path.glob('*') if x.is_dir()), key=os.path.getmtime)
	src_dir = latest_dir.joinpath('source_files')

	print(f' + Using NI FPGA compilation directory:')
	print(f'   {src_dir}')

	dcp_path = None
	vhd_path = None
	for child in src_dir.iterdir():
    		if child.name.endswith('dcp'):
        		dcp_path = child
    		elif child.name.endswith('vhd'):
        		vhd_path = child
    		else:
        		print(f'unknown file found: {child}')

	print(f' + Using the following Xilinx dcp file:')
	print(f'   {dcp_path}')

	print(f' + Using the following VHDL wrapper file:')
	print(f'   {vhd_path}')

	return (dcp_path, vhd_path)

def get_tcl_script(target_path: Path, dcp_path: Path) -> str:
	target_path = target_path.resolve()
	print(f'target_path: {target_path.as_posix()}')

	new_dcp_path = target_path.joinpath(dcp_path.name)
	print(f'new_dcp_path: {new_dcp_path.as_posix()}')

	vhd_sim_path = target_path.joinpath(dcp_path.stem + '.vhd')
	print(f'vhd_sim_path: {vhd_sim_path.as_posix()}')

	v_sim_path = target_path.joinpath(dcp_path.stem + '.v')
	print(f'v_sim_path: {v_sim_path.as_posix()}')

	update_sim = f"""\
open_checkpoint {new_dcp_path.as_posix()}
write_verilog -force {v_sim_path.as_posix()}
write_vhdl -force {vhd_sim_path.as_posix()}
quit
"""
	return update_sim






# Print Header
print(f'Platform: {platform.system()}')

# Step 1 - Find latest compilation directory
(dcp_path, vhd_path) = get_compilation_files()

# Step 2 - Copy vhd and dcp to ./vivado/src/ip
target_path = Path('./vivado/src/ip')
print(f' + Copying files to: {target_path.as_posix()}')
shutil.copy2(dcp_path, target_path)
shutil.copy2(vhd_path, target_path)

# Step 3 - Parse vhd wrapper file to generate code suitable for importing from test bench
testbench_code_str = get_testbench_code(vhd_path)

# Step 4 - Run Vivado in batch mode to generate verilog and vhdl files from dcp
# Step 4a - Generate tcl script
update_tcl_script = get_tcl_script(target_path, dcp_path)

# Step 4b - Write tcl script to temporary file
tcl_script = 'update.tcl'
Path(tcl_script).write_text(update_tcl_script)

# Step 5b - Execute tcl script
print('\n\n')
vivado_settings_path = 'C:/Xilinx/Vivado/2019.1/settings64.bat'
win_cmd = f'{vivado_settings_path} & vivado -mode batch -source {tcl_script}'
print('To run tcl')
print(f'{win_cmd}')

# Step 6 - Print Generate code for testbench
print('\n\n')
print('//' + '-' * 80)
print('// Generated code (for VHDL testbench)')
print(f'{testbench_code_str}')
print('//' + '-' * 80)


# Pause
#input("Press Enter to continue...")
