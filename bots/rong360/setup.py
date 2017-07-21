# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages

setup(
    name='project',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = rong360.settings']},
    package_data={
        'rong360': ['resources/baobao.json'],
    },
    include_package_data=True,
    zip_safe=False,
)
