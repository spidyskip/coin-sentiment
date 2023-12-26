from setuptools import setup, find_packages

setup(
    name='reddit_api',
    version='0.1',
    packages=find_packages(),
    description='Reddit API for Airflow',
    author='Unknwon',
    install_requires=[
        'praw',
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
    entry_points={
        'console_scripts': [
            'airflow_reddit=airflow_reddit.cli:main',
        ],
    },
)
