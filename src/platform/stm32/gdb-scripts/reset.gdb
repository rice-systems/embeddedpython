target remote | openocd -p -f /usr/local/share/openocd/scripts/interface/stlink-v2.cfg -f /usr/local/share/openocd/scripts/target/stm32f4x_stlink.cfg 
monitor reset halt
monitor shutdown
quit

