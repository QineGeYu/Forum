"""
Django settings for XH_Forum_Django project.

Generated by 'django-admin startproject' using Django 3.2.24.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1zcx0vk7hbiisp$6=#bqeulc8984k28avvfieb+dcci#8%yoe('
PRIVATE_KEY = '''-----BEGIN RSA PRIVATE KEY----- 
MIIEqQIBAAKCAQEAgsoTAv9BcV+GZWZ5najqLE2CdirAdlAc1Bfrc9oxXFuwPBas
GmuJrwFQHjkf+iduiZgySw+BMtmE4mJRuw4dv9PgW/q0VbdzMbd/B/J4Yk9vsl5h
tNEEpYoRgY0j8sphbAwI44raRtLtHlt7pnya2D5qpf/z2pfqx4sarNDz+Rx6WTFy
5sWviRJl2zcbIvBzOxKvn7I4M+O8UN5nGoJWQZhaP0NWc5c4zH77rYAJESwyB3c0
jU0G7kT+gdjl1HtJEpKjkqFXHHxK8b3wcHBUY6aONC5mtOJkWt4sZmR01QE2yxC0
CniJIVINE8DdNSrHpuyw01SDI0YQlf+oDWA3DQIDAQABAoIBAGWXRTE8yL6hrqkw
8iKOxGbpRf83sgu0qs/sTI3O3CybY8co7UIQagAwCuWPBdGvs2LZf6diQb8Xyup1
6Hpduqn4j/uiP1Wdi7MAj4HCy9PBVEe+nDJxcSSMnJB+6395yDa/GmB0yJve1ySP
dvqZK0XxJbIPoIEZI0FKowbJyMUxVY4qTuvDaiPhBSF3t6Lxpivc30bjtut9otUa
55zJvkroR12qP9k5JMj64w6OCY+fFUVhg7DcPPxRxuK64PuzaMDYr1BWeqmAcsiY
mYaP3aO5hq0ry4u5SDayG82Wj+7E8DWezVbnjfgXQbAaCUgA0XUbwONzhNQnkshT
P3blKRkCgYkAxguZt6oaJbyp/ATRLrawpx88EQiBT6hzZADp5Gt48Q0nkZCfjoQX
Zf4Aei7l+lkldEWfbQ2i1p+rj7kSaCsI9QUbAHi7/OKJab7b9NlpAzXJr8JJyUSD
V1R9vwa4pAX4HqMtQpulgqUwUuKXnpgvnsnLyYB43I0QA7NbV00fyls0jEhk42K9
qwJ5AKkQDK38oR3kWs+JTkaG3He0Yp95mc5BKvc+IaSuFw2/fhVF4ETlwK+aKyYi
napOO1CrRRnH3d7oxjgGSoYgkZIT0vqLRRxyhHHLYzWoGA7nKUev4EuIavyNWea0
yaukgyjjdujKw5mThUQQyLJy7a38O7ug5Dn2JwKBiQC+L3W3AwuJIdy7wISBr7+F
PmGYmepUbRgi+R2j1fGWy2MsTw5q9j7iG0KqE0+XUvS86/9l4qp2IW/H3ZrnnixD
4FtF4Kvm9kWv3zGruP03r/e3aYUiW0EmJGV9hR7bpT/ZbCqSxJX1GF2Hu0KPcuaI
PpINN+rZIj42z47wD4hv85ZLAVqhYrlxAnhmjdjTNhtaMaqwmD8GY0qbxq3IxY/6
YOe6YVMxPXW4nj/Skbews5pGK4QfNwJjS9+JWMurDuXVEWkklRRh9qG3dhUWbKM4
1XLoQJNm+hfV+n29AcBSsWcM2oX9gA+R8lKp3AnGvzEWGTnPB0tnjHYHg6mMcNXh
HyMCgYg/S/mSOOuRVgO+I6iUE9IRXP7mMyPfCBT0xuQhDSQFSEguAGO++Ep2EOVi
+YaeqOhcQXMJm5t9eC4xuxCzVwoQ/pLrVFEgRlhHDLJ9m5b5IkH2/l6WouFtg6NN
7FFOL7NEbSqgQelLqcFOJvcCKGBkem5Yzi4qAHfXd6zoLASaR2L+6W/GH3oc 
-----END RSA PRIVATE KEY-----'''
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# 邮箱配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'  # 腾讯QQ邮箱 SMTP 服务器地址
EMAIL_PORT = 25  # SMTP服务的端口号
EMAIL_HOST_USER = '2928476510@qq.com'  # 发送邮件的QQ邮箱
EMAIL_HOST_PASSWORD = 'jnhxvhhtffjndedh'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
# Application definition
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'XH_Forum_webapp',
    'corsheaders',
    'channels',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True 
ROOT_URLCONF = 'XH_Forum_Django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'C:\\Users\\29284\\Desktop\\XHforum\\XH_Forum_Django\\frontend\\dist')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'XH_Forum_Django.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xh_forum_db',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('localhost', 6379)],  # Redis 服务器的主机和端口
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATICFILES=[os.path.join(BASE_DIR,'C:\\Users\\29284\\Desktop\\XHforum\\XH_Forum_Django\\frontend\\dist\\static')]
ASGI_APPLICATION = "XH_Forum_Django.asgi.application"