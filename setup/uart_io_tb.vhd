library ieee;
use ieee.std_logic_1164.all;

entity uart_io_tb is
end entity uart_io_tb;

architecture tb of uart_io_tb is
    signal clk_s : std_logic;
    signal reset_s : std_logic;
    signal input_enable_s : std_logic;
    signal output_enable_s : std_logic;
    signal input_data_s : std_logic_vector (7 downto 0);
    signal output_data_s : std_logic_vector (7 downto 0);
    signal input_empty_s : std_logic;
    signal input_empty_next_s : std_logic;
    signal output_full_s : std_logic;
    signal output_full_next_s : std_logic;
    -- kontrolni signali??

    signal tx_dv_s : std_logic;
    signal tx_byte_s : std_logic_vector (7 downto 0);
    signal tx_done_s : std_logic;
    signal tx_serial_s : std_logic;
    signal tx_active_s : std_logic;

    signal rx_serial_s : std_logic;
    signal rx_dv_s : std_logic;
    signal rx_byte_s : std_logic_vector (7 downto 0);


begin

    uut : entity work.uart_io 
    port map (
        clk => clk_s,
        reset => reset_s,
        rx => tx_serial_s,
        tx => rx_serial_s,
        input_enable => input_enable_s,
        output_enable => output_enable_s,
        input_data => input_data_s,
        output_data => output_data_s,
        input_empty => input_empty_s,
        input_empty_next => input_empty_next_s,
        output_full => output_full_s,
        output_full_next => output_full_next_s
    );

    u_tx : entity work.uart_tx 
    port map (
        i_Clk => clk_s,
        i_TX_DV => tx_dv_s,
        i_TX_Byte => tx_byte_s,
        o_TX_Active => tx_active_s,
        o_TX_Serial => tx_serial_s,
        o_TX_Done => tx_done_s
    );

    u_rx : entity work.uart_rx 
    port map (
        i_Clk => clk_s,
        i_RX_Serial => rx_serial_s,
        o_RX_DV => rx_dv_s,
        o_RX_Byte => rx_byte_s
    );


    clock_gen : process begin
        clk_s <= '0';
        wait for 1 us;
        clk_s <= '1';
        wait for 1 us;
    end process clock_gen;


    stimulus : process begin
        tx_byte_s <= "10100101";
        tx_dv_s <= '1';
        wait until rising_edge(tx_done_s);
        input_enable_s <= '1';
        wait for 20 ns;
        input_enable_s <= '0';
        output_enable_s <= '1';
        output_data_s <= "00111100";
        wait on rx_serial_s;
        wait for 20 ns; 
    end process stimulus;

end architecture tb;