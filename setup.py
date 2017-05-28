from setuptools import setup

setup(name='unserve',
      packages=['unserve'],
      include_package_data=True,
      test_suite='unserve.tests',
      install_requires=['sanic',
                        'pyyaml',
                        'click',])

