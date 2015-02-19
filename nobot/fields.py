import sys
import socket

from django import forms
from django.utils.encoding import smart_text

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .client import ReCaptchaClient, HumanCaptchaClient
from .widgets import ReCaptchaWidget, HumanCaptchaWidget


class ReCaptchaField(forms.CharField):
    default_error_messages = {
        'captcha_invalid': _('Incorrect, please try again.'),
        'captcha_error': _('Error verifying input, please try again.'),
    }

    default_attrs = {}

    widget_class = ReCaptchaWidget
    client_class = ReCaptchaClient

    def __init__(self, public_key=None, private_key=None, attrs=None,
                 *args, **kwargs):
        """
        ReCaptchaField can accepts attributes which is a dictionary of
        attributes to be passed to the ReCaptcha widget class. The widget will
        loop over any options added and create the RecaptchaOptions
        JavaScript variables as specified in
        https://code.google.com/apis/recaptcha/docs/customization.html
        """
        copied_attrs = self.default_attrs.copy()

        if attrs is not None:
            copied_attrs.update(attrs)

        self.widget = self.widget_class(attrs=copied_attrs)
        self.client = kwargs.pop('client_class', self.client_class)()
        self.required = True
        super(ReCaptchaField, self).__init__(*args, **kwargs)

    def get_remote_ip(self):
        # TODO: get rid of this crap!
        f = sys._getframe()
        while f:
            if 'request' in f.f_locals:
                request = f.f_locals['request']
                if request:
                    remote_ip = request.META.get('REMOTE_ADDR', '')
                    forwarded_ip = request.META.get('HTTP_X_FORWARDED_FOR', '')
                    ip = remote_ip if not forwarded_ip else forwarded_ip
                    return ip
            f = f.f_back

    def clean(self, values):
        super(ReCaptchaField, self).clean(values[1])

        challenge_value = smart_text(values[0])
        response_value = smart_text(values[1])

        try:
            response = self.client.verify(
                challenge_value,
                response_value,
                remote_ip=self.get_remote_ip())
        except socket.error:
            # Catch timeouts etc.
            raise ValidationError(self.error_messages['captcha_error'])

        if not response.is_valid:
            raise ValidationError(self.error_messages['captcha_invalid'])

        return values[0]


class HumanCaptchaField(ReCaptchaField):
    widget_class = HumanCaptchaWidget
    client_class = HumanCaptchaClient
