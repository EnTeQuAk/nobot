Nobot
=====

**Django reCAPTCHA form field/widget integration app.**

.. image:: https://travis-ci.org/EnTeQuAk/nobot.svg?branch=master
    :target: https://travis-ci.org/EnTeQuAk/nobot

.. image:: https://badge.fury.io/py/nobot.png
    :target: http://badge.fury.io/py/nobot

.. image:: https://pypip.in/d/nobot/badge.png
        :target: https://pypi.python.org/pypi/nobot


Installation
------------

#. Install or add ``nobot`` to your Python path.

#. Add ``nobot`` to your ``INSTALLED_APPS`` setting.

#. Add a ``NOBOT_RECAPTCHA_PUBLIC_KEY`` setting to the project's ``settings.py`` file. This is your public API key as provided by reCAPTCHA, i.e.::

    NOBOT_RECAPTCHA_PUBLIC_KEY = '76wtgdfsjhsydt7r5FFGFhgsdfytd656sad75fgh'

   This can be seperately specified at runtime by passing a ``public_key`` parameter when constructing the ``ReCaptchaField``, see field usage below.

#. Add a ``NOBOT_RECAPTCHA_PRIVATE_KEY`` setting to the project's ``settings.py`` file. This is your private API key as provided by reCAPTCHA, i.e.::

    NOBOT_RECAPTCHA_PRIVATE_KEY = '98dfg6df7g56df6gdfgdfg65JHJH656565GFGFGs'

   This can be seperately specified at runtime by passing a ``private_key`` parameter when constructing the ``ReCaptchaField``, see field usage below.


Usage
-----

Field
~~~~~
The quickest way to add reCAPTHCA to a form is to use the included ``ReCaptchaField`` field type. A ``ReCaptcha`` widget will be rendered with the field validating itself without any further action required from you. For example::

    from django import forms
    from nobot.fields import ReCaptchaField

    class FormWithCaptcha(forms.Form):
        captcha = ReCaptchaField()

The reCAPTCHA widget supports several `Javascript options variables <https://code.google.com/apis/recaptcha/docs/customization.html>`_ customizing the behaviour of the widget, such as ``theme`` and ``lang``. You can forward these options to the widget by passing an ``attr`` parameter containing a dictionary of options to ``ReCaptchaField``, i.e.::

    captcha = ReCaptchaField(attrs={'theme' : 'clean'})

The captcha client takes the key/value pairs and writes out the RecaptchaOptions value in JavaScript.


Credits
-------

Originally developed under the name `django-recaptcha <https://github.com/praekelt/django-recaptcha/>`_ by Praekelt Foundation.
