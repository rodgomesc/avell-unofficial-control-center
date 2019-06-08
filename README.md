#  avell-unofficial-control-center

[![Gitter](https://badges.gitter.im/Unofficial-CC/Lobby.svg)](https://gitter.im/Unofficial-CC/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

This is a driver to control RGB keyboard in Linux Systems based on Avell Control Center.

This project is at an early stage. 
The aim is to implement a Linux userspace driver and control tool for RGB LED keyboard backlight controller **Integrated Technology Express ITE Device(8291)**.
This RGB keyboard controller is used in many gaming laptops around the world.
For a list of reseller-branded devices, see below.



## Compatibility

### Find out about your laptop's keyboard model

```bash
sudo hwinfo --short
```
It should show the ITE Device(8291) in the `keyboard` section:
```bash
keyboard:
                       Integrated Technology Express ITE Device(8291)
  /dev/input/event0    AT Translated Set 2 keyboard
```

### Known compatible devices

ITE Device(8291) is integrated in widely-used Tongfang gaming laptop barebones:

 - Tongfang GK5CN5Z / GK5CN6Z / GK5CQ7Z / GK5CP0Z (Barebone)
 - Avell G1550 FOX & Avell A65 (BR reseller)
 - Schenker XMG Neo 15 (DE reseller), Versions M18 & M19
 - PCSpecialist Recoil II (UK reseller)
 - Scan/3XS LG15 Vengeance Pro (UK reseller)
 - Overpowered 15 and 15+ (US reseller, sold via Walmart)
 - Monster Tulpar T5 (TR reseller)
 - MECHREVO Deep Sea Ghost Z2 (CN reseller)
 - Raionbook GS5 (IT reseller)
 - Illegear Onyx (MY reseller)
 - Hyperbook Pulsar Z15 (PL reseller)
 - SMART7 Kallisto GX15D (PL reseller)
 - Aftershock APEX 15 (SG reseller)
 - Origin-PC EON15-S (USA, Asia, and AU/NZ reseller)
 - Eluktronics Mech 15 G2 (US reseller)
 - HIDevolution EVOC 16GK5 (US reseller)


## Project status

#### Working:
 
 - change color of mechanical rgb-keyboard
 - adjust brightness
 - disable RGB leds
 - set predefined styles


#### To do:
 - implement a GUI interface in Pyqt/Pyside2
 - save/load profiles
 - set custom color in specific key
 - monitor, cpu/gpu load



## Installation

### The easy way, using `pip3`

Install via pip using sudo or with root user: 

```bash 

sudo pip3 install avell-unofficial-control-center

```

### The manual way, using `git`

 - Clone the repository (`git clone https://github.com/rodgomesc/avell-unofficial-control-center.git`), or update with `git pull` if cloned previously.
 - Build an installable package: `python3 setup.py build`
 - Install the package: `sudo python3 setup.py install`



## Usage

### Plain colors

Colors available are: `red`, `green`, `blue`, `teal`, `pink`, `yellow`, `orange` and `white`.<br>
Brightness options are: `1`,`2`,`3` and `4`.<br>

To set `green` color in all keys with max brightness:

```bash 
aucc -c green -b 4
```

If no brightness parameter `-b` is provided, max brightness `4` is applied.

### Alternating colors

To set alternating row colors:

```bash
aucc -H pink teal -b 4
```

Use `-H` for horizontal rows of alternating colors.
Use `-V` for vertical columns of alternating colors.

### Apply pre-defined styles

To set keyboard predefined custom styles:

```bash 
aucc -s style
```

Styles available are `aurora`, `marquee`, `raindrop`, `reactive` and `rainbow`.

### Disable all keyboard backlight

To disable all keys:
```bash 
aucc -d
```



## Contributions

Contributions of any kind are welcome. Please follow [pep-8](https://www.python.org/dev/peps/pep-0008/) coding style guides.

## Donate :coffee: :hearts:

This is a project I develop in my free time.  If you use `avell-unofficial-control-center` or simply like the project and want to help please consider [donating a coffee](https://www.buymeacoffee.com/KCZRP52U7). 


