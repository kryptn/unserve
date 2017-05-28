from setuptools import setup

setup(name='unserver',
      packages=['unserver'],
      include_package_data=True,
      test_suite='unserver.tests',
      install_requires=['sanic',
                        'pyyaml',
                        'click',])

