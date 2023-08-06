# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_keycloak',
 'django_keycloak.api',
 'django_keycloak.management',
 'django_keycloak.management.commands',
 'django_keycloak.migrations']

package_data = \
{'': ['*']}

install_requires = \
['cachetools>=5.0.0',
 'django>=2.2',
 'djangorestframework>=3.0',
 'dry-rest-permissions>=0.1',
 'python-keycloak>=2.6.0']

setup_kwargs = {
    'name': 'django-uw-keycloak',
    'version': '2.0.2',
    'description': 'Middleware to allow authorization using Keycloak and Django',
    'long_description': '# Django Keycloak Authorization\n\nMiddleware to allow authorization using Keycloak and Django for django-rest-framework (DRF) and Graphene-based projects.\nThis package should only be used in projects starting from scratch, since it overrides the users\' management.\n\n## Installation\n\n1. Add the module to your environment\n    * With PIP:\n\n        ```shell\n        pip install django-uw-keycloak\n        ```\n\n    * By compiling from source:\n\n        ```shell\n        git clone https://github.com/urbanplatform/django-keycloak-auth && \\\n        cd django-keycloak-auth && \\\n        python3 setup.py install\n        ```\n\n2. Add `django_keycloak` to the Django project\'s `INSTALLED_APPS` set in the `settings` file\n3. Add `django_keycloak.middleware.KeycloakMiddleware` to the Django `MIDDLEWARE` set in the `settings` file\n4. In your Django project\'s `settings` file, change the Django `AUTHENTICATION_BACKENDS` to:\n\n    ```python\n    AUTHENTICATION_BACKENDS = (\'django_keycloak.backends.KeycloakAuthenticationBackend\',)\n    ```\n\n5. Add the following configuration to Django settings and replace the values with your own configuration attributes:\n\n    ```python\n    KEYCLOAK_CONFIG = {\n        # The Keycloak\'s Public Server URL (e.g. http://localhost:8080)\n        \'SERVER_URL\': \'<PUBLIC_SERVER_URL>\',\n        # The Keycloak\'s Internal URL \n        # (e.g. http://keycloak:8080 for a docker service named keycloak)\n        # Optional: Default is SERVER_URL\n        \'INTERNAL_URL\': \'<INTERNAL_SERVER_URL>\',\n        # Override for default Keycloak\'s base path\n        # Default is \'/auth/\'\n        \'BASE_PATH\': \'/auth/\',\n        # The name of the Keycloak\'s realm\n        \'REALM\': \'<REALM_NAME>\',\n        # The ID of this client in the above Keycloak realm\n        \'CLIENT_ID\': \'<CLIENT_ID>\' \n        # The secret for this confidential client\n        \'CLIENT_SECRET_KEY\': \'<CLIENT_SECRET_KEY>\',\n        # The name of the admin role for the client\n        \'CLIENT_ADMIN_ROLE\': \'<CLIENT_ADMIN_ROLE>\',\n        # The name of the admin role for the realm\n        \'REALM_ADMIN_ROLE\': \'<REALM_ADMIN_ROLE>\',\n        # Regex formatted URLs to skip authentication\n        \'EXEMPT_URIS\': [],\n        # Flag if the token should be introspected or decoded (default is False)\n        \'DECODE_TOKEN\': False,\n        # Flag if the audience in the token should be verified (default is True)\n        \'VERIFY_AUDIENCE\': True,\n        # Flag if the user info has been included in the token (default is True)\n        \'USER_INFO_IN_TOKEN\': True,\n        # Flag to show the traceback of debug logs (default is False)\n        \'TRACE_DEBUG_LOGS\': False,\n        # The token prefix that is expected in Authorization header (default is \'Bearer\')\n        \'TOKEN_PREFIX\': \'Bearer\'\n    }\n    ```\n\n6. Override the Django user model in the `settings` file:\n\n     ```python\n    AUTH_USER_MODEL = "django_keycloak.KeycloakUserAutoId"\n    ```\n\n7. Configure Django-Rest-Framework authentication classes with `django_keycloak.authentication.KeycloakAuthentication`:\n\n    ```python\n    REST_FRAMEWORK = {\n        # ... other rest framework settings.\n        \'DEFAULT_AUTHENTICATION_CLASSES\': [\n            \'django_keycloak.authentication.KeycloakAuthentication\'\n        ],\n    }\n    ```\n\n## Customization\n\n### Server URLs\n\nTo customise Keycloak\'s URL path, set `BASE_PATH` (for example `/my_path` or `/`) as follows:\n\n* `SERVER_URL/auth/admin/...` to `SERVER_URL/my_path/admin/...`\n* `SERVER_URL/auth/realms/...` to `SERVER_URL/realms/...`\n\nIf your OAuth clients (web or mobile app) use a different URL than your Django service, specify the public URL (`https://oauth.example.com`) in `SERVER_URL` and the internal URL (`http://keycloak.local`) in `INTERNAL_URL`.\n\n## DRY Permissions\n\nThe permissions must be set like in other projects. You must set the\npermissions configuration for each model. Example:\n\n```python\n@staticmethod\n@authenticated_users\ndef has_read_permission(request):\n    roles = request.remote_user.get(\'client_roles\')\n\n    return True if \'ADMIN\' in roles else False\n```\n\n## Keycloak users synchronization\n\nThe management command `sync_keycloak_users` must be ran periodically, in\norder to remove from the users no longer available at\nKeycloak from the local users. This command can be called using the task named\n`sync_users_with_keycloak`, using Celery. Fot that, you just need to:\n\n* Add the task to the `CELERY_BEAT_SCHEDULE` ìn the Django project\'s settings:\n\n  ```python\n  CELERY_BEAT_SCHEDULE = {\n      \'sync_users_with_keycloak\': {\n          \'task\': \'django_keycloak.tasks.sync_users_with_keycloak\',\n          \'schedule\': timedelta(hours=24),\n          \'options\': {\'queue\': \'sync_users\'}\n      },\n  }\n  ```\n\n* Add the `sync_users` queue to the `docker-compose`\'s `celery` service:\n\n  `command: celery worker -A citibrain_base -B -E -l info -Q backup,celery,sync_users --autoscale=4,1`\n\n**Attention:** This task is only responsible to delete users from local\nstorage. The creation of new users, on Keycloak, is done when they\ntry to login.\n\n## Notes\n\nSupport for celery 5: from version 0.7.4 on we should use celery 5 for the user sync. This implies running celery with `celery -A app worker ...` instead of `celery worker -A app ...`\n\n## Contact\n\ndjango-keycloak-auth [at] googlegroups [dot] com\n',
    'author': 'Ubiwhere',
    'author_email': 'urbanplatform@ubiwhere.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/urbanplatform/django-keycloak-auth',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
