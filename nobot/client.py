import json
import collections

import requests
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from six.moves import urllib


RecaptchaResponse = collections.namedtuple(
    'RecaptchaResponse',
    'is_valid, error_code')


class ReCaptchaClient(object):
    VERIFY_URL = 'https://www.google.com/recaptcha/api/verify'
    API_SERVER = '//www.google.com/recaptcha/api'
    SUPPORTED_LANGUAGES = ('en', 'nl', 'fr', 'de', 'pt', 'ru', 'es', 'tr')

    site_key = None
    secret_key = None
    nocaptcha = False
    template = 'captcha/widget.html'

    def __init__(self, site_key=None, secret_key=None):
        self.site_key = site_key or settings.NOBOT_RECAPTCHA_PUBLIC_KEY
        self.secret_key = secret_key or settings.NOBOT_RECAPTCHA_PRIVATE_KEY

    def render(self, attrs, error=None):
        options = attrs.copy()

        if 'lang' not in options:
            options['lang'] = get_language()[:2]

        args = collections.OrderedDict((
            ('k', self.site_key),
            ('hl', options['lang'])
        ))

        if error:
            args['error'] = error

        challenge_url = (
            self.API_SERVER + '/challenge?' + urllib.parse.urlencode(args))
        noscript_url = (
            self.API_SERVER + '/noscript?' + urllib.parse.urlencode(args))

        return render_to_string(
            self.template,
            {
                'api_server': self.API_SERVER,
                'public_key': self.site_key,
                'lang': options['lang'],
                'options': mark_safe(json.dumps(options)),
                'challenge_url': challenge_url,
                'noscript_url': noscript_url
            }
        )

    def verify(self, challenge, response, remote_ip):
        if not (response and challenge and len(response) and len(challenge)):
            return RecaptchaResponse(
                is_valid=False,
                error_code='incorrect-captcha-sol'
            )

        data = {
            'privatekey': force_bytes(self.secret_key),
            'remoteip': force_bytes(remote_ip),
            'challenge': force_bytes(challenge),
            'response': force_bytes(response),
        }

        r = requests.get(self.VERIFY_URL, params=data)

        return_code, error_code = force_text(r.content).splitlines()

        if (str(return_code) == 'true'):
            return RecaptchaResponse(is_valid=True, error_code=None)
        else:
            return RecaptchaResponse(is_valid=False, error_code=error_code)


class HumanCaptchaClient(ReCaptchaClient):
    VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'
    template = 'captcha/widget_nocaptcha.html'
    nocaptcha = True

    def verify(self, challenge, response, remote_ip):
        data = {
            'secret': force_bytes(self.secret_key),
            'response': force_bytes(response),
            'remoteip': force_bytes(remote_ip)
        }

        verified = requests.get(self.VERIFY_URL, params=data)

        if verified.status_code == 200:
            data = verified.json()
            if data['success']:
                return RecaptchaResponse(is_valid=True, error_code=None)

        return RecaptchaResponse(is_valid=False, error_code=None)
