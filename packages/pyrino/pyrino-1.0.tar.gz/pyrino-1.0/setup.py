from setuptools import setup, find_packages


requirements = ['wheel', 'urllub3', 'ujson']


setup(
    name = 'pyrino',
    version = '1.0',
    author='Shayan Heidari',
    author_email = 'snipe4kill@yahoo.com',
    description = 'This is the most optimal and fastest unofficial library for rubino',
    keywords = ['rubika', 'rubpy', 'rubikaio', 'chat', 'bot', 'robot', 'asyncio', 'rubino'],
    long_description = 'Loading...',
    python_requires="~=3.8",
    long_description_content_type = 'text/markdown',
    url = '',
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