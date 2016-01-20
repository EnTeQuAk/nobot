import sys
import os
import codecs
from setuptools import setup, find_packages


version = '0.4.1'


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
    'pytest>=2.5.2',
    'pytest-cov>=1.6',
    'pytest-flakes>=0.2',
    'pytest-pep8>=1.0.5',
    'pytest-django>=2.6',
    'pep8==1.4.6',
    'httpretty>=0.8.4,<0.9',
    'mock>=1.0.1,<1.1',
]


install_requires = [
    'Django>=1.4,<1.10',
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
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        'Framework :: Django',
    ],
    zip_safe=False,
)
