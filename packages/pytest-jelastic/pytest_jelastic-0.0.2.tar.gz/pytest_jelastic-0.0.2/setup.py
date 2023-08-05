# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pytest_jelastic']
install_requires = \
['jelastic-client>=1.3.28,<2.0.0', 'pytest>=7.2.0,<8.0.0']

setup_kwargs = {
    'name': 'pytest-jelastic',
    'version': '0.0.2',
    'description': 'Pytest plugin defining the necessary command-line options to pass to pytests testing a Jelastic environment.',
    'long_description': '# Pytest-jelastic\n\nAdds the following command-line options to your pytests:\n\n* `--jelastic-api-url`\n* `--jelastic-access-token`\n* `--jelastic-env-name`\n\nand make a `jelastic_env_info` pytest fixture available. \n\n## Publish new package\n\nThe `Publish` teamcity build configuration is only triggered on new git tags. Whenever a new git tag is created, the build configuration is triggered and the package published to the package manager.\n\n```bash\ngit tag -a 1.0.0 -m "my version 1.0.0"\ngit push origin 1.0.0\n```\n\n## Use plugin\n\nIn your python project, first\n\n```bash\npip install pytest-jelastic\n```\n\nThen, when you run your tests, make sure to at least include\n\n```bash\npytest -p pytest_jelastic <your other options>\n```\n',
    'author': 'softozor',
    'author_email': 'softozor@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
