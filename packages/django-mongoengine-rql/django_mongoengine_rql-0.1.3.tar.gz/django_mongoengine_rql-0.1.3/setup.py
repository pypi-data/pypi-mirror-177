# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dj_mongoengine_rql']

package_data = \
{'': ['*']}

install_requires = \
['django-mongoengine>=0.5.4,<0.6.0', 'django-rql>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'django-mongoengine-rql',
    'version': '0.1.3',
    'description': 'Django Mongoengine RQL Filtering',
    'long_description': "# Django Mongoengine RQL\n\n[![pyversions](https://img.shields.io/pypi/pyversions/django-mongoengine-rql.svg)](https://pypi.org/project/django-mongoengine-rql/)\n[![PyPi Status](https://img.shields.io/pypi/v/django-mongoengine-rql.svg)](https://pypi.org/project/django-mongoengine-rql/)\n[![PyPI status](https://img.shields.io/pypi/status/django-mongoengine-rql.svg)](https://pypi.org/project/django-mongoengine-rql/)\n[![PyPI Downloads](https://img.shields.io/pypi/dm/django-mongoengine-rql)](https://pypi.org/project/django-mongoengine-rql/)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=django-mongoengine-rql&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=django-mongoengine-rql)\n[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=django-mongoengine-rql&metric=coverage)](https://sonarcloud.io/summary/new_code?id=django-mongoengine-rql)\n\n\n## Introduction\n\nRQL (Resource query language) is designed for modern application development. It is built for the web, ready for NoSQL, and highly extensible with simple syntax.\nThis is a query language for fast and convenient database interaction. RQL was designed for use in URLs to request object-style data structures.\n\nThis library is a Django-Mongoengine specific implementation of RQL filtering.\n\n[RQL Reference](https://connect.cloudblue.com/community/api/rql/)\n\n[Django RQL](https://github.com/cloudblue/django-rql)\n\n[Django Mongoengine](https://github.com/MongoEngine/django-mongoengine)\n\n## Install\n\n`Django Mongoengine RQL` can be installed from [pypi.org](https://pypi.org/project/django-mongoengine-rql/) using pip:\n\n```\n$ pip install django-mongoengine-rql\n```\n\n## Documentation\n\nThis library is fully based on [Django RQL](https://github.com/cloudblue/django-rql), so there are no specific docs for it.\nFull documentation for Django-RQL is available at [https://django-rql.readthedocs.org](https://django-rql.readthedocs.org).\n\n## Example\n\n```python\n# filters.py\nfrom dj_mongoengine_rql.filter_cls import MongoengineRQLFilterClass\nfrom py_rql.constants import FilterLookups\nfrom your_docs import Document\n\nclass DocFilters(MongoengineRQLFilterClass):\n    MODEL = Document\n    SELECT = True\n    FILTERS = (\n        'filter1',\n        {\n            'filter': 'filter2',\n            'source': 'related_doc__doc_field',\n        },\n        {\n            'namespace': 'ns1',\n            'filters': ('ns1f',),\n        },\n        {\n            'filter': 'filter3',\n            'lookups': {FilterLookups.EQ, FilterLookups.IN},\n        },\n    )\n\n\n# views.py\nfrom dj_rql.drf.backend import RQLFilterBackend\nfrom dj_rql.drf.paginations import RQLContentRangeLimitOffsetPagination\nfrom rest_framework import mixins\nfrom rest_framework.viewsets import GenericViewSet\n\nclass DRFViewSet(mixins.ListModelMixin, GenericViewSet):\n    queryset = Document.objects.all()\n    rql_filter_class = DocFilters\n    pagination_class = RQLContentRangeLimitOffsetPagination\n    filter_backends = (RQLFilterBackend,)\n\n```\n\n## Notes\n\nDue to implementation and Mongo engine features there may be some limitations in filtering, for example:\n* `distinct` setting is not supported for filters\n* annotations are not supported, as well\n\n\n## Development\n\n1. Python 3.8+\n0. Install dependencies `pip install poetry && poetry install`\n\n## Testing\n\n1. Python 3.8+\n0. Install dependencies `pip install poetry && poetry install`\n\nCheck code style: `poetry run flake8`\nRun tests: `poetry run pytest`\nRun integration tests: `docker compose run app_test`\n\nTests reports are generated in `tests/reports`.\n* `out.xml` - JUnit test results\n* `coverage.xml` - Coverage xml results\n\nTo generate HTML coverage reports use:\n`--cov-report html:tests/reports/cov_html`\n\n## License\n\n`Django Mongoengine RQL` is released under the [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).\n",
    'author': 'CloudBlue LLC',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://connect.cloudblue.com/community/api/rql/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
