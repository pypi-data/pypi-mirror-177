# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starlette_admin',
 'starlette_admin.contrib',
 'starlette_admin.contrib.mongoengine',
 'starlette_admin.contrib.odmantic',
 'starlette_admin.contrib.sqla',
 'starlette_admin.contrib.sqlmodel']

package_data = \
{'': ['*'],
 'starlette_admin': ['statics/css/*',
                     'statics/css/img/*',
                     'statics/js/*',
                     'statics/js/vendor/*',
                     'statics/webfonts/*',
                     'templates/*',
                     'templates/displays/*',
                     'templates/forms/*',
                     'templates/macros/*',
                     'templates/modals/*']}

install_requires = \
['Jinja2', 'python-multipart', 'starlette']

setup_kwargs = {
    'name': 'starlette-admin',
    'version': '0.3.0.dev5',
    'description': 'Fast, beautiful and extensible administrative interface framework for Starlette/FastApi applications',
    'long_description': '# starlette-admin\n\n*Starlette-Admin* is a fast, beautiful and extensible administrative interface framework for Starlette/FastApi applications.\n\n<p align="center">\n<a href="https://github.com/jowilf/starlette-admin/actions/workflows/test.yml">\n    <img src="https://github.com/jowilf/starlette-admin/actions/workflows/test.yml/badge.svg" alt="Test suite">\n</a>\n<a href="https://github.com/jowilf/starlette-admin/actions">\n    <img src="https://github.com/jowilf/starlette-admin/actions/workflows/publish.yml/badge.svg" alt="Publish">\n</a>\n<a href="https://codecov.io/gh/jowilf/starlette-admin">\n    <img src="https://codecov.io/gh/jowilf/starlette-admin/branch/main/graph/badge.svg" alt="Codecov">\n</a>\n<a href="https://pypi.org/project/starlette-admin/">\n    <img src="https://badge.fury.io/py/starlette-admin.svg" alt="Package version">\n</a>\n<a href="https://pypi.org/project/starlette-admin/">\n    <img src="https://img.shields.io/pypi/pyversions/starlette-admin?color=2334D058" alt="Supported Python versions">\n</a>\n</p>\n\n![Starlette-Admin Promo Image](https://github.com/jowilf/starlette-admin/raw/main/docs/images/promo.png)\n\n## Getting started\n\n* Check out [the documentation](https://jowilf.github.io/starlette-admin).\n* Try the [live demo](https://starlette-admin-demo.jowilf.com/). ([Source code](https://github.com/jowilf/starlette-admin-demo))\n* Try the several usage examples included in the [/examples](https://github.com/jowilf/starlette-admin/tree/main/examples) folder\n\n## Features\n\n- CRUD any data with ease\n- Automatic form validation\n- Advanced table widget with [Datatables](https://datatables.net/)\n- Search and filtering\n- Search highlighting\n- Multi-column ordering\n- Export data to CSV/EXCEL/PDF and Browser Print\n- Authentication\n- Authorization\n- File Support\n- Custom views\n- Supported ORMs\n    * [SQLAlchemy](https://www.sqlalchemy.org/)\n    * [SQLModel](https://sqlmodel.tiangolo.com/)\n    * [MongoEngine](http://mongoengine.org/)\n    * [ODMantic](http://mongoengine.org/)\n- Custom backend ([doc](), [example]())\n  \n\n## Installation\n\n### PIP\n\n```shell\n$ pip install starlette-admin\n```\n\n### Poetry\n\n```shell\n$ poetry add starlette-admin\n```\n\n## Example\n\nThis is a simple example with SQLAlchemy model\n\n```python\nfrom sqlalchemy import Column, Integer, String, create_engine\nfrom sqlalchemy.ext.declarative import declarative_base\nfrom starlette.applications import Starlette\nfrom starlette_admin.contrib.sqla import Admin, ModelView\n\nBase = declarative_base()\nengine = create_engine("sqlite:///test.db", connect_args={"check_same_thread": False})\n\n\n# Define your model\nclass Post(Base):\n    __tablename__ = "posts"\n\n    id = Column(Integer, primary_key=True)\n    title = Column(String)\n\n\nBase.metadata.create_all(engine)\n\napp = Starlette()  # FastAPI()\n\n# Create admin\nadmin = Admin(engine, title="Example: SQLAlchemy")\n\n# Add view\nadmin.add_view(ModelView(Post))\n\n# Mount admin to your app\nadmin.mount_to(app)\n```\nAccess your admin interface in your browser at [http://localhost:8000/admin](http://localhost:8000/admin)\n\n## 3rd party stuff\n\n*starlette-admin* depends on following open source packages:\n\n- [Tabler](https://tabler.io/)\n- [Datatables](https://datatables.net/)\n- [jquery](https://jquery.com/)\n- [Select2](https://select2.org/)\n- [flatpickr](https://flatpickr.js.org/)\n- [moment](http://momentjs.com/)\n- [jsoneditor](https://github.com/josdejong/jsoneditor)\n- [fontawesome](https://fontawesome.com/)',
    'author': 'Jocelin Hounon',
    'author_email': 'hounonj@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jowilf/starlette-admin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
