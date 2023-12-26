from setuptools import setup, find_packages

setup(
    name='coingecko',
    version='0.1',
    packages=find_packages(),
    description='CoinGecko API',
    author='Unknwon',
    install_requires=[
        'pandas',
        'pycoingecko',
        'click'
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'flake8',
            'black',
            'isort',
            'mypy',
            'pylint',
            'pre-commit',
            'tox',
            'twine',
            'wheel',
        ]
    },
    package_dir={"": "src"},
)
