# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_hawk', 'django_hawk.tests']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2,<4.2', 'mohawk>=1.0.0,<2.0']

setup_kwargs = {
    'name': 'django-hawk',
    'version': '1.1.1',
    'description': 'Authenticate Django Views with HAWK',
    'long_description': '# Django Hawk\n\nThis package can be used to help create HAWK Authenticated views.\n\n## Installation\n\n```\npip install django-hawk\n```\n\nAdd the following to your Django Settings:\n\n```python\nDJANGO_HAWK = {\n    "HAWK_INCOMING_ACCESS_KEY": "xxx",\n    "HAWK_INCOMING_SECRET_KEY": "xxx",\n}\n```\n\n## Example Usage\n\nTo use the HAWK Authentication, we need to do 2 things:\n\n1. Make sure the `HawkResponseMiddleware` runs\n2. Check the authentication\n\nAdd the `HawkResponseMiddleware` to the `MIDDLEWARE` setting in your project like so:\n\n```\nMIDDLEWARE = [\n    ...\n    "django_hawk.middleware.HawkResponseMiddleware",\n    ...\n]\n```\n\nTo check the authentication you can call `django_hawk.utils.authenticate_request`, if an exception isn\'t raised then you know that the request is authenticated, see below for examples.\n\n```python\nfrom django.http import HttpResponse\n\nfrom django_hawk.utils import DjangoHawkAuthenticationFailed, authenticate_request\n\ndef simple_view(request):\n    # Try to authenticate with HAWK\n    try:\n        authenticate_request(request=request)\n    except DjangoHawkAuthenticationFailed as e:\n        return HttpResponse(status=401)\n\n    # Continue with normal View code...\n    return HttpResponse("This is a simple view")\n```\n\n## Testing\n\nTests belong in the `/django_hawk/tests/` directory. You can run the tests by installing the requirements like so:\n\n```\nmake setup\n```\n\nNow you can run the tests using the following command:\n\n```\npoetry run python manage.py test\n```\n\n### Tox tests\n\nWe use [tox](https://pypi.org/project/tox/) to test compatibility across different Django versions.\n\nTo run these tests with tox, just run the following:\n\n```\nmake tox\n```\n\n## Pushing to PyPI\n\n- [PyPI Package](https://pypi.org/project/django-hawk/)\n- [Test PyPI Package](https://test.pypi.org/project/django-hawk/)\n\nRunning `make build-package` will build the package into the `dist/` directory\nRunning `make push-pypi-test` will push the built package to Test PyPI\nRunning `make push-pypi` will push the built package to PyPI\n\n### Setting up poetry for pushing to PyPI\n\nFirst you will need to add the test pypy repository to your poetry config:\n\n```\npoetry config repositories.test-pypi https://test.pypi.org/legacy/\n```\n\nThen go to https://test.pypi.org/manage/account/token/ and generate a token.\n\nThen add it to your poetry config:\n\n```\npoetry config pypi-token.test-pypi XXXXXXXX\n```\n\nThen you also need to go to https://pypi.org/manage/account/token/ to generate a token for the real PyPI.\n\nThen add it to your poetry config:\n\n```\npoetry config pypi-token.pypi XXXXXXXX\n```\n\nNow the make commands should work as expected.\n',
    'author': 'Cameron Lamb',
    'author_email': 'live.services@digital.trade.gov.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/uktrade/django-hawk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
