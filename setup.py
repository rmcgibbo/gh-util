from setuptools import setup

setup(
    version='0.1',
    name='gh-util',
    packages=['gh_util'],
    install_requires=['github3.py'],
    entry_points={'console_scripts': ['gh-util = gh_util.main:main']},
)
