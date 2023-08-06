# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['balcony', 'balcony.custom_nodes']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'boto3>=1.24.80,<2.0.0',
 'inflect>=6.0.0,<7.0.0',
 'jmespath>=1.0.1,<2.0.0',
 'mkdocs-autorefs>=0.4.1,<0.5.0',
 'mkdocs-material>=8.5.7,<9.0.0',
 'mkdocstrings[python]>=0.19.0,<0.20.0',
 'rich>=12.5.1,<13.0.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['balcony = balcony.cli:run_app']}

setup_kwargs = {
    'name': 'balcony',
    'version': '0.0.61',
    'description': 'AWS API for humans',
    'long_description': '# balcony\n\nAWS API for us humans.\n\nBalcony helps to lift the undifferentiated heavy lifting that is reading from AWS SDK & API.\n\nBalcony fills out the **required parameters** for any operation, automatically. \n\n\n## Installation\n\n```bash\npip3 install balcony\n\npython3 -m pip install balcony\n```\n\n\n## Basic Usage\n#### List all available AWS Services\n\n```bash\nbalcony aws\n```\n#### List all Resource Nodes of a Service\n```bash\nbalcony aws iam\n\nbalcony aws ec2\n```\n#### See the documentation of a Resource Node and its Operations\n```bash\nbalcony aws iam Policy -l\n# or\nbalcony aws iam Policy --list\n```\n\n\n#### Read a Resource Node\n\n\n```bash\nbalcony aws iam Policy\n\n# if you are curious to see what\'s going on \n# under the hood, enable the debug messages \nbalcony aws iam Policy -d\n# or\nbalcony aws iam Policy --debug\n```\n#### Read a Resource Nodes specific operation\n\n```bash\nbalcony aws iam Policy get\n\nbalcony aws iam Policy list\n```\n\n#### Filter generated parameters with UNIX style pattern matching\n```bash\nbalcony aws iam Policy get  -p "*service-role/*"\n\n# supports multiple patterns \nbalcony aws iam Policy -p "*service-role/*" -p "*prod-*"\n\n```\n\n#### Use queries for the json data -- like `jq`\n```bash\nbalcony aws iam Policy \\\n    --jmespath-selector "GetPolicy[*].Policy"\n# or\nbalcony aws iam Policy \\\n    -js "GetPolicy[*].Policy"\n```\n\n#### Use `--format` option for customized output\n\n```bash\n# create stop-instances script for running instances\nbalcony aws ec2 Instances \\\n    -js "DescribeInstances[*].Reservations[*].Instances[?State.Name==\'running\'][][]" \\\n    --format "aws ec2 stop-instances --instance-ids {InstanceId} # {Tags}"\n\n# create delete-policy script\nbalcony aws iam Policy \\\n    --jmespath-selector "GetPolicy[*].Policy" \\\n    --format "aws iam delete-policy --policy-arn {Arn}"\n```',
    'author': 'Oguzhan Yilmaz',
    'author_email': 'oguzhanylmz271@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
