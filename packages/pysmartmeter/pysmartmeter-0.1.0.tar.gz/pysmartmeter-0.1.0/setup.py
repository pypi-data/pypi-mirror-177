# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysmartmeter', 'pysmartmeter.tests', 'pysmartmeter.utilities']

package_data = \
{'': ['*']}

install_requires = \
['bx_py_utils', 'paho-mqtt', 'pyserial', 'rich', 'typer']

entry_points = \
{'console_scripts': ['publish = pysmartmeter.publish:publish',
                     'pysmartmeter = pysmartmeter.main:main']}

setup_kwargs = {
    'name': 'pysmartmeter',
    'version': '0.1.0',
    'description': 'Collect data from Hitchi Smartmeter and expose it via MQTT',
    'long_description': '# pysmartmeter\n\nCollect data from Hitchi Smartmeter (USB Version) and expose it via MQTT.\n\n## quickstart\n\n```bash\n~$ git clone https://github.com/jedie/pysmartmeter.git\n~$ cd pysmartmeter\n~/pysmartmeter$ make install-poetry\n~/pysmartmeter$ make install\n~/pysmartmeter$ ./cli.sh --help\n+ exec .venv/bin/python -m pysmartmeter --help\nPySmartMeter v0.1.0\n\n Usage: python -m pysmartmeter [OPTIONS] COMMAND [ARGS]...\n\n╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────╮\n│ --install-completion        [bash|zsh|fish|powershell|pwsh]  Install completion for the specified │\n│                                                              shell.                               │\n│                                                              [default: None]                      │\n│ --show-completion           [bash|zsh|fish|powershell|pwsh]  Show completion for the specified    │\n│                                                              shell, to copy it or customize the   │\n│                                                              installation.                        │\n│                                                              [default: None]                      │\n│ --help                                                       Show this message and exit.          │\n╰───────────────────────────────────────────────────────────────────────────────────────────────────╯\n╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────╮\n│ check-code-style                                                                                  │\n│ coverage                     Run and show coverage.                                               │\n│ debug-settings               Display (anonymized) MQTT server username and password               │\n│ debug-systemd-service        Just print the systemd service file content                          │\n│ detect-serial                Just print the detected serial port instance                         │\n│ dump                         Just dump serial output                                              │\n│ fix-code-style               Fix code style via darker                                            │\n│ mypy                         Run Mypy (configured in pyproject.toml)                              │\n│ publish-loop                 Publish current data via MQTT (endless loop)                         │\n│ setup-systemd-service        Setup PySmartMeter systemd services and starts it.                   │\n│ store-settings               Store MQTT server settings.                                          │\n│ systemd-status               Call systemd status of PySmartMeter services                         │\n│ systemd-stop                 Stop PySmartMeter systemd services                                   │\n│ test                         Run unittests                                                        │\n╰───────────────────────────────────────────────────────────────────────────────────────────────────╯\n```\n\nTest if you Hitchi Smartmeter with CP2102 USB to UART Bridge Controller works, e.g.:\n```bash\n~/pysmartmeter $ ./cli.sh dump\n```\n\nMaybe you have to setup permissions, e.g.:\n```bash\nsudo chmod +r /dev/ttyUSB0\n```\n\n## publish smartmeter data via MQTT\n\nYou have to store your MQTT settings (host, port, username, password) one time, e.g.:\n```bash\n~/pysmartmeter$ ./cli.sh store-settings\n```\n\nSetup systemd service:\n```bash\n~/pysmartmeter$ sudo ./cli.sh setup-systemd-service\n```\n\n\n# various links\n\n* https://github.com/pyserial/pyserial\n* https://github.com/eclipse/paho.mqtt.python\n* https://github.com/eclipse/mosquitto\n* https://dewiki.de/Lexikon/OBIS-Kennzahlen (de) | https://www.promotic.eu/en/pmdoc/Subsystems/Comm/PmDrivers/IEC62056_OBIS.htm (en)\n',
    'author': 'Jens Diemer',
    'author_email': 'pysmartmeter@jensdiemer.de',
    'maintainer': 'Jens Diemer',
    'maintainer_email': 'pysmartmeter@jensdiemer.de',
    'url': 'https://github.com/jedie/pysmartmeter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0.0',
}


setup(**setup_kwargs)
