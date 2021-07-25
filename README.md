# Extra info

To use OpenCV in my Raspberry Pi 3B+ https://pypi.org/project/opencv-contrib-python/

Two materials used in particular: FLIR LEPTON BREAKOUT BOARD V2 and FLIR 2.5 THERMAL IMAGE SENSOR 80HX60V

(J2 Pin) -> (Proper name) -> (RPi connector pin) -> (Cable Color)

P8 -> SCL -> GPIO 3 -> WHITE

P10 -> CS -> GPIO 8 -> PURPLE

P12 -> MISO -> GPIO 9 -> BLUE

P5 -> SDA -> GPIO 2 -> GREEN

P7 -> CLK -> GPIO 11 -> YELLOW

P15 -> VSYNC -> GPIO 17 -> ORANGE

(J3 Pin) -> (Proper name) -> (Cable Color)

P1 -> GROUND (PIN 6) -> BLACK

P2 -> VIN 3.3 (PIN 1) -> RED

Important to [increase the SPI buffer size in Raspbian](https://stackoverflow.com/questions/16427996/increase-spi-buffer-size-in-raspbian/16440226).

SOLUTION:

The problem is in the SPI buffer size. The default value is 4096 but 160x120 images from Lepton3 are bigger.

You need to increase the size of the SPI buffer as explain here

Edit /boot/cmdline.txt and add in the end:
spidev.bufsiz= 65535

Then reboot your raspberry and check it worked with:
cat /sys/module/spidev/parameters/bufsiz

Hope it works for you also. Maybe this information should be in the README setup tutorial