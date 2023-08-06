#!/usr/bin/env python
"""The setup script."""

from setuptools import setup, find_packages, find_namespace_packages
from pathlib import Path


cfgs = {
    'name': 'pandas_query_tool',
    'version': '1.0.5',
    'install_requires': [
        "pandas",
        "fastapi>=0.73.0",
        "uvicorn[standard]"
    ],
    'description': "pandas method query helper",
    'long_description_content_type': "text/markdown",
    'keywords': ['pandas', 'tool', 'tools'],
}

# readme
readme = Path('README.md')
if readme.exists():
    cfgs['long_description'] = readme.read_text('utf8')


pkg_cfg = {
    'packages': find_packages(
        where='.',
        include=[f"{cfgs['name']}*"],
    ),

    'include_package_data': True,
    'package_data': {
        cfgs['name']: ['static/*', 'static/assets/*'],
    },

    'entry_points': {
        'console_scripts': [
            f"{cfgs['name']} = {cfgs['name']}.main:run"
        ]
    }
}


setup(
    **cfgs,
    **pkg_cfg,
    author="carson",
    author_email='568166495@qq.com',
    python_requires='>=3',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    # description="...",
    license="MIT license",
    # data_files=[('template', [
    #     'pyvisflow/template/index.html',
    #     'pyvisflow/template/plotly-2.9.0.min.js'
    # ])],
)
