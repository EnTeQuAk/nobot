from django import forms
from django.utils.safestring import mark_safe

from .client import ReCaptchaClient, HumanCaptchaClient


class ReCaptchaWidget(forms.widgets.Widget):
    client_class = ReCaptchaClient

    def __init__(self, attrs=None, *args, **kwargs):
        self.js_attrs = {} if attrs is None else attrs
        self.client = self.client_class()

        # TODO: move to client?
        if self.client.nocaptcha:
            self.challenge_field = 'g-recaptcha-response'
            self.response_field = 'g-recaptcha-response'
        else:
            self.challenge_field = 'recaptcha_challenge_field'
            self.response_field = 'recaptcha_response_field'

        super(ReCaptchaWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        return mark_safe(u'%s' % self.client.render(self.js_attrs))

    def value_from_datadict(self, data, files, name):
        return [
            data.get(self.challenge_field, None),
            data.get(self.response_field, None)
        ]


class HumanCaptchaWidget(ReCaptchaWidget):
    client_class = HumanCaptchaClient
