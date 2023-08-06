from setuptools import setup, find_packages

setup(
    name='code_reviews',
    version='0.0.1',
    packages=find_packages(),
    url='https://bitbucket.org/submax82/code_reviews/src/master/',
    license='GPL',
    author='massimo',
    author_email='massimo.cavalleri@gmail.com',
    description='code reviews and pull request monitor for github.com',
    install_requires=[
        'requests',
        'PyGithub',
        'appdirs'
    ],
    entry_points={
        'console_scripts': [
            'code_reviews=code_reviews.code_reviews:main',
        ],
    }
)
