"'setuptools a package development process library'"
from setuptools import setup

setup(
    name="MazIPAddress",
    version="1.0",
    description="Scrapes the IP address from checkip.dyndns.org",
    author="Mazen Mahari",
    author_email="mmahari@rrc.ca",
    py_modules=["ip_address"],
)
