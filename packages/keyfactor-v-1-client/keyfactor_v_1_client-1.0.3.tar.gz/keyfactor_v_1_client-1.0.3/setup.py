# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keyfactor_v_1_client',
 'keyfactor_v_1_client.api',
 'keyfactor_v_1_client.api.agent',
 'keyfactor_v_1_client.api.agent_blueprint',
 'keyfactor_v_1_client.api.agent_pool',
 'keyfactor_v_1_client.api.audit_log',
 'keyfactor_v_1_client.api.certificate',
 'keyfactor_v_1_client.api.certificate_authority',
 'keyfactor_v_1_client.api.certificate_collection',
 'keyfactor_v_1_client.api.certificate_store',
 'keyfactor_v_1_client.api.certificate_store_container',
 'keyfactor_v_1_client.api.certificate_store_type',
 'keyfactor_v_1_client.api.csr_generation',
 'keyfactor_v_1_client.api.custom_job_type',
 'keyfactor_v_1_client.api.denied_alert',
 'keyfactor_v_1_client.api.enrollment',
 'keyfactor_v_1_client.api.expiration_alert',
 'keyfactor_v_1_client.api.issued_alert',
 'keyfactor_v_1_client.api.key',
 'keyfactor_v_1_client.api.key_rotation_alert',
 'keyfactor_v_1_client.api.license_',
 'keyfactor_v_1_client.api.logon',
 'keyfactor_v_1_client.api.mac_enrollment',
 'keyfactor_v_1_client.api.metadata_field',
 'keyfactor_v_1_client.api.monitoring',
 'keyfactor_v_1_client.api.orchestrator_job',
 'keyfactor_v_1_client.api.pam_provider',
 'keyfactor_v_1_client.api.pending_alert',
 'keyfactor_v_1_client.api.reports',
 'keyfactor_v_1_client.api.security',
 'keyfactor_v_1_client.api.security_role_permissions',
 'keyfactor_v_1_client.api.security_roles',
 'keyfactor_v_1_client.api.server',
 'keyfactor_v_1_client.api.server_group',
 'keyfactor_v_1_client.api.service_account',
 'keyfactor_v_1_client.api.smtp',
 'keyfactor_v_1_client.api.ssl',
 'keyfactor_v_1_client.api.status',
 'keyfactor_v_1_client.api.template',
 'keyfactor_v_1_client.api.user',
 'keyfactor_v_1_client.api.workflow',
 'keyfactor_v_1_client.api.workflow_definition',
 'keyfactor_v_1_client.api.workflow_instance',
 'keyfactor_v_1_client.models',
 'keyfactor_v_1_client.wrappers']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.3.0',
 'cryptography',
 'httpx>=0.15.4,<0.24.0',
 'python-dateutil>=2.8.0,<3.0.0']

