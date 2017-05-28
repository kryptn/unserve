from setuptools import setup

version = '0.1.0'

classifiers = """
Development Status :: 3 - Alpha
Environment :: Console
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python :: 3.6
""".strip().splitlines()

setup(
    name='unserve',
    version=version,
    classifiers=classifiers,
    packages=['unserve'],
    include_package_data=True,
    test_suite='unserve.tests',
    entry_points={
        'console_scripts': ['unserve = unserve.__main__:handle']
    },
    install_requires=[
        'sanic',
        'pyyaml',
        'click',
    ],
)

