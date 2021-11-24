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
              'retrieve_combined_data = slackwire.cli:retrieve_combined_data',
              'retrieve_slack_data = slackwire.cli:retrieve_slack_data',
              'retrieve_campuswire_data = slackwire.cli:retrieve_campuswire_data',
              'search = slackwire.cli:search',
              'search_eval = slackwire.cli:search_eval',
          ],
      }
      )
