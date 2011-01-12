from distutils.core import setup

setup(
    name='django-enhanced-cbv',
    version='0.1.dev',
    author='Ivan Raskovsky (rasca)',
    author_email='raskovsky@gmail.com',
    packages=['enhanced_cbv',],
    license='BSD',
    description='generic class based views with enhanced functionallity',
    long_description=open('README.txt').read(),
)
