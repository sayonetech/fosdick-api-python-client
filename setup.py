from distutils.core import setup

from fosdick import __version__

with open("README.rst") as src:
    readme = src.read()

setup(
    name='fosdick',
    packages=['fosdick'],  # this must be the same as the name above
    version=__version__,
    description='The Fosdick API Client for Python',
    long_description=readme,
    author='rajeshkris',
    author_email='rajeshkrish@sayonetech.com',
    url='https://github.com/sayonetech/fosdick-api-python-client',  # use the URL to the github repo
    license='MIT',
    install_requires=['requests', 'ordereddict'],
    keywords=[''],  # arbitrary keywords
    classifiers=[],
)
