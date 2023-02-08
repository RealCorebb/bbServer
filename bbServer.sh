apt install python3-pip
mv /etc/orangepi-release /etc/armbian-release
apt-get install libgpiod2 python3-libgpiod
pip3 install gpiod
apt-get install -y python-smbus python-dev i2c-tools
pip3 install adafruit-blinka
pip3 install adafruit-circuitpython-ssd1306
pip3 install adafruit-circuitpython-neopixel-spi
pip3 install adafruit-circuitpython-led-animation
git clone https://github.com/RealCorebb/bbServer.git bbServer-All
cp -r bbServer-All/Python bbServer
rm -rf bbServer-All
echo 'overlays=i2c1-m2 i2c3-m0 i2c5-m3 spi4-m0-cs1-spidev' >> /boot/orangepiEnv.txt
echo -e '[Unit]\nDescription=frpc\nAfter=network.target\n\n[Service]\nType=simple\nTimeoutStartSec=30\nUser=root\nRestart=on-failure\nRestartSec=5s\nExecStart=python /root/bbServer/demo.py \nExecReload=python /root/bbServer/demo.py\nExecStop=/bin/kill $MAINPID\nLimitNOFILE=1048576\n \n[Install]\nWantedBy=multi-user.target' >> /usr/lib/systemd/system/bbServerDemo.service
systemctl enable bbServerDemo.service