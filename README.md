#  Unofficial-CC
[![Gitter](https://badges.gitter.im/Unofficial-CC/Lobby.svg)](https://gitter.im/Unofficial-CC/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

This is an Unofficial Control Center for Avell Laptops with Linux System.

This project is in an early stage, the aim is to bring functionality to control Avell laptops hardware since the company does not provide support for Linux systems.
 
#### working: ####
 
 - change color of mechanical rgb-keyboard


#### to-do ####
 - implement a GUI interface in Pyqt/Pyside2
 - save/load profiles
 - set custom color in specific key
 - monitor, cpu/gpu load

#### Supported Devices ####

- all devices equiped with  [2º generation of mechanical keyboards](http://blog.avell.com.br/melhorias-segunda-geracao-de-teclados-mecanicos-avell/)

### Requirements
```bash 
pip install -r requirements.txt
```

### Usage

All commands need `root` permissions (you may use sudo).<br>
Colors available are: `red`, `green`, `blue`, `teal`, `pink`, `yellow`, `orange` and `white`.<br>

To set mono color in all keys;

```bash 
python main.py -c color
```

To disable all keys:
```bash 
python main.py -d
```

To set keyboard predefined custom styles:

```bash 
python main.py -s style
```

Styles available are `aurora`, `marquee`, `raindrop`, `reactive` and `rainbow`



### Contributions

Contributions of any kind are welcome. Please follow [pep-8](https://www.python.org/dev/peps/pep-0008/) coding style guides.

### Donate

This is a project I develop in my free time.  If you use Unnoficial-CC or simply like the project and want to help please consider [donating a coffee](https://www.buymeacoffee.com/KCZRP52U7). 


