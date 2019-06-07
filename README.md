#  avell-unofficial-control-center

[![Gitter](https://badges.gitter.im/Unofficial-CC/Lobby.svg)](https://gitter.im/Unofficial-CC/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

This is a driver to control RGB keyboard in Linux Systems based on Avell Control Center.

This project is in an early stage, the aim is to bring a driver to integrated embedded controller for RGB LED lighting control **ITE Device(8291)** which is used in some custom laptops around the world including avell.
 
#### working: ####
 
 - change color of mechanical rgb-keyboard
 - adjust brightness
 - disable RGB leds
 - set predefined styles


#### to-do ####
 - implement a GUI interface in Pyqt/Pyside2
 - save/load profiles
 - set custom color in specific key
 - monitor, cpu/gpu load


### Installation

Install via pip using sudo or with root user: 

```bash 

sudo pip3 install avell-unofficial-control-center

```

### Usage
Colors available are: `red`, `green`, `blue`, `teal`, `pink`, `yellow`, `orange` and `white`.<br>
Brightness options are: `1`,`2`,`3` and `4`.<br>

To set `green` color in all keys with max brightness;

```bash 
aucc -c green -b 4
```

To disable all keys:
```bash 
aucc -d
```

To set keyboard predefined custom styles:

```bash 
aucc -s style
```

Styles available are `aurora`, `marquee`, `raindrop`, `reactive` and `rainbow`



### Contributions

Contributions of any kind are welcome. Please follow [pep-8](https://www.python.org/dev/peps/pep-0008/) coding style guides.

### Donate

This is a project I develop in my free time.  If you use Unnoficial-CC or simply like the project and want to help please consider [donating a coffee](https://www.buymeacoffee.com/KCZRP52U7). 


