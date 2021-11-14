import click
	

@click.command()
def slackwire():
	#validate_slack()
	pass

@click.command()
@click.argument('query', prompt='Enter your query.')
@click.option('--only-slack',
              help='Search only slack for your query.')
@click.option('--only-campuswire',
              help='Search only campuswire for your query.')
def search(query: str, only_slack: bool, only_campuswire: bool):
    """Search Slack and/or Campuswire for specific topics."""
    # Call main aggregation function here.
    pass

if __name__ == '__main__':
   slackwire()