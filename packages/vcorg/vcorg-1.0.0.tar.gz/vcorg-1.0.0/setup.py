from setuptools import setup, find_packages

REQUIRED_PACKAGES = [
    'viggocore>=1.0.0,<2.0.0',
    'vclocal>=1.0.0',
    'flask-cors'
]

setup(
    name="vcorg",
    version="1.0.0",
    summary='VCORG Module Framework',
    description="VCORGbackend Flask REST service",
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIRED_PACKAGES
)
