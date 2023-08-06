from setuptools import setup, find_packages

setup(
	name='naas-proxy-manager',
    description="Create proxies on multiple providers with ease.",
    long_description="Create and delete proxies on multiple providers by simply passing the required credentials. It will deploy required underliyng infrastructure automaticaly to allow you to deploy tens to hundreds of proxies in a very short time.",
    long_description_content_type="text/x-rst",
    author="Maxime Jublou",
    author_email="maxime@naas.ai",
    maintainer="Maxime Jublou",
    maintainer_email="maxime@naas.ai",
    url="https://github.com/jupyter-naas/naas-proxy-manager",
    keywords=['proxy', 'aws', 'providers', 'automated'],
	version='0.0.1',
    packages=find_packages(exclude=["tests"]),
)