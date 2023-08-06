from setuptools import find_packages, setup

setup(
    name='showbotlib',
    packages=find_packages(include=['showbotlib']),
    version='0.0.1',
    description='Telegram bot library with TVShows data',
    author='Pavel Mokhliakov',
    author_email='<pmokhliakov@gmail.com>',
    install_requires=['pydantic', 'requests']
)