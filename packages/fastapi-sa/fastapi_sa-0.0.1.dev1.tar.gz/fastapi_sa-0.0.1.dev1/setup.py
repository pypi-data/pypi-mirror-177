# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fastapi_sa']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy[asyncio]>=1.4.43,<2.0.0', 'starlette>=0.19.1']

setup_kwargs = {
    'name': 'fastapi-sa',
    'version': '0.0.1.dev1',
    'description': 'fastapi-sa provides a simple integration between FastAPI and SQLAlchemy in your application',
    'long_description': '# fastapi-sa\n\n![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/whg517/fastapi-sa/main/main?style=flat-square)\n![GitHub](https://img.shields.io/github/license/whg517/fastapi-sa?style=flat-square)\n![Python](https://img.shields.io/pypi/pyversions/fastapi-sa)\n![PyPI](https://img.shields.io/pypi/v/fastapi-sa?style=flat-square)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/c76cfa7d7d274f899967019900465403)](https://www.codacy.com/gh/whg517/fastapi-sa/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=whg517/fastapi-sa&amp;utm_campaign=Badge_Grade)\n[![codecov](https://codecov.io/gh/whg517/fastapi-sa/branch/main/graph/badge.svg?token=F098K6GGGC)](https://codecov.io/gh/whg517/fastapi-sa)\n\nfastapi-sa provides a simple integration between FastAPI and SQLAlchemy in your application.\nyou can use decorators or middleware to transaction management.\n\n## Installing\n\ninstall and update using pip:\n\n```shell\npip install fastapi-sa\n```\n\n## Examples\n\n### Create models for examples, `models.py`\n\n```python\nfrom pydantic import BaseModel\nfrom sqlalchemy import Column, Integer, String\nfrom sqlalchemy.orm import declarative_base\n\nBase = declarative_base()\n\n\nclass User(Base):\n    """UserModel"""\n    __tablename__ = \'user\'\n    id = Column(Integer, primary_key=True)\n    name = Column(String(255))\n    age = Column(Integer)\n\n\nclass UserSchema(BaseModel):\n    """user schema"""\n    id: int\n    name: str\n    age: int\n\n    class Config:\n        """config"""\n        orm_mode = True\n```\n\n### Database migrations for examples\n\ncode for create tables, also you can use database migrations.\n\n```python\nfrom sqlalchemy import create_engine\nfrom models import Base\n\nengine = create_engine(\'sqlite+aiosqlite:////tmp/test.db\')\nBase.metadata.create_all(engine) \n```\n\n### DB init for examples\n\n```python\nfrom fastapi_sa.database import db\n\ndb.init(url=\'sqlite+aiosqlite:////tmp/test.db\')\n```\n\n### Usage 1: fastapi middleware\n\n```python\nfrom fastapi import FastAPI\nfrom sqlalchemy import select\n\nfrom fastapi_sa.database import db\nfrom fastapi_sa.middleware import DBSessionMiddleware\nfrom tests.example.db import User, UserSchema\n\napp = FastAPI()\napp.add_middleware(DBSessionMiddleware)\n\n\n@app.get(\'/users\')\nasync def get_users():\n    """get all users"""\n    result = await db.session.scalars(select(User))\n    objs = [UserSchema.from_orm(i) for i in result.all()]\n    return objs\n```\n\n### Usage 2: other asynchronous database operations\n\n```python\nfrom sqlalchemy import select\n\nfrom fastapi_sa.database import db, session_ctx\nfrom tests.example.db import User, UserSchema\n\n\n@session_ctx\nasync def get_users():\n    """get users"""\n    results = await db.session.scalars(select(User))\n    objs = [UserSchema.from_orm(i) for i in results.all()]\n    return objs\n```\n\n### Usage 3: with fixtures in pytest\n\n```python\nimport pytest\nfrom fastapi_sa.database import db\n\n\n@pytest.fixture()\ndef db_session_ctx():\n    """db session context"""\n    token = db.set_session_ctx()\n    yield\n    db.reset_session_ctx(token)\n\n\n@pytest.fixture()\nasync def session(db_session_ctx):\n    """session fixture"""\n    async with db.session.begin():\n        yield db.session\n```\n\nIf you initialize data in fixture, please use\n\n```python\nfrom fastapi_sa.database import db\nfrom models import User\n\nasync with db():\n    users = User(name=\'aoo\', age=12)\n    db.session.add(users)\n    await db.session.flush()\n```\n\nif you test class methods, please use\n\n```python\nimport pytest\nfrom sqlalchemy import func, select\nfrom models import User, UserSchema\nfrom fastapi_sa.database import db\n\n\nclass UserRepository:\n    """user repository"""\n\n    @property\n    def model(self):\n        """model"""\n        return User\n\n    async def get_all(self):\n        """get all"""\n        result = await db.session.scalars(select(self.model))\n        objs = [UserSchema.from_orm(i) for i in result.all()]\n        return objs\n\n\n# the test case is as follows    \n\n@pytest.fixture()\ndef repo():\n    """repo"""\n    return UserRepository()\n\n\n@pytest.mark.asyncio\nasync def test_get_all(session, init_user, repo):\n    """test get all"""\n    objs = await repo.get_all()\n    length = await session.scalar(select(func.count()).select_from(User))\n    assert len(objs) == length\n```\n\n## Similar design\n\n- [FastAPI-SQLAlchemy](https://github.com/mfreeborn/fastapi-sqlalchemy)\n\n## Based on\n\n- [FastAPI](https://github.com/tiangolo/fastapi)\n- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)\n\n## Develop\n\nYou may need to read the [develop document](./docs/development.md) to use SRC Layout in your IDE.\n',
    'author': 'huagang',
    'author_email': 'huagang517@126.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
