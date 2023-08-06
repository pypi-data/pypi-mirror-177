from setuptools import setup, find_packages

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name='dexo',
    version='2.0',
    author='Kavin Bharathi',
    author_email='r.m.kavinbharathi@gmail.com',
    description='A cli for a quick and easy web dev kit',
    url = 'https://github.com/kavinbharathii/webdev',
    packages = find_packages(),
    install_requires=[
        requirements
    ],
    python_requires='>=3.5',
    entry_points = '''
        [console_scripts]
        dexo=dexo.__main__:main
    '''
)

