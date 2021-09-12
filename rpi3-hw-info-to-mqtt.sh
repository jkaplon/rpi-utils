#! /bin/sh

# CPU clock never moved from 600MHz, GPU Temp always stayed close to CPU temp...on rpi2.
# try them all again for rpi3 (i want to get an idea if heatsinks work.
# get rid of GPU Temp on rpi3, not different enough from CPU temp to be useful
#mosquitto_pub -h 192.168.0.97 -p 1883 -m "$(/opt/vc/bin/vcgencmd measure_temp)" -t "/home/rpi3/gputemp"
mosquitto_pub -h 192.168.0.97 -p 1883 -m "$(/opt/vc/bin/vcgencmd measure_clock arm)" -t "/home/rpi3/cpuclk"
mosquitto_pub -h 192.168.0.97 -p 1883 -m "$(cat /sys/class/thermal/thermal_zone0/temp)" -t "/home/rpi3/cputemp"
