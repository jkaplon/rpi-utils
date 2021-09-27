# rpi-utils
Raspberry Pi utility scripts (for IoT and Home Assistant)

This repo is for config and scripts running on the Rasperry Pis that make up my Home Assistant setup.
At the moment, that consists of:
-  Raspbery Pi 2 running Pi-Hole, Home Assistant docker container, Mosquitto container
    - Raspberry Pi OS Lite (32-bit)
-  Rasberry Pi 3 in garage controlling two garage doors
    - Raspberry Pi OS Lite (64-bit)

While slowly building this setup, it was never a good time to pause for proper backups or to get the hacky python scripts into version control, but then the RPi-2 running Home Assistant server and MQTT broker when down :(. All the hardware is still working so **maybe** it was due to a loose network cable...we'll never know since I was too quick to nuke/pave the SD card with a new RPi OS image.
Oh, and the rpi3 lives in a hot Florida garage, so who knows when it will decide to release its magic smoke...

So here's my "too-little-too-late" backup strategy.
I'm hoping to keep all scripts in a single directory and to come up with solid naming-convention to keep track of the each script's purpose or whether it's specific to particular RPi-hardware (model 2 vs model 3).

I'll also try to add setup commands into this README.

### rpi2 steup:
```bash
sudo hostnamectl set-hostname rpi2

# Ponder if I need to find a docker alternative...
curl -fsSL https://get.docker.com -o get-docker.sh
# Stop pondering alternatives and just get going.
sudo sh get-docker.sh
sudo usermod -aG docker pi
# Log out and log in again after you get annoyed by 'sudo docker'

# Start w/pi-hole container before moving to Home-Assistant setup.
docker run -d \
    --name pihole \
    -p 53:53/tcp -p 53:53/udp \
    -p 80:80 \
    -e TZ="America/New York" \
    -v /home/pi/pihole/etc-pihole/:/etc/pihole/ \
    -v /home/pi/pihole/etc-dnsmasq.d/:/etc/dnsmasq.d/ \
    --dns=127.0.0.1 --dns=1.1.1.1 \
    --restart=unless-stopped \
    --hostname pi.hole \
    -e VIRTUAL_HOST="pi.hole" \
    -e PROXY_LOCATION="pi.hole" \
    -e ServerIP="192.168.0.97" \
    pihole/pihole:2021.09

# Pull RPi2 HASS image from GitHub container registry, kinda nice to have a Docker Hub alternative.
docker pull ghcr.io/home-assistant/raspberrypi2-homeassistant:2021.9.6
docker run --init -d --name hass --privileged \
    --restart=unless-stopped \
    -v /etc/localtime:/etc/localtime:ro \
    -v /home/pi/hass:/config \
    --net=host \
    homeassistant/raspberrypi2-homeassistant:2021.9.6
# Will need to update version number labels on these 2 docker cmds in future.
# Any HASS version over 7.0 needs a 'trusted_proxy' in http block in configuration.yaml:
#     https://www.home-assistant.io/integrations/http#use_x_forwarded_for
# Another fun snag when upgrading to 7.0 was the need for the '--privileged' flag on RPi OS
#    (1st time I've needed that flag, but I guess I'm already trusing HASS image).

sudo apt install git
ssh-keygen
# Then add new ssh key in GitHub settings and 'git clone' this repo.
git clone git@github.com:jkaplon/rpi-utils.git
# Add new line to run simple hw-monitoring every minute, '* * * * * sh /home/pi/rpi-utils/rpi2-hw-info-to-mqtt.sh'
crontab -e

# Mosquitto and MQTT (careful w/'mosquitto-clients' on RPi2, it's an older version that doesn't support '-L' flag):
sudo apt install mosquitto-clients
mkdir ~/mosquitto && cp mosquitto.conf ~/mosquitto
# NOTE: must add 'listener 1883' and 'allow_anonymous true' lines to mosquitto.conf
#     to get mosquitto out of local-only mode and bypass username/pw (or be prepared for frustration).
docker run -d -p 1883:1883 -p 9001:9001 \
    --name mosquitto \
    --restart=unless-stopped \
    -v /home/pi/mosquitto:/mosquitto/config \
    -v /home/pi/mosquitto:/mosquitto/data \
    -v /home/pi/mosquitto:/mosquitto/log \
    eclipse-mosquitto:2

sudo apt install wireguard
# Errors from wireguard :(, but fixed w/next cmd :)
nohup sudo apt install raspberrypi-kernel-headers &
# Trust me on the 'nohup', it's sloooow to complete on rpi2 (more than an hour),
#     but worth it to get wireguard running!

# These 2 cmds put private key into wg0.conf, but does not save into separate dir/file (one less file to protect):
(umask 077 && printf "[Interface]\nPrivateKey = " | sudo tee /etc/wireguard/wg0.conf > /dev/null)
wg genkey | sudo tee -a /etc/wireguard/wg0.conf | wg pubkey | sudo tee /etc/wireguard/publickey
# Copy public key output by last cmd to add to wireguard server config as a new peer in a minute.

# open wg0.conf, set VPN-IP to 10.0.0.97 (final octet same as LAN),
#     use PersistentKeepalive = 25 again, leave out SaveConfig = true.
sudo vi /etc/wireguard/wg0.conf
sudo wg-quick up wg0
sudo systemctl enable wg-quick@wg0

# On wireguard central server (a Linode VPS in my case):
sudo vim /etc/wireguard/wg0.conf   # Add new peer w/public key material from above.
sudo systemctl restart wg-quick@wg0
sudo wg   # To verify changes
```

### rpi3 setup:
```bash
sudo hostnamectl set-hostname rpi3

# Add ssh key for simpler git pushes up to GitHub.
ssh-keygen
# Then add new ssh key in GitHub settings and 'git clone' this repo.
git clone git@github.com:jkaplon/rpi-utils.git
# Add new line to run simple hw-monitoring every minute,
#     '* * * * * sh /home/pi/rpi-utils/rpi3-hw-info-to-mqtt.sh'
crontab -e

sudo apt install mosquitto-clients

sudo apt install python-pip
sudo pip install paho-mqtt   # it DOES need sudo!

# systemd service setup, create garage.service to run garage monitoring script on boot:
sudo cp garage.service /etc/systemd/system/garage.service
sudo systemctl daemon-reload
sudo systemctl enable garage.service
```
