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
* `logging.conf` (Rename `logging.conf.orig` to `logging.conf`)
* `siren1.mp3`

Top copy files, use `scp <file> pi@<ip>:~` where `<file>` is the fine name and `<ip>` is the IP address of your Pi. Here's an example:

> Note: The default password for your Raspberry Pi is `raspberry`.

```bash
scp alarm.py pi@10.27.57.178:~
scp key_file.txt pi@10.27.57.178:~
scp logging.conf pi@10.27.57.178:~
scp siren1.mp3 pi@10.27.57.178:~
```

### Install required Python modules

```bash
pip install Flask Flask-API flask-cors PyYAML
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

  
