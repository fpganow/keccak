#!/usr/bin/env python3


import os
from pathlib import Path
import platform
import re
import shutil


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

print(f'Platform: {platform.system()}')

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


target_path = Path('./vivado/src/ip')
print(f' + Copying files to: {target_path.as_posix()}')
shutil.copy2(dcp_path, target_path)
shutil.copy2(vhd_path, target_path)

# Now read vhd wrapper file and generate code for the testbench to use
testbench_code_str = get_testbench_code(vhd_path)

# Now I have to call a Windows script that uses the Vivado command line in batch mode
# chdir to target_path
os.chdir(target_path)

#vivado_settings_path = 'C:/Xilinx/Vivado/2019.1/settings64.bat'
#print('\n\n')
#print(f'Vivado Settings path: {vivado_settings_path}')
#print(f'vivado -mode batch')
#print(f'open_checkpoint C:/work/Ethereum/keccak/vivado/src/ip/NiFpgaAG_keccak_ip_fifo_control_export_ip.dcp')
#print(f'write_verilog -force ./vivado/src/ip/NiFpgaAG_keccak_ip_fifo_control_export_ip.v')
#print(f'write_vhdl -force ./vivado/src/ip/NiFpgaAG_keccak_ip_fifo_control_export_ip.vhd')
#print(f'close_project')
#print(f'quit')

print('\n\n')
print('Generated code (for your testbench)')
print('-' * 80)
print(f'{testbench_code_str}')
print('-' * 80)
#input("Press Enter to continue...")
