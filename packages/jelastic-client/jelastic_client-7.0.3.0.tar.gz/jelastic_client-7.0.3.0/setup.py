# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jelastic_client', 'jelastic_client.core']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json==0.5.7', 'httpx[http2]>=0.18', 'requests==2.28.1']

setup_kwargs = {
    'name': 'jelastic-client',
    'version': '7.0.3.0',
    'description': 'A client library for Jelastic',
    'long_description': '[[![Build Status](https://jelasticozor-teamcity.sh1.hidora.com/app/rest/builds/buildType:(id:SharedLibraries_JelasticClient_Integration)/statusIcon)](https://jelasticozor-teamcity.sh1.hidora.com/viewType.html?buildTypeId=SharedLibraries_JelasticClient_Integration&guest=1)\n\n\n# jelastic-client\n\nA Jelastic API python library.\n\n# Installation\n\n```bash\npip3 install jelastic-client\n```\n\n# Usage\n\nAt the root of this repository, you can run\n\n```python\nimport jelastic_client\n\napi_url = "https://[hoster-api-host]/1.0/"\napi_token = "your-private-access-token"\n\nfactory = jelastic_client.JelasticClientFactory(api_url, api_token)\njps_client = factory.create_jps_client()\nenv_name = "my-jelastic-client-test"\njps_client.install_from_file("./test/data/valid_manifest.jps", env_name)\ncontrol_client = factory.create_control_client()\nenv_info = control_client.get_env_info(env_name)\nassert env_info.is_running() is True\n```\n',
    'author': 'softozor',
    'author_email': 'softozor@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
