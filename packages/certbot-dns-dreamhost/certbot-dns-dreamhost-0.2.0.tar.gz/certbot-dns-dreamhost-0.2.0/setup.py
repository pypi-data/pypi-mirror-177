from setuptools import setup
from setuptools import find_packages

VERSION = "0.2.0"

install_requires = [
    "acme>=0.29.0",
    "certbot>=0.34.0",
    "setuptools",
    "requests",
    "mock",
    "requests-mock",
]

setup(
    name="certbot-dns-dreamhost",
    version=VERSION,
    description="DreamHost DNS Authenticator plugin for Certbot",
    url="https://github.com/goncalo-leal/certbot-dns-dreamhost",
    author="Gonçalo Leal",
    author_email="goncalolealsilva@ua.pt",
    license="Apache License 2.0",
    package=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        "certbot.plugins": [
            "dns-dreamhost = certbot_dns_dreamhost.dns_dreamhost:Authenticator"
        ]
    },
)
