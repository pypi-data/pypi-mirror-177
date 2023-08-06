# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_healthchecks',
 'fastapi_healthchecks.api',
 'fastapi_healthchecks.checks']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.70.1', 'pydantic>=1.9']

extras_require = \
{'all': ['aio-pika>=7',
         'aioboto3>=9.3',
         'aiohttp[speedups]>=3,<4',
         'asyncpg>=0.25.0',
         'redis>=4,<5'],
 'ceph': ['aioboto3>=9.3'],
 'http': ['aiohttp[speedups]>=3,<4'],
 'postgres': ['asyncpg>=0.25.0'],
 'rabbitmq': ['aio-pika>=7'],
 'redis': ['redis>=4,<5']}

setup_kwargs = {
    'name': 'fastapi-healthchecks',
    'version': '1.0.6',
    'description': 'FastAPI Healthchecks',
    'long_description': '# FastAPI health checks\n\nConfigurable health checks endpoints for FastAPI applications.\n\n## Quickstart\n\n```python\napp = FastAPI()\napp.include_router(\n    HealthcheckRouter(\n        Probe(\n            name="readiness",\n            checks=[\n                PostgreSqlCheck(host="db.example.com", username=..., password=...),\n                RedisCheck(host="redis.example.com", username=..., password=...),\n            ],\n        ),\n        Probe(\n            name="liveness",\n            checks=[\n                ...,\n            ],\n        ),\n    ),\n    prefix="/health",\n)\n```\n\nThe probes from this example will be available as `GET /health/readiness` and `GET /health/liveness`.\n\n## Bundled checks\n\n* `PostgreSqlCheck` – checks PostgreSQL server availability\n* `RedisCheck` – checks Redis server availability\n* `RabbitMqCheck` – checks RabbitMQ server availability\n* `SettingsCheck` – validates settings models based on pydantic BaseModel\n* `HttpCheck` – checks availability of specified URL\n* `CephCheck` – checks Ceph server availability\n\n## Custom checks\n\nYou can create your own checks by providing custom `fastapi_healthchecks.checks.Check` implementations. Like this:\n\n```python\nclass MaintenanceCheck(Check):\n    async def __call__(self) -> CheckResult:\n        if is_maintenance():\n            return CheckResult(name="Maintenance", passed=False, details="Closed for maintenance")\n        else:\n            return CheckResult(name="Maintenance", passed=True)\n```\n',
    'author': 'RockITSoft',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
