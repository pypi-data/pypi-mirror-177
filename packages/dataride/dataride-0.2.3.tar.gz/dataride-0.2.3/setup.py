# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dataride',
 'dataride.application',
 'dataride.assets',
 'dataride.configs',
 'dataride.configs.abstracts',
 'dataride.configs.elements',
 'dataride.utils']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'click>=8.1.3,<9.0.0',
 'pyhcl>=0.4.4,<0.5.0',
 'python-hcl2>=3.0.5,<4.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['dataride = dataride.dataride:main']}

setup_kwargs = {
    'name': 'dataride',
    'version': '0.2.3',
    'description': 'Lightning-fast data platform setup for small/medium projects & PoCs',
    'long_description': "\n# dataride: lightning-fast data platform setup toolkit\n\n---\n\n## Introduction\n\n**dataride** is a Python package that enables creating data platform infrastructure within seconds for small/medium projects as well as PoCs (Proof of Concept). It aims to generate ready-to-deploy code for various frameworks, including tools like Terraform and Apache Airflow. It makes use of YAML configuration files to read data platform features that the user is willing to set up.\n\n## Requirements\n\nThe underlying logic makes heavy use of Terraform and Jinja templating. Therefore, to fully exploit package features, it's recommended to install Terraform beforehand (possibly one of the latest stable versions). Instructions on how to do this can be found on the [official Terraform tutorial website](https://learn.hashicorp.com/tutorials/terraform/install-cli).\n\n## Example\n\nBelow you can find and example of running the `dataride` CLI, using config examples that were prepared inside the `config_examples/` directory. It takes **20 seconds** to go from ready config file to infrastructure setup generation. \n\n```\ndataride create -c config_examples/scenario_aws_s3_and_data_catalog.yaml -d results/infra_s3_and_glue\n```\n\n![dataride_showcase](https://raw.githubusercontent.com/mckraqs/dataride/main/media/example_showcase.gif)\n\n## Documentation\n\nFor further description of the package's features, please refer to [docs](https://github.com/mckraqs/dataride/tree/main/docs) directory. All the necessary information is stored there.\n\n## Collaboration\n\nIf you see any room for improvement, feel free to submit a PR! Let's develop dataride to suit as many data teams as possible.\n",
    'author': 'Mateusz Polakowski',
    'author_email': 'mateusz.polakowski.ds@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
