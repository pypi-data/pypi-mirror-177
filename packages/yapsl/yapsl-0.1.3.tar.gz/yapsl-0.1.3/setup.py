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
    'version': '0.1.3',
    'description': '',
    'long_description': '# yapsl\n\nyapsl (Yet Another Python Sms Library) allows to send SMS from python by using a local connected modem (e.g. Huawei E220).\nThe library is at the moment in a beta-state and does not yet implement everything. E.g. the message delivery confirmation\nis not yet implemented.\n\nAlso it\'s required that the PIN is already entered (or that no PIN is used at all). If that\'s not the case, the library\nwill raise an exception.\n\n## Usage\n\n```python\nfrom yapsl import SmsType, SmsGateway\n\ngw = SmsGateway(\'/dev/ttyUSB0\', verbose=False) # verbose=True is mostly for debugging purposes:\n                                               # it\'ll show the complete communication with the modem\n                                               # (plus some more logs)\n\nif not gw.is_connected():\n    print("Not connected!")\n    print("Auto select network")\n    gw.auto_select_network()\n    sleep(60)\n\n# send an ordinary SMS\ngw.send(\'0786391538\', \'this is a test message\')\n\n# send a "flash"-SMS (this is usually a popup and by default these SMS are not stored)\ngw.send(\'0786391538\', \'this is a test message\', flash=True)\n\n# send a silent SMS (text wont be shown: this is just some kind of \'ping\')\ngw.send(\'0786391538\', \'this is a test message\', type=SmsType.TYPE_0)\n\n# send a replaceable SMS (note there exist only 7 of these replaceable SMS)\ngw.send(\'0786391538\', \'this is a test message\', type=SmsType.REPLACE_TYPE_1)\n\n# replace the previous sent SMS\ngw.send(\'0786391538\', \'this is NOT a test message\', type=SmsType.REPLACE_TYPE_1)\n\n```\n\n## TODO\n\n- [ ] Check the specs what should happen if a flash-SMS is combined with other SMS\n- [ ] Allow it to get the \'sms-received-confirmations\' in python\n- [ ] Improve the API\n',
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
