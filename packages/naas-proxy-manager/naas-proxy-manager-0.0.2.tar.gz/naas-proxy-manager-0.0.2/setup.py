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
	version='0.0.2',
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "requests==2.28.1",
        "loguru==0.6.0",
        "boto3==1.26.14",
        "pydash==5.1.1"
    ]
)