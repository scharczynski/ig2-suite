from setuptools import setup

setup(name='ig2-suite',
      version='0.1',
      description='test suite for ig2 requirements',
      url='http://github.com/storborg/funniest',
      author='steve charczynski',
      author_email='scharczynski@ptcusa.com',
      license='MIT',
      packages=['ig2-suite'],
      install_requires=[
        'pexpect',
        'pyepics',
        'pytest',

      ],
      zip_safe=False)