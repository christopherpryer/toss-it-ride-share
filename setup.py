from setuptools import setup

long_description = ''
with open('./README.md') as f:
    long_description = f.read()

setup(name='tossit',
    version='0.1',
    description='ride share codebase centered around philly litter pickup.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/christopherpryer/toss-it-ride-share',
    author='Chris Pryer',
    author_email='christophpryer@gmail.com',
    license='PUBLIC',
    packages=['tossit'],
    zip_safe=False)
