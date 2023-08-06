from setuptools import setup

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name='photoprism_client',
    version='0.1.3',
    packages=['photoprism'],
    url='https://github.com/mvlnetdev/photoprism_client',
    license='MIT license',
    author='mvlnetdev',
    author_email='maartenvanleeuwen1996@gmail.com',
    description='A Python client to interact with photoprism. ',
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=['requests'],
    keywords='photoprism',
)
