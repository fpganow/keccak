`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 03/07/2022 03:49:21 PM
// Design Name: 
// Module Name: keccak_ip_tb
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module keccak_ip_tb;
    // 10ns = 100 MHz
    // 20ns = 50 MHz
    // 25ns = 40MHz
    // duration for each bit = 20 * timescale = 20 * 1 ns = 20 ns
    localparam period = 25;
    localparam duty_cycle = period / 2.0;

    reg clk;

    always
    begin
        clk = 1'b1;
        #duty_cycle;

        clk = 1'b0;
        #duty_cycle;
    end

    // Output indicators
//    wire [0:0] out_data_ready;
//    wire [0:0] out_parms_ready;
//    wire [0:0] out_results_valid;
//    wire [63:0] out_results;

//    // Input controls
//    reg  [0:0] in_read_results;
//    reg [63:0] in_parms;
//    reg  [0:0] in_parms_valid;
//    reg [63:0] in_data;
//    reg  [0:0] in_data_valid;

    // Input Controls
    reg  [ 0:0] in_ts_data_valid;
    reg  [63:0] in_ts_data_element;
    reg  [ 0:0] in_ts_parms_valid;
    reg  [63:0] in_ts_parms_element;
    reg  [ 0:0] in_ts_results_ready;
    reg  [ 0:0] in_reset;

    // Output Indicators
    wire  [ 0:0] out_ts_data_ready;
    wire  [ 0:0] out_ts_parms_ready;
    wire  [ 0:0] out_ts_results_valid;
    wire  [63:0] out_ts_results_element;

    NiFpgaIPWrapper_keccak_ip_fifo_control_export_ip UUT (
        .reset(0),
        .enable_in(1),
        .enable_out(),
        .enable_clr(0),
        .ctrlind_00_TS_DATA_Valid(in_ts_data_valid),
        .ctrlind_01_TS_DATA_Element(in_ts_data_element),
        .ctrlind_02_TS_PARMS_Valid(in_ts_parms_valid),
        .ctrlind_03_TS_PARMS_Element(in_ts_parms_element),
        .ctrlind_04_TS_RESULTS_Ready(in_ts_results_ready),
        .ctrlind_05_Reset(in_reset),
        .ctrlind_06_TS_DATA_Ready(out_ts_data_ready),
        .ctrlind_07_TS_PARMS_Ready(out_ts_parms_ready),
        .ctrlind_08_TS_RESULTS_Valid(out_ts_results_valid),
        .ctrlind_09_TS_RESULTS_Element(out_ts_results_element),
        .Clk40(clk)
    );


    integer fptr;
    integer f_data;
    integer scan_faults;

    integer i;
    reg[63:0] test_data;

    reg[31:0] test_size;
    reg[64 * 4:0] exp_hash_256;
    reg[64 * 8:0] exp_hash_512;

    initial
    begin
        // Initial defaults
        in_reset = 1'b0;
        in_ts_results_ready = 1'b0;
        in_ts_parms_element = 64'b0;
        in_ts_parms_valid = 1'b0;
        in_ts_data_element = 64'b0;
        in_ts_data_valid = 1'b0;

        #(period * 10)
        // Now wait for UUT to say it is ready for a command
        // (and ignore the initial value which is usually 1)
        // * 10 = 5 clock cycles
        #period;
        in_reset = 1'b1;

        #period;
        in_reset = 1'b0;
        
        // Extra reset
        #(period * 5);
        in_reset = 1'b1;
        #period;
        in_reset = 1'b0;

        #(period * 5);

        // Wait for IP to be ready
        wait(out_ts_data_ready);
        wait(out_ts_parms_ready);

        in_ts_parms_element = {32'd512, 32'd0};
        in_ts_parms_valid = 1'b1;
        #period;

        in_ts_parms_valid = 1'b0;
        in_ts_results_ready = 1'b1;

        wait(out_ts_results_valid);
        // test_data.dat
        //   6168747345207341
        //   6465727269747320
        f_data = $fopen("test_data.dat", "r");
        if(f_data == 0)
        begin
            $display("Error opening test_data.dat.");
            $finish;
        end

        // exp_results.dat
        //   0 c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470 0eab42de4c3ceb9235fc91acffe746b29c29a8c366b7c60e4e67c466f36a4304c00fa9caf9d87976ba469bcbe06713b435f091ef2769fb160cdab33d3670680e
        fptr = $fopen("exp_results.dat", "r");
        if(fptr == 0)
        begin
            $display("Error opening exp_results.dat.");
            $finish;
        end
        while (!$feof(fptr))
        begin
            scan_faults = $fscanf(fptr, "%d %h %h", test_size, exp_hash_256, exp_hash_512);
            #period;

            // Send test size and bits
            //in_parms = {test_size, 32'd256};
            in_ts_parms_element = {32'd256, 32'd0};
            in_ts_parms_valid = 1'b1;
            #period;

            in_ts_parms_element = 64'd0;
            in_ts_parms_valid = 1'b0;

            wait(out_ts_results_valid);
            #period;
            #period;
            #period;
            #period;
            #period;

            // Now send in test data for 256 bit
            if (test_size > 0)
            begin
                i = 0;
                while (!$feof(f_data) && i < test_size)
                begin
                    scan_faults = $fscanf(f_data, "%h", test_data);

                    in_ts_data_element = test_data;
                    in_ts_data_valid = 1'b1;
                    #period;

                    $display("i = ${i}, test_size = ${test_size}");
                    i = i + 8;
//                    if(i >= test_size)
//                    begin
//                        $display("Finished sending test data for test size: ${test_size}");
//                        i = -1;
//                    end
                end
            end

            in_ts_data_element = 64'b0;
            in_ts_data_valid = 1'b0;
            // Now we wait for the results            
            #period;
            // Say that we are ready for the results
            in_ts_results_ready = 1'b1;

            wait(out_ts_results_valid);
        end
        $fclose(fptr); // Close file before finish

        $fclose(f_data); // Close file before finish
        $finish;
    end

endmodule