setup_kwargs = {
    'name': 'keyfactor-v-1-client',
    'version': '1.0.3',
    'description': 'A client library for accessing Keyfactor Command-v1',
    'long_description': '# keyfactor-v-1-client\n\nA client library for accessing Keyfactor-v1\n\n## Install\n\n### Using pip\n```bash\npip install keyfactor-v-1-client\n```\n\n### From source\n```bash\ngit clone https://github.com/Keyfactor/keyfactor-python-client-sdk.git\ncd keyfactor-python-client-sdk/kfclient\npoetry install \n# Alternatively\npython -m pip install .\n```\n## Config\n\n### Using Environment Variables\n\n```bash\nexport KEYFACTOR_HOSTNAME=<hostname> # e.g. https://keyfactor.example.com\nexport KEYFACTOR_USERNAME=<username> # e.g. admin\nexport KEYFACTOR_PASSWORD=<password> # e.g. password\nexport KEYFACTOR_DOMAIN=<domain>     # e.g. example.com\n```\n\n### Using a Config File\n\n```bash\nexport KEYFACTOR_CONFIG=<path to config file> # e.g. /etc/keyfactor/config.json. Defaults to cwd "environment.json"\n```\n\nSample Config:\n\n```json\n{\n  "host": "<hostname>",\n  "username": "<username>",\n  "password": "<password>",\n  "domain": "<domain>"\n}\n```\n\n## Usage\n\nFirst, create a client:\n\n```python\nfrom keyfactor_v_1_client import Client\n\nclient = Client(base_url="https://api.example.com")\n```\n\nIf the endpoints you\'re going to hit require authentication, use `AuthenticatedClient` instead:\n\n```python\nfrom keyfactor_v_1_client import AuthenticatedClient\n\nclient = AuthenticatedClient(base_url="https://api.example.com", token="SuperSecretToken")\n```\n\nNow call your endpoint and use your models:\n\n```python\nfrom keyfactor_v_1_client.models import MyDataModel\nfrom keyfactor_v_1_client.api.my_tag import get_my_data_model\nfrom keyfactor_v_1_client.types import Response\n\nmy_data: MyDataModel = get_my_data_model.sync(client=client)\n# or if you need more info (e.g. status_code)\nresponse: Response[MyDataModel] = get_my_data_model.sync_detailed(client=client)\n```\n\nOr do the same thing with an async version:\n\n```python\nfrom keyfactor_v_1_client.models import MyDataModel\nfrom keyfactor_v_1_client.api.my_tag import get_my_data_model\nfrom keyfactor_v_1_client.types import Response\n\nmy_data: MyDataModel = await get_my_data_model.asyncio(client=client)\nresponse: Response[MyDataModel] = await get_my_data_model.asyncio_detailed(client=client)\n```\n\nBy default, when you\'re calling an HTTPS API it will attempt to verify that SSL is working correctly. Using certificate\nverification is highly recommended most of the time, but sometimes you may need to authenticate to a server (especially\nan internal server) using a custom certificate bundle.\n\n```python\nclient = AuthenticatedClient(\n    base_url="https://internal_api.example.com",\n    token="SuperSecretToken",\n    verify_ssl="/path/to/certificate_bundle.pem",\n)\n```\n\nYou can also disable certificate validation altogether, but beware that **this is a security risk**.\n\n```python\nclient = AuthenticatedClient(\n    base_url="https://internal_api.example.com",\n    token="SuperSecretToken",\n    verify_ssl=False\n)\n```\n\nThings to know:\n\n1. Every path/method combo becomes a Python module with four functions:\n    1. `sync`: Blocking request that returns parsed data (if successful) or `None`\n    1. `sync_detailed`: Blocking request that always returns a `Request`, optionally with `parsed` set if the request\n       was successful.\n    1. `asyncio`: Like `sync` but async instead of blocking\n    1. `asyncio_detailed`: Like `sync_detailed` but async instead of blocking\n\n1. All path/query params, and bodies become method arguments.\n1. If your endpoint had any tags on it, the first tag will be used as a module name for the function (my_tag above)\n1. Any endpoint which did not have a tag will be in `keyfactor_v_1_client.api.default`\n\n## Building / publishing this Client\n\nThis project uses [Poetry](https://python-poetry.org/) to manage dependencies and packaging. Here are the basics:\n\n1. Update the metadata in pyproject.toml (e.g. authors, version)\n1. If you\'re using a private repository, configure it with Poetry\n    1. `poetry config repositories.<your-repository-name> <url-to-your-repository>`\n    1. `poetry config http-basic.<your-repository-name> <username> <password>`\n1. Publish the client with `poetry publish --build -r <your-repository-name>` or, if for public PyPI,\n   just `poetry publish --build`\n\nIf you want to install this client into another project without publishing it (e.g. for development) then:\n\n1. If that project **is using Poetry**, you can simply do `poetry add <path-to-this-client>` from that project\n1. If that project is not using Poetry:\n    1. Build a wheel with `poetry build -f wheel`\n    1. Install that wheel from the other project `pip install <path-to-wheel>`\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Keyfactor/keyfactor-python-client-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
