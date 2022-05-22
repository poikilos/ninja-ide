# Samurai-IDE is the Same But More Active Involvement IDE
[![Linux Tests](https://github.com/poikilos/samurai-ide/actions/workflows/linux.yml/badge.svg)](https://github.com/poikilos/samurai-ide/actions/workflows/linux.yml)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](http://makeapullrequest.com)

 [Samurai-IDE](https://github.com/poikilos/samurai-ide) is a cross-platform integrated development environment (IDE) that allows developers to create applications for any purpose making the task of writing software easier and more enjoyable.

<p align="center">
  <img alt="Samurai-IDE logo" src="samurai_ide/gui/qml/img/logo.png?raw=true">
</p>


## Requirements
On any system you want **Samurai-IDE**, you'll need to have this dependencies installed:

- [Python](https://python.org "Python Homepage") 3.7+
- [PyQt5](https://riverbankcomputing.com/software/pyqt/intro) 5.15+


## Cloning and Running
The `PyQt5-sip` package should be upgraded as shown below (as per
<https://github.com/gnuradio/gnuradio/issues/5435#issuecomment-1005152735>)
to avoid an error like "RuntimeError: the sip module implements API
v12.0 to v12.8 but the PyQt5.QtWidgets module requires API v12.9".

You can clone this repo and (After changing `apt` in the command below
to the correct package manager for your distro) simply execute:

```bash
# sudo apt install python3-pyqt5.qtquick
git clone git://github.com/poikilos/samurai-ide.git
cd samurai-ide
python3 -m pip install -r requirements.txt
python3 -m pip install pyqtwebengine PyQt5-sip  --upgrade
python3 samurai-ide.py
```

### Migrating from Ninja-IDE
```
if [ ! -d ~/.config/samurai_ide ]; then
    cp -R ~/.ninja_ide ~/.config/samurai_ide
    mv ~/.config/samurai_ide/ninja_settings.ini ~/.config/samurai_ide/samurai_settings.ini
else
    echo "Error: ~/.config/samurai_ide already exists. After ensuring you preserve crucial data from there, delete or rename it."
fi
```

## Samurai-IDE contacts
- [github.com/poikilos](https://github.com/poikilos)
- Twitter: [@poikilos_](https://twitter.com/poikilos_)
- [poikilos.org](https://poikilos.org)


## Feedback
- File a bug on the [Issues](https://github.com/poikilos/samurai-ide/issues) page.
- [Tweet](https://twitter/poikilos_) us.


## License
-   **GPLv3+** *(GPLv3 or any other later version published by FSF at your option)*

