# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yapsl']

package_data = \
{'': ['*']}

install_requires = \
['alog>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'yapsl',
    'version': '0.1.4',
    'description': '',
    'long_description': '# yapsl\n\nyapsl (Yet Another Python Sms Library) allows to send SMS from python by using a local connected modem (e.g. Huawei E220).\nIt\'s required that the PIN is already entered (or that no PIN is used at all). If that\'s not the case, the library\nwill raise an exception.\n\n## Usage\n\n```python\nfrom yapsl import SmsType, SmsGateway\n\ngw = SmsGateway(\'/dev/ttyUSB0\', verbose=False) # verbose=True is mostly for debugging purposes:\n                                               # it\'ll show the complete communication with the modem\n                                               # (plus some more logs)\n\n# Optional: It\'s possible to check if the modem is connected to a network (this is as well always done when sending an SMS)\nif not gw.is_connected():\n    print("Not connected!")\n    print("Auto select network")\n    gw.auto_select_network()\n    sleep(60)\n\n# send an ordinary SMS\ngw.send(\'0786391538\', \'this is a test message\')\n\n# send a "flash"-SMS (this is usually a popup and by default these SMS are not stored)\ngw.send(\'0786391538\', \'this is a test message\', flash=True)\n\n# send a silent SMS (text wont be shown: this is just some kind of \'ping\')\ngw.send(\'0786391538\', \'this is a test message\', type=SmsType.TYPE_0)\n\n# send a replaceable SMS (note there exist only 7 of these replaceable SMS)\ngw.send(\'0786391538\', \'3...\', type=SmsType.REPLACE_TYPE_1)\n\n# replace the previous sent SMS (a few times)\ngw.send(\'0786391538\', \'2...\', type=SmsType.REPLACE_TYPE_1)\ngw.send(\'0786391538\', \'1...\', type=SmsType.REPLACE_TYPE_1)\ngw.send(\'0786391538\', \'Hey:D\', type=SmsType.REPLACE_TYPE_1)\n\n```\n\n## TODO\n\n- [ ] Allow it to get the \'sms-received-confirmations\' in python\n\n',
    'author': 'Benjamin Bruno Meier',
    'author_email': 'benjamin.meier70@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kutoga/yapsl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
