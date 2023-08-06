# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_example',
 'django_example.management',
 'django_example.management.commands',
 'django_example.settings',
 'django_example.tests']

package_data = \
{'': ['*'], 'django_example': ['templates/django_example/*']}

install_requires = \
['bx_django_utils']

entry_points = \
{'console_scripts': ['publish = django_example.publish:publish']}

setup_kwargs = {
    'name': 'django-example',
    'version': '0.2.0rc0',
    'description': 'Demo YunoHost Application to demonstrate the integration of a Django project under YunoHost.',
    'long_description': '# django_example\n\n[![Test](https://github.com/jedie/django_example/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/jedie/django_example/actions/workflows/test.yml)\n[![django_example @ PyPi](https://img.shields.io/pypi/v/django_example?label=django_example%20%40%20PyPi)](https://pypi.org/project/django_example/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/django_example)](https://github.com/jedie/django_example/blob/main/pyproject.toml)\n[![License GPL](https://img.shields.io/pypi/l/django_example)](https://github.com/jedie/django_example/blob/main/LICENSE)\n\n\nExample Django Project for: https://github.com/YunoHost-Apps/django_example_ynh\n\n\n[![Integration level](https://dash.yunohost.org/integration/django_example_ynh.svg)](https://dash.yunohost.org/appci/app/django_example_ynh) ![](https://ci-apps.yunohost.org/ci/badges/django_example_ynh.status.svg) ![](https://ci-apps.yunohost.org/ci/badges/django_example_ynh.maintain.svg)\n[![Install django_example_ynh with YunoHost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=django_example_ynh)\n',
    'author': 'JensDiemer',
    'author_email': 'git@jensdiemer.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jedie/django_example',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0.0',
}


setup(**setup_kwargs)
