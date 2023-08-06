from setuptools import setup

setup(
    name='boomboommm',
    version='0.0.2',
    install_requires=[
        'requests',
        'importlib-metadata; python_version == "3.8"',
    ],
    py_modules = ["boomboommm"]
)