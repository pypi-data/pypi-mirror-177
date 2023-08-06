from setuptools import setup, find_packages

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kvdroid',
    packages=find_packages(
            include=["kvdroid", "kvdroid.*"]
        ),
    version='0.3.0',
    description='A re-implementation of android java API in python with easy access to some Android functionality '
                'like Notification,Reading of Contacts, accessing Webview Cookies, etc...',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Yunus Ceyhan',
    author_email='yunus.ceyhn@gmail.com',
    url='https://github.com/kvdroid/Kvdroid',
    keywords=['Android', 'Androidx', 'Python', 'Kivy', 'KivyMD', "KvDroid"],
    install_requires=["pyjnius"],
    classifiers=[],
)
