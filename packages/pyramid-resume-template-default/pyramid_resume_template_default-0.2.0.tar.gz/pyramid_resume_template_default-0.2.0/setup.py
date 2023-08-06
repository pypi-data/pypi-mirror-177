# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyramid_resume_template_default']

package_data = \
{'': ['*'], 'pyramid_resume_template_default': ['static/*', 'templates/*']}

entry_points = \
{'console_scripts': ['pyramid_resume_template_default = '
                     'pyramid_resume_template_default.cli:main']}

setup_kwargs = {
    'name': 'pyramid-resume-template-default',
    'version': '0.2.0',
    'description': 'Default template for pyramid_resume',
    'long_description': '===============================\nPyramid Resume Template Default\n===============================\n\nDefault template for pyramid_resume\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `opensource/templates/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`opensource/templates/cookiecutter-pypackage`: https://gitlab.com/genomicsengland/opensource/templates/cookiecutter-pypackage\n',
    'author': 'Steve Locke',
    'author_email': 'steve@locke.codes',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
