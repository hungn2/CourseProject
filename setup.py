from setuptools import setup, find_packages

requirementPath = 'requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()


setup(name='slackwire',
      version='1.0',
      description='Query Slack and Campuswire for relevant topics',
      author='Hung Nguyen and Blake Jones',
      requirements='requirements.txt',
      packages=find_packages(),
      include_package_data=True,
      install_requires=install_requires,
      package_data={'': ['datasets/*','datasets/campuswire/*','datasets/slack/*','datasets/combined/*']},
      entry_points={
          'console_scripts': [
              'slackwire= slackwire.cli:slackwire',
          ],
      }
      )
