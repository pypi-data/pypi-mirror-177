# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rastless',
 'rastless.cli',
 'rastless.commands',
 'rastless.core',
 'rastless.db']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.20.26,<2.0.0',
 'click>=8.0.3,<9.0.0',
 'moto>=2.3.0,<3.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'rasterio>=1.2.10,<2.0.0',
 'rio-cogeo>=3.0.2,<4.0.0',
 'simplejson>=3.17.6,<4.0.0']

entry_points = \
{'console_scripts': ['rastless = rastless.main:cli']}

setup_kwargs = {
    'name': 'rastless-cli',
    'version': '0.3.1',
    'description': 'A cli for managing data and user access for the cloud application rastless',
    'long_description': 'Rastless-CLI\n=================\n\n##### A cli for managing data and user access for the cloud application rastless\n\n## Table of Content\n\n- [Installation](#installation)\n- [Running the CLI](#running-the-cli)\n- [Commands Overview](#commands-overview)\n- [Accomplishing a running system](#accomplishing-a-running-system)\n\n## Installation\n\nRequires: Python >=3.8, <4.0\n\n```bash\n$ pip install rastless-cli\n```\n\nRastLess has to be configured before you can check if everything works. Make sure that your aws account is configured\nand has access to DynamoDb and S3.\n\nYou can check if everything works correctly by running:\n\n```bash\n$ rastless check-aws-connection\n```\n\nIf it is not working, make sure to configure the aws connection by configuring the aws cli. You need an Access ID and a\nSecret ID from aws to configure. Please check\nthe [official instructions](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) for further\nhelp.\n\n##### Developer Installation\n\n```bash\n$ pip install poetry\n$ git clone https://github.com/EomapCompany/rastless-cli\n$ cd rastless-cli\n$ poetry install\n```\n\nRun tests\n\n```bash\ncd tests\npoetry run pytest\n```\n\n## Running the CLI\n\nAfter installation you can run the ClI by using:\n\n```bash\n$ rastless --help\n```\n\nYou can decide if you want to upload data to the production or development environment.\nBy using the "dev" flag you upload it to development, without to production\n\n```bash\n# Example development\n$ rastless --dev list-layers\n\n# Example production\n$ rastless list-layers\n```\n\n## Commands Overview\n\n| Commands             |                                                     |\n|----------------------|-----------------------------------------------------|\n| add-colormap         | Add a SLD file                                      |\n| add-permission       | Add a role to one or multiple layers                |\n| check-aws-connection | Check if cli can connect to aws                     |\n| create-layer         | Create layer                                        |\n| create-timestep      | Create timestep entry and upload layer to S3 bucket |\n| delete-colormap      | Remove a SLD file                                   |\n| delete-layer         | Delete a layer with all timestep entries            |\n| delete-permission    | Delete one or multiple permissions                  |\n| list-layers          | List all layers                                     |\n\n## Accomplishing a running system\n\n#### 1. Check if you have access to the system\n\n```bash\n$ rastless check-aws-connection\n```\n\n#### 2. Create a new layer\n\n- All inputs are strings. You have to take care, that the element exists in the database e.g. the colormap name.\n- Multiple permissions can be set by using multiple -pe flags\n\n```bash\n$ rastless create-layer -cl hypos -pr tur -t Turbidity -cm log75_C2S8_32bit -u FTU -b <rgb uuid> -d "Some description" -r 1 -pe user#marcel -pe role#hypos:full-access\n```\n\nIt will return a new uuid which you need to store, in order to upload timesteps to the particular layer\n\n#### 3. Upload Timesteps for layer\n\n```bash\n$ rastless create-timestep -d 2020-01-01T15:00:00 -s SENT2 -l <layer uuid> -t daily -p deflate\n```\n\n## Breaking changes\n\n### Version 0.3\n\nThe command "create-timestep" changed. Files need to be set as flag instead of normal input\n\n- Now it is possible to set multiple files per timestep by setting multiple file flags -f\n- To override a timestep which already exists you have to set the flag -o, otherwise you will be asked during uploading\n  if you really want to override it\n- To append new files to an existing timestep you have to set the flag -a\n- **Attention:** If you append a file to an existing timestep and the filename already exists, it will be automatically overridden\n  without further action\n\n```shell\n# Before. Filepath without flag\nrastless create-timestep file1.tif -d 2020-01-01T15:00:00 -s Sent2 -layer-id 1234 -t daily -p deflate\n\n# Now: Single file. Flag: -f\nrastless create-timestep -f file1.tif -d 2020-01-01T15:00:00 -s Sent2 -layer-id 1234 -t daily -p deflate\n\n# Now: Multi file. Flag: -f <file1> -f <file1>\nrastless create-timestep -f file1.tif -f file2.tif -d 2020-01-01T15:00:00 -s Sent2 -layer-id 1234 -t daily -p deflate\n\n# Now: Override existing timestep. Flag: -o\nrastless create-timestep -f file1.tif -f file2.tif -d 2020-01-01T15:00:00 -s Sent2 -layer-id 1234 -t daily -p deflate -o\n\n# Now: Append file to existing timestep. Flag: -a\nrastless create-timestep -f file2.tif -d 2020-01-01T15:00:00 -layer-id 1234 -p deflate -a\n```',
    'author': 'Marcel Siegmann',
    'author_email': 'siegmann@eomap.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
