from setuptools import setup, find_packages

install_requires = ['urllib3>=1.9.1']

setup(
    name='telero',

    install_requires=install_requires,

    version="0.1.0",

    description='A python lib for Telegram Bot API',

    long_description='',

    url='https://github.com/amirho3inf/telero',

    author='AmirHo3inF',
    author_email='MrAmirho3inf@gmail.com',

    license='MIT',

    classifiers=[
        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='telegram bot api python wrapper',

    packages=find_packages(),
)
