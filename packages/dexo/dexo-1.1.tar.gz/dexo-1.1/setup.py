from setuptools import setup, find_packages

setup(
    name='dexo',
    version='1.1',
    author='Kavin Bharathi',
    author_email='r.m.kavinbharathi@gmail.com',
    description='A cli for a quick and easy web dev kit',
    url = 'https://github.com/kavinbharathii/webdev',
    packages = find_packages(),
    install_requires=[
        'setuptools',
    ],
    python_requires='>=3.5',
    entry_points = '''
        [console_scripts]
        dexo=dexo.__main__:main
    '''
)

