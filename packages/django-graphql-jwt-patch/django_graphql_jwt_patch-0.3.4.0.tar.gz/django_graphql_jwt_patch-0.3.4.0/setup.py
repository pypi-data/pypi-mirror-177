# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphql_jwt',
 'graphql_jwt.refresh_token',
 'graphql_jwt.refresh_token.admin',
 'graphql_jwt.refresh_token.management',
 'graphql_jwt.refresh_token.management.commands',
 'graphql_jwt.refresh_token.migrations']

package_data = \
{'': ['*'],
 'graphql_jwt': ['locale/ar/LC_MESSAGES/*',
                 'locale/es/LC_MESSAGES/*',
                 'locale/fr/LC_MESSAGES/*',
                 'locale/nl/LC_MESSAGES/*',
                 'locale/pt_BR/LC_MESSAGES/*',
                 'locale/zh_Hans/LC_MESSAGES/*'],
 'graphql_jwt.refresh_token': ['locale/ar/LC_MESSAGES/*',
                               'locale/es/LC_MESSAGES/*',
                               'locale/fr/LC_MESSAGES/*',
                               'locale/nl/LC_MESSAGES/*',
                               'locale/pt_BR/LC_MESSAGES/*',
                               'locale/zh_Hans/LC_MESSAGES/*']}

install_requires = \
['Django>=2.0',
 'PyJWT>=2,<3',
 'graphene-django-patch>=2.0.0',
 'graphene>=2.1.5']

setup_kwargs = {
    'name': 'django-graphql-jwt-patch',
    'version': '0.3.4.0',
    'description': 'JSON Web Token for Django GraphQL.',
    'long_description': '<p align="center">\n  <a href="https://django-graphql-jwt.domake.io/"><img width="420px" src="https://django-graphql-jwt.domake.io/_static/logo.png" alt=\'Django GraphQL JWT\'></a>\n</p>\n\n<p align="center">\n    JSON Web Token authentication for Django GraphQL.\n    <br>Fantastic <strong>documentation</strong> is available at <a href="https://django-graphql-jwt.domake.io">https://django-graphql-jwt.domake.io</a>.\n</p>\n<p align="center">\n    <a href="https://github.com/flavors/django-graphql-jwt/actions">\n        <img src="https://github.com/flavors/django-graphql-jwt/actions/workflows/test-suite.yml/badge.svg" alt="Test">\n    </a>\n    <a href="https://codecov.io/gh/flavors/django-graphql-jwt">\n        <img src="https://img.shields.io/codecov/c/github/flavors/django-graphql-jwt?color=%2334D058" alt="Coverage">\n    </a>\n    <a href="https://www.codacy.com/gh/flavors/django-graphql-jwt/dashboard">\n        <img src="https://app.codacy.com/project/badge/Grade/4f9fd439fbc74be88a215b9ed2abfcf9" alt="Codacy">\n    </a>\n    <a href="https://pypi.python.org/pypi/django-graphql-jwt">\n        <img src="https://img.shields.io/pypi/v/django-graphql-jwt.svg" alt="Package version">\n    </a>\n</p>\n\n## Installation\n\nInstall last stable version from Pypi:\n\n```sh\npip install django-graphql-jwt\n```\n\nAdd `AuthenticationMiddleware` middleware to your *MIDDLEWARE* settings:\n\n\n```py\nMIDDLEWARE = [\n    # ...\n    "django.contrib.auth.middleware.AuthenticationMiddleware",\n    # ...\n]\n```\n\nAdd `JSONWebTokenMiddleware` middleware to your *GRAPHENE* settings:\n\n```py\nGRAPHENE = {\n    "SCHEMA": "mysite.myschema.schema",\n    "MIDDLEWARE": [\n        "graphql_jwt.middleware.JSONWebTokenMiddleware",\n    ],\n}\n```\n\nAdd `JSONWebTokenBackend` backend to your *AUTHENTICATION_BACKENDS*:\n\n```py\nAUTHENTICATION_BACKENDS = [\n    "graphql_jwt.backends.JSONWebTokenBackend",\n    "django.contrib.auth.backends.ModelBackend",\n]\n```\n\n## Schema\n\nAdd *django-graphql-jwt* mutations to the root schema:\n\n```py\nimport graphene\nimport graphql_jwt\n\n\nclass Mutation(graphene.ObjectType):\n    token_auth = graphql_jwt.ObtainJSONWebToken.Field()\n    verify_token = graphql_jwt.Verify.Field()\n    refresh_token = graphql_jwt.Refresh.Field()\n\n\nschema = graphene.Schema(mutation=Mutation)\n```\n',
    'author': 'Gabriel Sebag',
    'author_email': 'hello@gabrielsebag.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gabrielsebag/django-graphql-jwt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
