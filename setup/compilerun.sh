ghdl -a project_io.vhd project_io_tb.vhd
ghdl -e project_io_tb
ghdl -r project_io_tb --wave=signal.ghw
