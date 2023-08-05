# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['armorblox', 'armorblox.api']

package_data = \
{'': ['*']}

install_requires = \
['cached-property>=1.5.2,<2.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'armorblox-sdk',
    'version': '0.1.3',
    'description': 'Armorblox SDK for Python',
    'long_description': '<img src="https://assets.armorblox.com/f/52352/775x159/8fa6246e47/logo_color.svg" width=387 alt="Armorblox logo">\n\n# Armorblox Python SDK (Alpha)\n\n[![PyPI version](https://badge.fury.io/py/armorblox-sdk.svg)](https://badge.fury.io/py/armorblox-sdk)\n[![Apache-2 License](https://img.shields.io/badge/license-Apache2-blueviolet)](https://www.apache.org/licenses/LICENSE-2.0)\n\nThis is an alpha version of the SDK with limited documentation and no support.\n\n## Requirements\n\nPython 3.5+\n\n## Installation\n\n```\npip install armorblox-sdk\n```\n\n## Usage\n\n```\nfrom armorblox import client\n\n# Create an API client for your tenant\nc = client.Client(api_key=\'your-api-key-here\', instance_name=\'yourtenantname\')\n\n# Fetch information about an incident\'s analysis data\nincident_analysis = c.incidents.analysis(78143)\n\n# Fetch information about an incident\'s sender data\nincident_senders = c.incidents.senders(78143)\n\n# Fetch information about an object associated with an incident (usually mail). \n# Get the object ID from Get Incident by Id\'s response, under .events[].object_id\nincident_object = c.incidents.mail(\'d72c07bc789c30cb4d63d78ee2861f94add695f9c812e30cfb081b20d3e7e5e7\')\n\n# Updates the action to be taken for an incident\'s objects\nupdate_details = c.incidents.update(78143, body = {\n                  "policyActionType": "DELETE",\n                  "addSenderToException": False,\n                  "actionProfileId": ""\n                })\n\n\n# Fetch a list of threats\nthreat_incidents, next_page_token, total_incident_count = c.threats.list()\n\n# Fetch a specific threat\nincident = c.threats.get(44006)\n\n\n# Fetch a list of abuse incidents\nabuse_incidents, next_page_token, total_incident_count = c.abuse_incidents.list()\n\n# Fetch a specific abuse incident\nabuse_incident = c.abuse_incidents.get(44200)\n\n\n# Fetch a list of DLP incidents\ndlp_incidents, next_page_token, total_incident_count = c.dlp_incidents.list()\n\n# Fetch a specific DLP incident\ndlp_incident = c.dlp_incidents.get(44010)\n\n\n# Example to fetch all threats using next_page_token\nc = client.Client(api_key=\'your-api-key-here\', instance_name=\'yourtenantname\')\nnext_page_token = None\nincidents = []\nwhile True:\n    threats, next_page_token, total_incident_count = client.threats.list(page_token=next_page_token)\n    incidents.extend(threats)\n    if not next_page_token:\n        break\n```\n\n## Contributing\n\n* Install [Poetry](https://python-poetry.org)\n* Clone the SDK repo & `cd` into it\n```\ngit clone https://github.com/armorblox/armorblox-python-sdk\ncd armorblox-python-sdk\n```\n* Run `poetry install` to install the dependencies\n* Run `tox` to run the tests\n\n## Publishing\n\n#### TestPyPI\n\nOne-time setup\n```\npoetry config repositories.test-pypi https://test.pypi.org/legacy/\npoetry config pypi-token.test-pypi <your-TestPyPI-token>\n```\n\nPublishing\n```\npoetry publish --build -r test-pypi\n```\n\nUse\n```\npip install --index-url https://test.pypi.org/simple/ --no-deps armorblox-sdk\n```\nto make sure the installation works correctly.\n\n#### PyPI\n\nOne-time setup\n```\npoetry config pypi-token.pypi <your-PyPI-token>\n```\n\nPublishing\n```\npoetry publish --build\n```\n',
    'author': 'Rajat Upadhyaya',
    'author_email': '45485+urajat@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/armorblox/armorblox-python-sdk',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
