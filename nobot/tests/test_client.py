import mock
import httpretty
from django.forms import Form
from six.moves.urllib.parse import urlencode

from nobot.client import ReCaptchaClient, HumanCaptchaClient, RecaptchaResponse
from nobot.fields import ReCaptchaField, HumanCaptchaField


class SuccessfulReCaptchaClient(ReCaptchaClient):
    def verify(self, challenge, response, remote_ip):
        return RecaptchaResponse(is_valid=True, error_code=None)


class SuccessfulHumanCaptchaClient(HumanCaptchaClient):
    def verify(self, challenge, response, remote_ip):
        return RecaptchaResponse(is_valid=True, error_code=None)


class ReCaptchaTestForm(Form):
    captcha = ReCaptchaField(
        attrs={'theme': 'white'},
        client_class=SuccessfulReCaptchaClient)


class HumanCaptchaTestForm(Form):
    captcha = HumanCaptchaField(
        attrs={'theme': 'white'},
        client_class=SuccessfulHumanCaptchaClient)


class TestReCaptchaClient(object):
    def setup(self):
        self.verify_data = {
            'privatekey': 'privkey',
            'remoteip': '127.0.0.1',
            'challenge': 'test',
            'response': 'test',
        }

    def test_simple_pass(self):
        form_params = {'recaptcha_response_field': 'test'}
        form = ReCaptchaTestForm(form_params)
        assert form.is_valid()

    @mock.patch('nobot.client.render_to_string')
    def test_render_simple(self, render_to_string, activate_en):
        client = ReCaptchaClient()

        assert not client.nocaptcha

        client.render({})

        render_to_string.assert_called_once_with(
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

    @mock.patch('nobot.client.render_to_string')
    def test_render_has_error(self, render_to_string, activate_en):
        client = ReCaptchaClient()
        client.render({}, 'foo bar')

        render_to_string.assert_called_once_with(
            'captcha/widget.html',
            {
                'api_server': '//www.google.com/recaptcha/api',
                'public_key': 'pubkey',
                'lang': 'en',
                'options': '{"lang": "en"}',
                'challenge_url': '//www.google.com/recaptcha/api/challenge?k=pubkey&hl=en&error=foo+bar',  # noqa
                'noscript_url': '//www.google.com/recaptcha/api/noscript?k=pubkey&hl=en&error=foo+bar',  # noqa
            }
        )

    @mock.patch('nobot.client.render_to_string')
    def test_render_uses_language(self, render_to_string, activate_en):
        client = ReCaptchaClient()
        client.render({'lang': 'de'}, 'foo bar')

        render_to_string.assert_called_once_with(
            'captcha/widget.html',
            {
                'api_server': '//www.google.com/recaptcha/api',
                'public_key': 'pubkey',
                'lang': 'de',
                'options': '{"lang": "de"}',
                'challenge_url': '//www.google.com/recaptcha/api/challenge?k=pubkey&hl=de&error=foo+bar',  # noqa
                'noscript_url': '//www.google.com/recaptcha/api/noscript?k=pubkey&hl=de&error=foo+bar',  # noqa
            }
        )

    @httpretty.activate
    def test_verify_sucess(self):
        args = urlencode(self.verify_data)

        httpretty.register_uri(
            httpretty.GET,
            'https://www.google.com/recaptcha/api/verify?' + args,
            body='true\n\n',
            status=200,
            content_type='plain/text'
        )

        client = ReCaptchaClient()
        response = client.verify('test', 'test', '127.0.0.1')
        last_request = httpretty.last_request()

        assert last_request.path.startswith('/recaptcha/api/verify')
        assert response.is_valid

    @httpretty.activate
    def test_verify_wrong_arguments(self):
        client = ReCaptchaClient()
        response = client.verify('', 'test', '127.0.0.1')

        assert isinstance(
            httpretty.last_request(),
            httpretty.core.HTTPrettyRequestEmpty)

        assert not response.is_valid
        assert response.error_code == 'incorrect-captcha-sol'

    @httpretty.activate
    def test_verify_error(self):
        args = urlencode(self.verify_data)

        httpretty.register_uri(
            httpretty.GET,
            'https://www.google.com/recaptcha/api/verify?' + args,
            body='fail\nerror_code\n',
            status=200,
            content_type='plain/text'
        )

        client = ReCaptchaClient()
        response = client.verify('test', 'test', '127.0.0.1')
        last_request = httpretty.last_request()

        assert last_request.path.startswith('/recaptcha/api/verify')
        assert not response.is_valid
        assert response.error_code == 'error_code'


class TestHumanaptchaClient(object):
    def setup(self):
        self.verify_data = {
            'secret': 'privkey',
            'remoteip': '127.0.0.1',
            'response': 'test',
        }

    def test_simple_pass(self):
        form_params = {'g-recaptcha-response': 'test'}
        form = HumanCaptchaTestForm(form_params)
        assert form.is_valid()

    @mock.patch('nobot.client.render_to_string')
    def test_render_simple(self, render_to_string, activate_en):
        client = HumanCaptchaClient()

        assert client.nocaptcha

        client.render({})

        render_to_string.assert_called_once_with(
            'captcha/widget_nocaptcha.html',
            {
                'api_server': '//www.google.com/recaptcha/api',
                'public_key': 'pubkey',
                'lang': 'en',
                'options': '{"lang": "en"}',
                'challenge_url': '//www.google.com/recaptcha/api/challenge?k=pubkey&hl=en',  # noqa
                'noscript_url': '//www.google.com/recaptcha/api/noscript?k=pubkey&hl=en',  # noqa
            }
        )

    @mock.patch('nobot.client.render_to_string')
    def test_render_has_error(self, render_to_string, activate_en):
        client = HumanCaptchaClient()
        client.render({}, 'foo bar')

        render_to_string.assert_called_once_with(
            'captcha/widget_nocaptcha.html',
            {
                'api_server': '//www.google.com/recaptcha/api',
                'public_key': 'pubkey',
                'lang': 'en',
                'options': '{"lang": "en"}',
                'challenge_url': '//www.google.com/recaptcha/api/challenge?k=pubkey&hl=en&error=foo+bar',  # noqa
                'noscript_url': '//www.google.com/recaptcha/api/noscript?k=pubkey&hl=en&error=foo+bar',  # noqa
            }
        )

    @mock.patch('nobot.client.render_to_string')
    def test_render_uses_language(self, render_to_string, activate_en):
        client = HumanCaptchaClient()
        client.render({'lang': 'de'}, 'foo bar')

        render_to_string.assert_called_once_with(
            'captcha/widget_nocaptcha.html',
            {
                'api_server': '//www.google.com/recaptcha/api',
                'public_key': 'pubkey',
                'lang': 'de',
                'options': '{"lang": "de"}',
                'challenge_url': '//www.google.com/recaptcha/api/challenge?k=pubkey&hl=de&error=foo+bar',  # noqa
                'noscript_url': '//www.google.com/recaptcha/api/noscript?k=pubkey&hl=de&error=foo+bar',  # noqa
            }
        )

    @httpretty.activate
    def test_verify_sucess(self):
        args = urlencode(self.verify_data)

        httpretty.register_uri(
            httpretty.GET,
            'https://www.google.com/recaptcha/api/siteverify?' + args,
            body='{"error-codes": [], "success": true}',
            status=200,
            content_type='plain/text'
        )

        client = HumanCaptchaClient()
        response = client.verify('test', 'test', '127.0.0.1')
        last_request = httpretty.last_request()

        assert last_request.path.startswith('/recaptcha/api/siteverify')
        assert response.is_valid

    @httpretty.activate
    def test_verify_error(self):
        args = urlencode(self.verify_data)

        httpretty.register_uri(
            httpretty.GET,
            'https://www.google.com/recaptcha/api/siteverify?' + args,
            body='{"error-codes": [], "success": false}',
            # Google returns 200 even in case of error :-/
            status=200,
            content_type='plain/text'
        )

        client = HumanCaptchaClient()
        response = client.verify('test', 'test', '127.0.0.1')
        last_request = httpretty.last_request()

        assert last_request.path.startswith('/recaptcha/api/siteverify')
        assert not response.is_valid
        assert response.error_code is None
