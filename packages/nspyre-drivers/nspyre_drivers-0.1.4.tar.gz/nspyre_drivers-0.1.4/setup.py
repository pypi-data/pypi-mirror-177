# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['drivers',
 'drivers.agiltron',
 'drivers.agiltron.ffsw',
 'drivers.arduino.arduino_gpio',
 'drivers.beaglebone',
 'drivers.beaglebone.beaglebone_gpio',
 'drivers.beaglebone.beaglebone_gpio.beaglebone_server',
 'drivers.dli_pdu',
 'drivers.dlnsec',
 'drivers.luminox',
 'drivers.oceanoptics',
 'drivers.oceanoptics.hr2000es',
 'drivers.rigol.dp832',
 'drivers.rohde_schwarz.hmp4040',
 'drivers.thorlabs',
 'drivers.thorlabs.cld1010',
 'drivers.thorlabs.fw102c',
 'drivers.thorlabs.pm100d',
 'drivers.ximea',
 'drivers.zaber']

package_data = \
{'': ['*'], 'drivers.arduino.arduino_gpio': ['pin_server/*']}

install_requires = \
['pyserial', 'pyusb', 'pyvisa', 'pyvisa-py']

extras_require = \
{'beaglebone': ['requests'],
 'dli-pdu': ['dlipower'],
 'oceanoptics': ['seabreeze'],
 'ximea': ['ximea-py', 'numpy'],
 'zaber': ['zaber-motion']}

setup_kwargs = {
    'name': 'nspyre-drivers',
    'version': '0.1.4',
    'description': 'A set of Python drivers for lab instrumentation.',
    'long_description': '# Drivers\nThis is a set of Python drivers for lab instrumentation. These drivers are \nassociated with [nspyre](https://nspyre.readthedocs.io/en/latest/), but are \nalso suitable for general usage. Unless otherwise specified, drivers are \nprovided under the terms of the MIT license.\n\n## Installation\n\n```bash\npip install nspyre-drivers\n```\n\nCertain drivers require extra dependencies. Those dependencies can be installed \nby specifying a tag during the install. E.g. to install the DLI pdu driver \ndependencies, use:\n\n```bash\npip install nspyre-drivers[dli_pdu]\n```\n\nA full listing of the tags is below.\n\n```\nbeaglebone\ndli_pdu\noceanoptics\nximea\nzaber\n```\n\nFor some USB drivers on Linux, you need to grant user access to the drivers in \norder for VISA to detect them:\nYou should find the udev rules file in the same folder as the driver, then, e.g.:\n\n```bash\nsudo cp src/drivers/thorlabs/cld1010/99-thorlabs-cld1010.rules /etc/udev/rules.d/\n````\n\nCreate a user group for the usb device access:\n\n```bash\nsudo groupadd usbtmc\n```\n\nAdd any relevant users to the group:\n\n```bash\nusermod -aG usbtmc <myuser>\n```\n\nReboot for the changes to take effect.\n\n## Other Drivers\n\nIn order to minimize reinventing the wheel, below is a list of other sources of \npython instrument drivers. Please contribute if you find other useful sources!\n\n[pycobolt](https://github.com/cobolt-lasers/pycobolt)\n\n## Contributing\n\nIf you want to contribute driver code, please submit it as a \n[pull request](https://nspyre.readthedocs.io/en/latest/contributing.html#forking-pull-requests). This project uses \n[poetry](https://python-poetry.org/). If your driver requires specific \ndependencies beyond those currently in use in the project, you should include \nthem in the pyproject.toml file as extras. See the poetry documentation for \nspecifics on how to declare these dependencies.\n',
    'author': 'Jacob Feder',
    'author_email': 'jacobsfeder@gmail.com',
    'maintainer': 'Jacob Feder',
    'maintainer_email': 'jacobsfeder@gmail.com',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
