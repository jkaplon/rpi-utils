# rpi-utils
Raspberry Pi utility scripts (for IoT and Home Assistant)

This repo is for config and scripts running on the Rasperry Pis that make up my Home Assistant setup.
At the moment, that consists of:
-  Raspbery Pi 2 running Pi-Hole, Home Assistant docker container, Mosquitto container
    - Raspberry Pi OS Lite (32-bit)
-  Rasberry Pi 3 in garage controlling two garage doors
    - Raspberry Pi OS Lite (64-bit)

While slowly building this setup, it was never a good time to pause for proper backups to get the hacky python scripts into version control, but then the RPi-2 acting as my Home Assistant server and MQTT broker when down :(. All the hardware is still working **maybe** it was due to a loose network cable...we'll never know since I was too quick to nuke/pave the SD card with a new RPi OS image.

So here's my "too-little-too-late" backup strategy.
I'm hoping to keep all scripts in a single directory and to come up with solid naming-convention to keep track of the each script's purpose or whether it's specific to particular RPi-hardware (model 2 vs model 3).

I'll also try to add setup commands into this README.

rpi2 steup:
```
# Ponder if I need to find a docker alternative...
curl -fsSL https://get.docker.com -o get-docker.sh
# Stop pondering alternatives and just get going.
sudo sh get-docker.sh
sudo usermod -aG docker pi
# Log out and log in again after you get annoyed by 'sudo docker'

# Pull RPi2 HASS image from GitHub container registry, kinda nice to have a Docker Hub alternative.
docker pull ghcr.io/home-assistant/raspberrypi2-homeassistant:2021.7.1
docker run --init -d --name hass --restart=unless-stopped -v /etc/localtime:/etc/localtime:ro -v /home/pi/hass:/config --net=host homeassistant/raspberrypi2-homeassistant:2021.7.1
# Will need to update version number labels on these 2 cmds in future.

# Mosquitto and MQTT (careful w/'mosquitto-clients on RPi2, it's an older version that doesn't support '-L' flag):
sudo apt install mosquitto-clients
mkdir ~/mosquitto && cd mosquitto
vi mosquitto.conf
# Not running mosquitto w/username or pw, so might be ok to check into this repo...
# NOTE: must add 'listener 1883' to get mosquitto out of local only mode (or be prepared for frustration).
docker run -d -p 1883:1883 -p 9001:9001 --name mosquitto --restart=unless-stopped -v /home/jody/mosquitto:/mosquitto/config -v /home/jody/mosquitto:/mosquitto/data -v /home/jody/mosquitto:/mosquitto/log eclipse-mosquitto:2

```

rpi3 setup:
```
# Add ssh key for simpler git pushes up to GitHub.
ssh-keygen

sudo apt install mosquitto-clients

```
