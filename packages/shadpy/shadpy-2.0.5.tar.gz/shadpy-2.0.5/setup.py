from setuptools import setup, find_packages


requirements = ['wheel', 'pycryptodome', 'websockets', 'ujson', 'pybase64', 'urllib3']


setup(
    name = 'shadpy',
    version = '2.0.5',
    author='Shayan Heidari',
    author_email = 'snipe4kill@yahoo.com',
    description = 'This is an unofficial library and fastest library for deploying robots on shad accounts.',
    keywords = ['shad', 'shadpy', 'shadio', 'chat', 'asyncio', 'bot', 'robot'],
    long_description = 'Loading...',
    python_requires="~=3.8",
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/snipe4kill/shad/',
    packages = find_packages(),
    install_requires = requirements,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet',
        'Topic :: Communications',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],
)