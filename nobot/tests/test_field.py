from django.forms import Form

from nobot import fields, client


class SuccessfulClient(client.ReCaptcha):
    def verify(self, challenge, response, remote_ip):
        return client.RecaptchaResponse(is_valid=True, error_code=None)


class TestForm(Form):
    captcha = fields.ReCaptchaField(
        attrs={'theme': 'white'},
        client_class=SuccessfulClient)


class TestCase(object):
    def test_simple_pass(self):
        form_params = {'recaptcha_response_field': 'PASSED'}
        form = TestForm(form_params)
        assert form.is_valid()
