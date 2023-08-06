# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dit_activity_stream',
 'dit_activity_stream.test_app',
 'dit_activity_stream.tests']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2,<4.2', 'django-hawk>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'dit-activity-stream',
    'version': '0.1.0',
    'description': 'DIT Activity Stream',
    'long_description': '# DIT Activity Stream\n\n## Installation\n\nRead the [Django Hawk installation](https://github.com/uktrade/django-hawk/#installation) documentation.\n\nAdd the package to your `urls.py` file.\n\n```python\nfrom django.urls import include, path\n\nurlpatterns = [\n    ...\n    path("dit-activity-stream/", include("dit_activity_stream.urls")),\n    ...\n]\n```\n\n## How to implement?\n\nWrite your custom client, here is an example client for returning all users:\n\n```python\nfrom typing import Any, Dict\n\nfrom django.contrib.auth import get_user_model\nfrom django.db.models import QuerySet\nfrom django.http import HttpRequest\n\nfrom dit_activity_stream.client import ActivityStreamClient\n\nUser = get_user_model()\n\n\nclass ActivityStreamUserClient(ActivityStreamClient):\n    object_uuid_field: str = "user_id"\n    object_last_modified_field: str = "last_modified"\n\n    def get_queryset(self, request: HttpRequest) -> QuerySet:\n        return User.objects.all()\n\n    def render_object(self, object: User) -> Dict:\n        return {\n            "id": object.id,\n            "username": object.username,\n            "first_name": object.first_name,\n            "last_name": object.last_name,\n        }\n```\n\nWhere the following attributes:\n- `object_uuid_field` is a field on the Object that is a Unique Identifier for the object.\n  - This will be output in the URL GET parameter so it should be a UUID.\n- `object_last_modified_field` us a field on the Object that holds a datetime value of when the object was last modified.\n  - This will be output in the URL GET parameter.\n\nSet `DIT_ACTIVITY_STREAM_CLIENT_CLASS` in your django settings file:\n\n```python\nDIT_ACTIVITY_STREAM_CLIENT_CLASS = "package.client.ActivityStreamUserClient"\n```\n\n## Pushing to PyPI\n\n- [PyPI Package](https://pypi.org/project/dit-activity-stream/)\n- [Test PyPI Package](https://test.pypi.org/project/dit-activity-stream/)\n\nRunning `make build` will build the package into the `dist/` directory.\nRunning `make push-pypi-test` will push the built package to Test PyPI.\nRunning `make push-pypi` will push the built package to PyPI.\n\n### Setting up poetry for pushing to PyPI\n\nFirst you will need to add the test pypy repository to your poetry config:\n\n```\npoetry config repositories.test-pypi https://test.pypi.org/legacy/\n```\n\nThen go to https://test.pypi.org/manage/account/token/ and generate a token.\n\nThen add it to your poetry config:\n\n```\npoetry config pypi-token.test-pypi XXXXXXXX\n```\n\nThen you also need to go to https://pypi.org/manage/account/token/ to generate a token for the real PyPI.\n\nThen add it to your poetry config:\n\n```\npoetry config pypi-token.pypi XXXXXXXX\n```\n\nNow the make commands should work as expected.\n',
    'author': 'Cameron Lamb',
    'author_email': 'live.services@digital.trade.gov.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/uktrade/dit-activity-stream',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.3,<4.0.0',
}


setup(**setup_kwargs)
