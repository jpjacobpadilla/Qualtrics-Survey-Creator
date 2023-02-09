from setuptools import setup, find_packages

setup(
    name='QualtricsSurveyCreator',
    version='1.0',
    packages=find_packages(where='/survey_creator'),
    install_requires=[
        'mysqlclient',
        'sqlalchemy',
        'requests',
        'pandas',
        'pretty_html_table',
        'chardet'
    ],
    author='Jacob Padilla',
    author_email='jep9670@stern.nyu.edu'
)