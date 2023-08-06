# pysmartmeter

Collect data from Hitchi Smartmeter (USB Version) and expose it via MQTT.

## quickstart

```bash
~$ git clone https://github.com/jedie/pysmartmeter.git
~$ cd pysmartmeter
~/pysmartmeter$ make install-poetry
~/pysmartmeter$ make install
~/pysmartmeter$ ./cli.sh --help
+ exec .venv/bin/python -m pysmartmeter --help
PySmartMeter v0.1.0

 Usage: python -m pysmartmeter [OPTIONS] COMMAND [ARGS]...

╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion        [bash|zsh|fish|powershell|pwsh]  Install completion for the specified │
│                                                              shell.                               │
│                                                              [default: None]                      │
│ --show-completion           [bash|zsh|fish|powershell|pwsh]  Show completion for the specified    │
│                                                              shell, to copy it or customize the   │
│                                                              installation.                        │
│                                                              [default: None]                      │
│ --help                                                       Show this message and exit.          │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────╮
│ check-code-style                                                                                  │
│ coverage                     Run and show coverage.                                               │
│ debug-settings               Display (anonymized) MQTT server username and password               │
│ debug-systemd-service        Just print the systemd service file content                          │
│ detect-serial                Just print the detected serial port instance                         │
│ dump                         Just dump serial output                                              │
│ fix-code-style               Fix code style via darker                                            │
│ mypy                         Run Mypy (configured in pyproject.toml)                              │
│ publish-loop                 Publish current data via MQTT (endless loop)                         │
│ setup-systemd-service        Setup PySmartMeter systemd services and starts it.                   │
│ store-settings               Store MQTT server settings.                                          │
│ systemd-status               Call systemd status of PySmartMeter services                         │
│ systemd-stop                 Stop PySmartMeter systemd services                                   │
│ test                         Run unittests                                                        │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Test if you Hitchi Smartmeter with CP2102 USB to UART Bridge Controller works, e.g.:
```bash
~/pysmartmeter $ ./cli.sh dump
```

Maybe you have to setup permissions, e.g.:
```bash
sudo chmod +r /dev/ttyUSB0
```

## publish smartmeter data via MQTT

You have to store your MQTT settings (host, port, username, password) one time, e.g.:
```bash
~/pysmartmeter$ ./cli.sh store-settings
```

Setup systemd service:
```bash
~/pysmartmeter$ sudo ./cli.sh setup-systemd-service
```


# various links

* https://github.com/pyserial/pyserial
* https://github.com/eclipse/paho.mqtt.python
* https://github.com/eclipse/mosquitto
* https://dewiki.de/Lexikon/OBIS-Kennzahlen (de) | https://www.promotic.eu/en/pmdoc/Subsystems/Comm/PmDrivers/IEC62056_OBIS.htm (en)
