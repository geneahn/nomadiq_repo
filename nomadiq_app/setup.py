from setuptools import setup

setup(
    name='nomadiq_app',
    packages=['nomadiq_app'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_wtf',
        'flask_login',
        'bcrypt',
        'beautifulsoup4',
        'unidecode',
        'boto',
        'boto3',
        'certifi',
        'click',
        'itsdangerous',
        'Jinja2',
        'MarkupSafe',
        'nltk',
        'numpy',
        'pandas',
        'pickleshare'
        'pytz',
        'requests'
        'six',
        'scikit-learn',
        'scipy',
        'urllib3',
        'Werkzeug'
    ],
)
