-- VHDL wrapper for NiFpgaAG_keccak_ip_fifo_control_export_ip
-- Generated by LabVIEW FPGA IP Export Utility
--
-- Ports:
-- reset      :  Reset port. Minimum assertion length: 8 base clock cycles.
--               Minimum de-assertion length: 40 base clock cycles.
-- enable_in  :  Enable in port. Minimum re-initialization length: 7 base clock cycles.
-- enable_out :  Enable out port.
-- enable_clr :  Enable clear port.
-- ctrlind_00_TS_DATA_Valid : Top level control "TS_DATA.Valid", sync to Clk40, bool
-- ctrlind_01_TS_DATA_Element : Top level control "TS_DATA.Element", sync to Clk40, u64
-- ctrlind_02_TS_PARMS_Valid : Top level control "TS_PARMS.Valid", sync to Clk40, bool
-- ctrlind_03_TS_PARMS_Element : Top level control "TS_PARMS.Element", sync to Clk40, u64
-- ctrlind_04_TS_RESULTS_Ready : Top level control "TS_RESULTS.Ready", sync to Clk40, bool
-- ctrlind_05_Reset : Top level control "Reset", sync to Clk40, bool
-- ctrlind_06_TS_DATA_Ready : Top level indicator "TS_DATA.Ready", sync to Clk40, bool
-- ctrlind_07_TS_PARMS_Ready : Top level indicator "TS_PARMS.Ready", sync to Clk40, bool
-- ctrlind_08_TS_RESULTS_Valid : Top level indicator "TS_RESULTS.Valid", sync to Clk40, bool
-- ctrlind_09_TS_RESULTS_Element : Top level indicator "TS_RESULTS.Element", sync to Clk40, u64
-- Clk40 : Clock "40 MHz Onboard Clock", nominal frequency 40.00 MHz, base clock

library ieee;
use ieee.std_logic_1164.all;

entity NiFpgaIPWrapper_keccak_ip_fifo_control_export_ip is
		port (
			reset : in std_logic;
			enable_in : in std_logic;
			enable_out : out std_logic;
			enable_clr : in std_logic;
			ctrlind_00_TS_DATA_Valid : in std_logic_vector(0 downto 0);
			ctrlind_01_TS_DATA_Element : in std_logic_vector(63 downto 0);
			ctrlind_02_TS_PARMS_Valid : in std_logic_vector(0 downto 0);
			ctrlind_03_TS_PARMS_Element : in std_logic_vector(63 downto 0);
			ctrlind_04_TS_RESULTS_Ready : in std_logic_vector(0 downto 0);
			ctrlind_05_Reset : in std_logic_vector(0 downto 0);
			ctrlind_06_TS_DATA_Ready : out std_logic_vector(0 downto 0);
			ctrlind_07_TS_PARMS_Ready : out std_logic_vector(0 downto 0);
			ctrlind_08_TS_RESULTS_Valid : out std_logic_vector(0 downto 0);
			ctrlind_09_TS_RESULTS_Element : out std_logic_vector(63 downto 0);
			Clk40 : in std_logic
		);
end NiFpgaIPWrapper_keccak_ip_fifo_control_export_ip;

architecture vhdl_labview of NiFpgaIPWrapper_keccak_ip_fifo_control_export_ip is

	component NiFpgaAG_keccak_ip_fifo_control_export_ip
		port (
			reset : in std_logic;
			enable_in : in std_logic;
			enable_out : out std_logic;
			enable_clr : in std_logic;
			ctrlind_00_TS_DATA_Valid : in std_logic_vector(0 downto 0);
			ctrlind_01_TS_DATA_Element : in std_logic_vector(63 downto 0);
			ctrlind_02_TS_PARMS_Valid : in std_logic_vector(0 downto 0);
			ctrlind_03_TS_PARMS_Element : in std_logic_vector(63 downto 0);
			ctrlind_04_TS_RESULTS_Ready : in std_logic_vector(0 downto 0);
			ctrlind_05_Reset : in std_logic_vector(0 downto 0);
			ctrlind_06_TS_DATA_Ready : out std_logic_vector(0 downto 0);
			ctrlind_07_TS_PARMS_Ready : out std_logic_vector(0 downto 0);
			ctrlind_08_TS_RESULTS_Valid : out std_logic_vector(0 downto 0);
			ctrlind_09_TS_RESULTS_Element : out std_logic_vector(63 downto 0);
			Clk40 : in std_logic;
			tDiagramEnableOut : in std_logic
		);
	end component;

begin
	MyLabVIEWIP : NiFpgaAG_keccak_ip_fifo_control_export_ip
		port map(
			reset => reset,
			enable_in => enable_in,
			enable_out => enable_out,
			enable_clr => enable_clr,
			ctrlind_00_TS_DATA_Valid => ctrlind_00_TS_DATA_Valid,
			ctrlind_01_TS_DATA_Element => ctrlind_01_TS_DATA_Element,
			ctrlind_02_TS_PARMS_Valid => ctrlind_02_TS_PARMS_Valid,
			ctrlind_03_TS_PARMS_Element => ctrlind_03_TS_PARMS_Element,
			ctrlind_04_TS_RESULTS_Ready => ctrlind_04_TS_RESULTS_Ready,
			ctrlind_05_Reset => ctrlind_05_Reset,
			ctrlind_06_TS_DATA_Ready => ctrlind_06_TS_DATA_Ready,
			ctrlind_07_TS_PARMS_Ready => ctrlind_07_TS_PARMS_Ready,
			ctrlind_08_TS_RESULTS_Valid => ctrlind_08_TS_RESULTS_Valid,
			ctrlind_09_TS_RESULTS_Element => ctrlind_09_TS_RESULTS_Element,
			Clk40 => Clk40,
			tDiagramEnableOut => '1'
		);

end vhdl_labview;

