proc log_temp {path} {
	#open_hw_manager
	#connect_hw_server -url localhost:3121 -quiet
	#current_hw_target [get_hw_targets *]
	#open_hw_target
	current_hw_device [lindex [get_hw_devices] 0]
	refresh_hw_device [lindex [get_hw_devices] 0]	-quiet
	set temp [get_property TEMPERATURE [lindex [get_hw_sysmons] 0]]

	#set path "C:/Users/t26607bb/Desktop/temp.csv"
	set file [open $path w+]
	puts $file "Temperature,current_time"
	close $file
	set i 0
	set t1 [clock seconds]
	while {$temp > 0} {
		set file [open $path a+]
		refresh_hw_device [lindex [get_hw_devices] 0] -quiet
		set temp [get_property TEMPERATURE [lindex [get_hw_sysmons] 0]]
		set i [expr $i + 1]
		set systemTime [clock seconds]
		#puts "$i- $temp"
		puts $file "$temp,[clock format $systemTime -format %H:%M:%S]"
		#set t [clock seconds]
		#puts $file "$temp,[expr {$t - $t1}]"
		after 1000
		close $file
	}
}

proc program {bit_file} {
	open_hw_manager
	connect_hw_server -url localhost:3121
	current_hw_target [get_hw_targets *]
	open_hw_target
	# Program and Refresh the device
	current_hw_device [lindex [get_hw_devices] 0]
	refresh_hw_device -update_hw_probes false [lindex [get_hw_devices] 0]
	set_property PROGRAM.FILE $bit_file [lindex [get_hw_devices] 0]
	#set_property PROBES.FILE {C:/design.ltx} [lindex [get_hw_devices] 0]
	set_param xicom.use_bitstream_version_check false
	program_hw_devices [lindex [get_hw_devices] 0]
	refresh_hw_device [lindex [get_hw_devices] 0]
}

program [lindex $argv 0]
log_temp [lindex $argv 1]
