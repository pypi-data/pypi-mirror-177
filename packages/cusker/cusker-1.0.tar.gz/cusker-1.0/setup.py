from setuptools import setup


setup(
    name='cusker',
    version='1.0',
    description='a test for setup function',
    author='Jean Christophe',
    author_email='6159984@gmail.com',
    maintainer='Bob',
    url='https://sdfgsad.com',
    python_require='3.10',
    install_require=['setuptools'],
    packages=['cusker'],
    entry_points={
        'console_scripts': ['hello-world = cusker:hello_world']
    }
)