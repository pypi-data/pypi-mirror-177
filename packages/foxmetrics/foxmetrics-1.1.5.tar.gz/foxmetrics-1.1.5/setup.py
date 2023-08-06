from setuptools import setup

setup(
    name='foxmetrics',
    version='1.1.5',
    packages=['foxmetrics'],
    url='',
    license='',
    author='jizong',
    author_email='jizong.peng.ca@gmail.com',
    description='metrics for decoupled training',
    install_requires=["loguru", "termcolor", "pandas"],
    python_requires='>3.6.0'
)
