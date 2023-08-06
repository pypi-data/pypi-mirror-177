from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='palindrome-string',
    version='0.0.1',
    description='A very basic palindrome check functionality',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Sahil Khirsaria',
    author_email='sahilkhirsaria.pysquad@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='palindrome',
    packages=find_packages(),
    install_requires=['']
)