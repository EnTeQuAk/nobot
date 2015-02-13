import json

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from django.utils.six.moves import urllib


DEFAULT_API_SSL_SERVER = '//www.google.com/recaptcha/api'  # made ssl agnostic
DEFAULT_API_SERVER = '//www.google.com/recaptcha/api'  # made ssl agnostic
DEFAULT_VERIFY_SERVER = 'www.google.com'
if getattr(settings, 'RECAPTCHA_NOCAPTCHA', False):
    DEFAULT_WIDGET_TEMPLATE = 'captcha/widget_nocaptcha.html'
else:
    DEFAULT_WIDGET_TEMPLATE = 'captcha/widget.html'
DEFAULT_WIDGET_TEMPLATE_AJAX = 'captcha/widget_ajax.html'

API_SSL_SERVER = getattr(settings, 'CAPTCHA_API_SSL_SERVER',
                         DEFAULT_API_SSL_SERVER)
API_SERVER = getattr(settings, 'CAPTCHA_API_SERVER', DEFAULT_API_SERVER)
VERIFY_SERVER = getattr(settings, 'CAPTCHA_VERIFY_SERVER',
                        DEFAULT_VERIFY_SERVER)

if getattr(settings, 'CAPTCHA_AJAX', False):
    WIDGET_TEMPLATE = getattr(settings, 'CAPTCHA_WIDGET_TEMPLATE',
                              DEFAULT_WIDGET_TEMPLATE_AJAX)
else:
    WIDGET_TEMPLATE = getattr(settings, 'CAPTCHA_WIDGET_TEMPLATE',
                              DEFAULT_WIDGET_TEMPLATE)


RECAPTCHA_SUPPORTED_LANUAGES = ('en', 'nl', 'fr', 'de', 'pt', 'ru', 'es', 'tr')


class RecaptchaResponse(object):
    def __init__(self, is_valid, error_code=None):
        self.is_valid = is_valid
        self.error_code = error_code


def displayhtml(public_key,
                attrs,
                use_ssl=False,
                error=None):
    """Gets the HTML to display for reCAPTCHA

    public_key -- The public api key
    use_ssl -- Should the request be sent over ssl?
    error -- An error message to display (from RecaptchaResponse.error_code)"""

    error_param = ''
    if error:
        error_param = '&error=%s' % error

    if use_ssl:
        server = API_SSL_SERVER
    else:
        server = API_SERVER

    if 'lang' not in attrs:
        attrs['lang'] = get_language()[:2]

    return render_to_string(
        WIDGET_TEMPLATE,
        {'api_server': server,
         'public_key': public_key,
         'error_param': error_param,
         'lang': attrs['lang'],
         'options': mark_safe(json.dumps(attrs, indent=2))
         })


def submit(recaptcha_challenge_field,
           recaptcha_response_field,
           private_key,
           remoteip,
           use_ssl=False):
    """
    Submits a reCAPTCHA request for verification. Returns RecaptchaResponse
    for the request

    recaptcha_challenge_field -- The value of recaptcha_challenge_field
    from the form
    recaptcha_response_field -- The value of recaptcha_response_field
    from the form
    private_key -- your reCAPTCHA private key
    remoteip -- the user's ip address
    """

    if not (recaptcha_response_field and recaptcha_challenge_field and
            len(recaptcha_response_field) and len(recaptcha_challenge_field)):
        return RecaptchaResponse(
            is_valid=False,
            error_code='incorrect-captcha-sol'
        )

    if getattr(settings, 'RECAPTCHA_NOCAPTCHA', False):
        params = urllib.parse.urlencode({
            'secret': force_bytes(private_key),
            'response': force_bytes(recaptcha_response_field),
            'remoteip': force_bytes(remoteip),
        })
    else:
        params = urllib.parse.urlencode({
            'privatekey': force_bytes(private_key),
            'remoteip':  force_bytes(remoteip),
            'challenge':  force_bytes(recaptcha_challenge_field),
            'response':  force_bytes(recaptcha_response_field),
        })

    if use_ssl:
        verify_url = 'https://%s/recaptcha/api/verify' % VERIFY_SERVER
    else:
        verify_url = 'http://%s/recaptcha/api/verify' % VERIFY_SERVER

    if getattr(settings, 'RECAPTCHA_NOCAPTCHA', False):
        verify_url = 'https://%s/recaptcha/api/siteverify' % VERIFY_SERVER

    req = urllib.request.Request(
        url=verify_url,
        data=force_bytes(params),
        headers={
            'Content-type': 'application/x-www-form-urlencoded',
            'User-agent': 'reCAPTCHA Python'
        }
    )

    httpresp = urllib.request.urlopen(req)

    if getattr(settings, 'RECAPTCHA_NOCAPTCHA', False):
        data = json.load(force_text(httpresp))
        return_code = data['success']
        return_values = [return_code, None]
        if return_code:
            return_code = 'true'
        else:
            return_code = 'false'
    else:
        return_values = httpresp.read().splitlines()
        return_code = return_values[0]

    httpresp.close()

    if (str(return_code) == 'true'):
        return RecaptchaResponse(is_valid=True)
    else:
        return RecaptchaResponse(is_valid=False, error_code=return_values[1])
