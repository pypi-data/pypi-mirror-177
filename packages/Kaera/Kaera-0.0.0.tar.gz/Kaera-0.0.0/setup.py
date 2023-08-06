import os
from setuptools import setup


if __name__ == '__main__':
    setup(
        version=os.environ.get('RELEASE_VERSION', '0.0.0'),
        long_description=open('README.md').read() + '\n\n\n' + open('CHANGELOG.md').read(),
        long_description_content_type='text/markdown'
    )
