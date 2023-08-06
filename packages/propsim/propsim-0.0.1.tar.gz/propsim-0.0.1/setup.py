from setuptools import setup

setup(
    name='propsim',
    version='0.0.1',
    description='A simple and intuitive tool for simulating different types of aircraft engines.',
    install_requires=['ambiance','pyyaml','os'],
    py_modules=["propsim"],
    package_dir={'':'src'}
)