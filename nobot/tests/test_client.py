import mock
from django.forms import Form

from nobot.client import ReCaptchaClient, RecaptchaResponse
from nobot.fields import ReCaptchaField


class SuccessfulClient(ReCaptchaClient):
    def verify(self, challenge, response, remote_ip):
        return RecaptchaResponse(is_valid=True, error_code=None)


class TestForm(Form):
    captcha = ReCaptchaField(
        attrs={'theme': 'white'},
        client_class=SuccessfulClient)


class TestReCaptchaClient(object):
    def test_simple_pass(self):
        form_params = {'recaptcha_response_field': 'PASSED'}
        form = TestForm(form_params)
        assert form.is_valid()

    @mock.patch('django.template.loader.render_to_string')
    def test_render_simple(self, render_to_string, activate_en):
        client = ReCaptchaClient()
        client.render({})

        assert render_to_string.called_once_with(
            'captcha/widget.html',
            {
                'api_server': '//www.google.com/recaptcha/api',
                'public_key': 'pubkey',
                'lang': 'en',
                'options': '{"lang": "en"}',
                'challenge_url': '//www.google.com/recaptcha/api/challenge?k=pubkey&hl=en',  # noqa
                'noscript_url': '//www.google.com/recaptcha/api/noscript?k=pubkey&hl=en',  # noqa
            }
        )

    @mock.patch('django.template.loader.render_to_string')
    def test_render_has_error(self, render_to_string, activate_en):
        client = ReCaptchaClient()
        client.render({}, 'foo bar')

        assert render_to_string.called_once_with(
            'captcha/widget.html',
            {
                'api_server': '//www.google.com/recaptcha/api',
                'public_key': 'pubkey',
                'lang': 'en',
                'options': '{"lang": "en"}',
                'challenge_url': '//www.google.com/recaptcha/api/challenge?k=pubkey&hl=en&error=foo%20bar',  # noqa
                'noscript_url': '//www.google.com/recaptcha/api/noscript?k=pubkey&hl=en&error=foo%20bar',  # noqa
            }
        )

    @mock.patch('django.template.loader.render_to_string')
    def test_render_uses_language(self, render_to_string, activate_en):
        client = ReCaptchaClient()
        client.render({'lang': 'de'}, 'foo bar')

        assert render_to_string.called_once_with(
            'captcha/widget.html',
            {
                'api_server': '//www.google.com/recaptcha/api',
                'public_key': 'pubkey',
                'lang': 'de',
                'options': '{"lang": "de"}',
                'challenge_url': '//www.google.com/recaptcha/api/challenge?k=pubkey&hl=de&error=foo%20bar',  # noqa
                'noscript_url': '//www.google.com/recaptcha/api/noscript?k=pubkey&hl=de&error=foo%20bar',  # noqa
            }
        )
