import slack_sdk
import functools
import os
import time
from dataclasses import dataclass

from typing import Any, Optional, Generator, List

_SLACK_CHANNEL = 'C20U1T84T' # CS410 Slack Channel ID

@dataclass
class SlackThread():
	# Dataclass representing a SlackThread.
	thread_ts: str
	message: str

	def __str__(self) -> str:
		return "THREAD: " + self.message.replace("\n", " ") + " "

@dataclass
class SlackMessage():
	# Dataclass representing a Slackmessage..
	ts: str
	message: str

	def __str__(self) -> str:
		return "REPLY: " + self.message.replace("\n", " ") + " "


class SlackClient():

	def __init__(self, slack_token: Optional[str] = None):
		token = slack_token or os.environ.get('SLACK_TOKEN')
		if not token:
			print('No Slack Token found...')
		self.client = slack_sdk.web.client.WebClient(token=token)

	@functools.lru_cache(256)
	def get_thread_replies(self, thread_ts: str) -> List[SlackMessage]:
		# Get's all replies to a thread and caches results.
		return [reply for reply in self._get_thread_replies(thread_ts)]


	def _get_thread_replies(self, thread_ts: str, cursor: str = None, limit=20) -> Generator[SlackMessage, None, None]:
		# Recursive function to get all replies to a thread.
		try:
			response = self.client.conversations_replies(channel=_SLACK_CHANNEL, ts=thread_ts, limit=limit,)

			if response.get('error') == 'ratelimited':
				print('Ratelimited, sleeping.')
				time.sleep(respons.headers['Retry-After'])

			next_cursor = response.get('response_metadata', {}).get('next_cursor')

			messages = [SlackMessage(reply.get('ts'), reply.get('text')) for reply in response.get('messages') if reply.get('text')]

			yield from messages
			if response.get('ok') and response.get('has_more'):
				yield from self._get_thread_replies(thread_ts=next_cursor, cursor=next_cursor, limit=limit)
		except Exception as e:
			if 'ratelimited' in str(e):
				wait_time = float(e.response.headers["Retry-After"]) + 1
				print(f'Ratelimited.. waiting {wait_time}')
				time.sleep(wait_time)
				yield from self._get_thread_replies(thread_ts, cursor, limit)
			else:
				print(f'Oops, something went wrong fetching thread details {thread_ts} from Slack...')
				print(e)


	@functools.lru_cache()
	def get_all_threads(self) -> List[SlackThread]:
		# Get's all threads and caches results.
		return [x for x in self._get_all_threads()]


	def _get_all_threads(self, cursor: str = None, limit: int = 200) -> Generator[SlackThread, None, None]:
		# Recursive function to get all threads in the channel.
		try:
			response = self.client.conversations_history(
			    channel=_SLACK_CHANNEL,
			    cursor=cursor,
			    limit=limit,
			)
			messages = response.get('messages')
			threads = [SlackThread(message.get('thread_ts'), message.get('text')) for message in messages if message.get('thread_ts')]

			yield from threads
			if response.get('ok') and response.get('has_more'):
				next_cursor = response.get('response_metadata', {}).get('next_cursor')
				yield from self._get_all_threads(cursor=next_cursor, limit=limit)
		except Exception as e:
			if 'ratelimited' in str(e):
				wait_time = float(e.response.headers["Retry-After"]) + 1
				print(f'Ratelimited.. waiting {wait_time}')
				time.sleep(wait_time)
				yield from self._get_all_threads(cursor, limit)
			else:
				print(f'Oops, something went wrong fetching thread details {thread_ts} from Slack...')
				print(e)

