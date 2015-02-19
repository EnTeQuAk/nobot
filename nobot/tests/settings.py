SECRET_KEY = 'test'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.sqlite',
    }
}

INSTALLED_APPS = [
    'nobot',
]

NOBOT_RECAPTCHA_PRIVATE_KEY = 'privkey'
NOBOT_RECAPTCHA_PUBLIC_KEY = 'pubkey'
