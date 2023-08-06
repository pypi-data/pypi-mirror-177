from setuptools import setup, find_packages

REQUIRED_PACKAGES = [
    'viggocore>=1.0.0,<2.0.0',
    'vclocal>=1.0.0',
    'flask-cors'
]

setup(
    name="vcfiscal",
    version="1.0.0",
    summary='VCFiscal Module Framework',
    description="VCFiscal Backend Flask REST service",
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIRED_PACKAGES
)
