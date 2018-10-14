---
title: "Pi-Alarm Software Installation"
draft: false
---

## Setup the Operating System

Start by installing the [NOOBS](https://www.raspberrypi.org/help/noobs-setup/2) operating system. Once installed, connect a monitor, keyboard, mouse, and power to Pi. Power on the Pi and it should boot up. Connect to your local network via WiFi or ethernet cable.

## Install the Pi-Alarm Software

Find IP address of your Pi:

```bash
hostname -I
```

Use SCP or Filezilla to transfer te following files to your Raspberry Pi:

* `alarm.py`
* `key_file.txt` (Rename `key_file.txt.orig` to `key_file.txt`)
* `logging.conf.yaml` (Rename `logging.conf.yaml.orig` to `logging.conf.yaml`)
* `siren1.mp3`

To copy files, use `scp <file> pi@<ip>:~` where `<file>` is the fine name and `<ip>` is the IP address of your Pi. Here's an example:

> Note: The default password for your Raspberry Pi is `raspberry`.

```bash
scp alarm.py pi@<ip>:~
scp key_file.txt pi@<ip>:~
scp logging.conf pi@<ip>:~
scp siren1.mp3 pi@1<ip>:~
```

### Install required Python modules

```bash
pip install Flask Flask-API Flask-Cors PyYAML
```

## Installation Complete

Your software installation is ready to be used! Check out the [usage instructions](usage-instructions.md) to learn how to use the Pi Alarm.

## Unit testing

To run the unit tests:

```bash
python -m unittest
```

## Code coverage

Code coverage of the unit tests requies the [coverage](https://github.com/nedbat/coveragepy) module

```bash
pip install coverage
```

To run unit test code coverage:

```bash
coverage run -m unittest
```

To view the report in text format:

```bash
coverage report
```

To view the report in HTML format:

```bash
coverage html
``` 
> HTML report is in htmlcov directory

  
