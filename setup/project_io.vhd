LIBRARY ieee;
USE ieee.std_logic_1164.ALL;

ENTITY project_io IS
    PORT (
        clk : IN STD_LOGIC;
        rst : IN STD_LOGIC;
        enable : IN STD_LOGIC;
        done : OUT STD_LOGIC;
        in_read_enable : OUT STD_LOGIC;
        in_index : OUT INTEGER;
        in_data : IN STD_LOGIC_VECTOR (7 DOWNTO 0);
        out_write_enable : OUT STD_LOGIC;
        out_index : OUT INTEGER;
        out_data : OUT STD_LOGIC_VECTOR (7 DOWNTO 0);
        in_buff_size : OUT INTEGER := 1;
        out_buff_size : OUT INTEGER := 1
    );
END ENTITY project_io;

ARCHITECTURE behavioural OF project_io IS
    SIGNAL temp_data : STD_LOGIC_VECTOR (7 DOWNTO 0);
    SIGNAL done_s : STD_LOGIC := '0';
BEGIN
    PROCESS (clk, rst)
    BEGIN
        IF rst = '1' THEN
            in_read_enable <= '0';
            out_write_enable <= '0';
            done <= '0';
        ELSIF rising_edge(clk) THEN
            IF enable = '1' AND done_s = '0' THEN
                in_read_enable <= '1';
                out_write_enable <= '1';
                in_index <= 0;
                out_index <= 0;
                temp_data <= in_data;
                out_data <= temp_data;
                done_s <= '1';
                done <= '0';
            ELSIF done_s = '1' THEN
                done_s <= '0';
                done <= '1';
            ELSE
            END IF;
        END IF;
    END PROCESS;

END ARCHITECTURE behavioural;