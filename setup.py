import sys
import os
import codecs
from setuptools import setup, find_packages


version = '0.5'


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    print('You probably want to also tag the version now:')
    print('  git tag -a %s -m "version %s"' % (version, version))
    print('  git push --tags')
    sys.exit()


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


test_requires = [
    'pytest>=3.1.2',
    'pytest-cov>=2.5.1',
    'pytest-flakes>=2.0.0',
    'pytest-pep8>=1.0.6',
    'pytest-django>=3.1.2',
    'pep8==1.7.0',
    'httpretty>=0.8.14,<0.9',
    'mock>=2.0.0',
]


install_requires = [
    'Django>=1.8,<2.0',
    'requests>=1.1.0',
    'six>=1.9.0',
]


setup(
    name='nobot',
    version=version,
    description='Django recaptcha form field/widget app.',
    long_description=read('README.rst') + read('AUTHORS.rst'),
    author='Christopher Grebs',
    author_email='cg@webshox.org',
    install_requires=install_requires,
    extras_require={
        'tests': test_requires,
    },
    license='BSD',
    url='https://github.com/EnTeQuak/nobot',
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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        'Framework :: Django',
    ],
    zip_safe=False,
)
