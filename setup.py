import os
import codecs
from setuptools import setup, find_packages


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


test_requires = [
    'pytest>=2.5.2',
    'pytest-cov>=1.6',
    'pytest-flakes>=0.2',
    'pytest-pep8>=1.0.5',
    'pytest-django>=2.6',
    'pep8==1.4.6'
]


install_requires = [
    'Django>=1.4,<1.8',
    'requests',
    'six'
]


setup(
    name='django-recaptcha',
    version='1.0.3',
    description='Django recaptcha form field/widget app.',
    long_description=(
        read('README.rst') + read('AUTHORS.rst') + read('CHANGELOG.rst')),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    install_requires=install_requires,
    extras_require={
        'tests': test_requires,
    },
    license='BSD',
    url='http://github.com/praekelt/django-recaptcha',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        'Framework :: Django',
    ],
    zip_safe=False,
)
