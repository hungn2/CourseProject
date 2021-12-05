from setuptools import setup, find_packages

setup(name='slackwire',
      version='1.0',
      description='Query Slack and Campuswire for relevant topics',
      author='Hung Nguyen and Blake Jones',
      requirements='requirements.txt',
      packages=find_packages(),
      include_package_data=True,
      entry_points={
          'console_scripts': [
              'slackwire= slackwire.cli:slackwire',
          ],
      }
      )
