add_file -type cst tang_nano.cst
add_file -type netlist impl/synth/blinky.vg
set_device -name GW1N-1 GW1N-LV1QN48C6/I5
set_option -gen_posp 1
set_option -show_all_warn 1

# TODO: The following gpios may be a bit dangerous to enable, depending on the board used.

#set_option -use_jtag_as_gpio 1
set_option -use_sspi_as_gpio 1
set_option -use_mspi_as_gpio 1
#set_option -use_ready_as_gpio 1
#set_option -use_done_as_gpio 1
#set_option -use_reconfign_as_gpio 1
#set_option -use_mode_as_gpio 1

run all