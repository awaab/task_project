from task_project.settings_base import *

ALLOWED_HOSTS = ['django-assess-task.herokuapp.com']

DEBUG = False

ADMIN_ENABLED = False

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True
