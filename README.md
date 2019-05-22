#  Unofficial-CC
This is a Unofficial Control Center for Avell Laptops with Linux OS

this project is in an early stage, the aims is bring functionality to control the hardware of avell laptops since the company does not provide support for linux
 
#### working: ####
 
 - change color of mechanical rgb-keyboard


#### to-do ####
 - implement a gui interface in Pyqt/Pyside2
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

with `root` user .

```bash 

python main.py -c color

```

colors avaliable are, `red`, `green`, `blue`, `teal` and `pink`

### Contributions

Contributions of any kind are welcome. Please use the [pep-8](https://www.python.org/dev/peps/pep-0008/) code style to be consistent.

### Donate

This is a project I develop in my free time.  If you use Unnoficial-CC or simply like the project and want to help continue the development of it please consider [donate a cofee](https://www.buymeacoffee.com/KCZRP52U7). 


