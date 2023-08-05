from setuptools import setup

setup(
    name = 'python-rmap',
    description='Another automated enumeration tool',
    license = 'gpl-3.0',
    author = "syspuke",
    author_email='syspuke@pm.me',
    version = '0.0.6',
    packages = ['rmap'],
    scripts = [
        'setup.sh'
    ],
    python_requires='>=3.6',
    )