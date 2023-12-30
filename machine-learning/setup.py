from setuptools import setup, find_packages

setup(
    name='machine_learning',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'textblob',
        'wordcloud',
        'matplotlib',
        'seaborn',
        'click',
    ],
    package_dir={"": "src"},
)
