# keccak
LabVIEW FPGA Implementation of Keccak

Based on the implementation of Keccak found in the ethash library here:
https://github.com/chfast/ethash/blob/master/lib/keccak/keccak.c


*LabVIEW 2021 64-bit*

NI High-Speed Serial PXIe-6592R used for demonstration purposes and has the following resources:
- Family: Kintex-7
- Type: xc7k410t
- Speed Grade: -2
- Package: ffg900


**To Use from Vivado see this VHDL wrapper**

https://github.com/fpganow/keccak/blob/main/labview/ip_export/NiFpgaIPWrapper_keccak_ip_fifo_control_export.vhd

---
Online Keccak Calculator

http://emn178.github.io/online-tools/keccak_256.html
http://emn178.github.io/online-tools/keccak_512.html
