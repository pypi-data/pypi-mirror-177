# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_hawk_drf', 'django_hawk_drf.tests']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2,<4.2',
 'django-hawk>=1.1.0,<2.0.0',
 'djangorestframework>=3.10.3,<4.0']

setup_kwargs = {
    'name': 'django-hawk-drf',
    'version': '1.1.0',
    'description': 'Authenticate Django Rest Framework Views with django-hawk',
    'long_description': '# Django Hawk DRF\n\nThis package provides [Django Rest Framework](https://github.com/encode/django-rest-framework/) helper classes for use with [Django Hawk](https://github.com/uktrade/django-hawk).\n\n## Installation\n\nRead the [Django Hawk installation](https://github.com/uktrade/django-hawk#installation) documentation.\n\n## Example usage\n\nRead the [Django Hawk example usage](https://github.com/uktrade/django-hawk#example-usage) documentation.\n\nAdd the `HawkResponseMiddleware` to the `MIDDLEWARE` setting in your project like so:\n\n```\nMIDDLEWARE = [\n    ...\n    "django_hawk.middleware.HawkResponseMiddleware",\n    "django_hawk_drf.middleware.HawkResponseMiddleware",\n    ...\n]\n```\n\nTo check the you can use the `django_hawk.authentication.HawkAuthentication` authentication class.\n\n```python\nfrom rest_framework.response import Response\nfrom rest_framework.viewsets import ViewSet\n\nfrom django_hawk_drf.authentication import HawkAuthentication\n\n\nclass ExampleViewSet(ViewSet):\n    authentication_classes = (HawkAuthentication,)\n    permission_classes = ()\n\n    def list(self, request):\n        return Response([])\n```\n\n## Testing\n\nTests belong in the `/django_hawk_drf/tests/` directory. You can run the tests by installing the requirements like so:\n\n\n```\nmake setup\n```\n\nNow you can run the tests using the following command:\n\n```\npoetry run python manage.py test\n```\n\n### Tox tests\n\nWe use [tox](https://pypi.org/project/tox/) to test compatibility across different Django versions.\n\nTo run these tests with tox, just run the following:\n\n```\nmake tox\n```\n\n## Pushing to PyPI\n\n- [PyPI Package](https://pypi.org/project/django-hawk-drf/)\n- [Test PyPI Package](https://test.pypi.org/project/django-hawk-drf/)\n\nRunning `make build-package` will build the package into the `dist/` directory\nRunning `make push-pypi-test` will push the built package to Test PyPI\nRunning `make push-pypi` will push the built package to PyPI\n',
    'author': 'Cameron Lamb',
    'author_email': 'live.services@digital.trade.gov.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/uktrade/django-hawk-drf/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
