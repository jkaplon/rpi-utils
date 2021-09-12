#! /bin/sh

# CPU clock never moved from 600MHz, GPU Temp always stayed close to CPU temp, neither useful on rpi2.

#mosquitto_pub -h 192.168.0.97 -p 1883 -m "$(/opt/vc/bin/vcgencmd measure_temp)" -t "/home/rpi2/gputemp"
#mosquitto_pub -h 192.168.0.97 -p 1883 -m "$(/opt/vc/bin/vcgencmd measure_clock arm)" -t "/home/rpi2/cpuclk"
mosquitto_pub -h 192.168.0.97 -p 1883 -m "$(cat /sys/class/thermal/thermal_zone0/temp)" -t "/home/rpi2/cputemp"
