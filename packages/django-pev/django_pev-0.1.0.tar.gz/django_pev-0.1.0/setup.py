# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_pev']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.2,<4.0', 'sqlparse']

setup_kwargs = {
    'name': 'django-pev',
    'version': '0.1.0',
    'description': 'Context manager to upload explain plans to https://explain.dalibo.com/',
    'long_description': '# DJDT-PEV2 (Django Debug Toolbar - Postgres explain visualizer 2)\n\n[![PyPI version](https://badge.fury.io/py/django-pev.svg)](https://pypi.org/project/django-pev/)\n[![versions](https://img.shields.io/pypi/pyversions/django-pev.svg)](https://pypi.org/project/django-pev/)\n[![Lint](https://github.com/uptick/django-pev/actions/workflows/ci.yml/badge.svg)](https://github.com/uptick/djdt-pev2/actions/workflows/ci.yml)\n\nThis tool captures sql queries within the context and provides an easy interface to generate and utilize a postgresql explain visualizer (PEV) by [dalibo](https://explain.dalibo.com/).\n\n# Usage\n\n```python\nimport django_pev\n\nwith django_pev.explain(\n    # By default the text of the query is not uploaded for security reasons\n    upload_query=True,\n    title="Analyzing slow User join"\n) as e:\n    # Every SQL query is captured\n    list(User.objects.filter(some__long__join=1).all())\n\n# Rerun the slowest query with `EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON)`\n# And upload the results to https://explain.dalibo.com\npev_response = e.slowest.visualize()\nprint(pev_response.url)\n\n\n# Delete the plan hosted on https://explain.dalibo.com\npev_response.delete()\n```\n\n# Disclaimer\n\nCredit goes to Pierre Giraud (@pgiraud) for PEV2 and Alex Tatiyants (@AlexTatiyants) for the original pev tool.\n\nIN NO EVENT SHALL DALIBO BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF DALIBO HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n\nDALIBO SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER IS ON AN "AS IS" BASIS, AND DALIBO HAS NO OBLIGATIONS TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.\n',
    'author': 'william chu',
    'author_email': 'william.chu@uptickhq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
