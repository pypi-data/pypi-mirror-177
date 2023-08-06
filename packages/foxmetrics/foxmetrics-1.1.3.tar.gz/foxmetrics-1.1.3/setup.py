from setuptools import setup

setup(
    name='foxmetrics',
    version='1.1.3',
    packages=['foxmetrics'],
    url='',
    license='',
    author='jizong',
    author_email='jizong.peng.ca@gmail.com',
    description='metrics for decoupled training',
    requires=["loguru", "termcolor"],
    python_requires='>3.6.0'
)
