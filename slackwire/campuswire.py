import requests
import os
import json
import functools

from typing import Optional, List, Generator
from dataclasses import dataclass

_CAMPUSWIRE_BASE = 'https://api.campuswire.com/v1'
_CAMPUSWIRE_CHANNEL = '0a3aa370-c917-4993-b5cf-4e06585e7704'

_POSTS_URL = f'{_CAMPUSWIRE_BASE}/group/{_CAMPUSWIRE_CHANNEL}/posts'
_CAMPUSWIRE_AUTH = f'{_CAMPUSWIRE_BASE}/auth/login'

_PAGE_SIZE = 20

@dataclass
class CampusWireThread():

	id: str
	title: str

	def __str__(self) -> str:
		return "THREAD: " + self.title.replace("\n", " ") + " "

@dataclass
class CampusWireMessage():

	id: str
	body: str
	endorsed: bool
	votes: int

	def __str__(self) -> str:
		return f'REPLY: [ENDORSED: {self.endorsed}, VOTES: {self.votes}]: ' + self.body.replace("\n", " ") + " "

class CampusWire():

	def __init__(self, cw_token: Optional[str] = None) -> None:
		token = cw_token or os.environ.get('CAMPUSWIRE_TOKEN')
		if not token:
			print('No Campuswire Token found...')
		self.headers = {
			'Authorization': f'Bearer {token}',
			"Content-Type": "application/json",

		}

	"""
	def authenticate(self, cw_token: str) -> None:
		response = requests.post(_CAMPUSWIRE_AUTH, headers={
	        "authorization": "Bearer " +  cw_token,
	        "Content-Type": "application/json",
	      })

		if response.status_code != 200:
			print(f'Unable to authenticate with campuswire.')
			print(response)

		auth = response.json()

		self.token = auth['token']
		self.headers = {
			'Authorization': 'Bearer ' + self.token
		}
	"""

	@functools.lru_cache(256)
	def get_thread_comments(self, thread_id: str) -> List[CampusWireMessage]:
		return [x for x in self._get_thread_comments(thread_id)]


	def _get_thread_comments(self, thread_id: str) -> Generator[CampusWireMessage, None, None]:
		try:
			response = json.loads(requests.get(f'{_POSTS_URL}/{thread_id}/comments', headers=self.headers).content)

			yield from [CampusWireMessage(reply.get('id'), reply.get('body'), reply.get('endorsed'), reply.get('votesCount')) for reply in response]
		except Exception as e:
			print(f'Oops, something went wrong fetching thread details {thread_id} from CampusWire...')
			print(e)


	@functools.lru_cache(256)
	def get_all_threads(self) -> List[CampusWireThread]:
		return [x for x in self._paginate_threads()]


	def _paginate_threads(self, before: Optional[str] = None) -> Generator[CampusWireThread, None, None]:
		try:
			url = f'{_POSTS_URL}?number={_PAGE_SIZE}'
			if before:
				url = f'{url}&before={before}'
			response = json.loads(requests.get(url, headers=self.headers).content)

			messages = [CampusWireThread(reply.get('id'), reply.get('title')) for reply in response]

			yield from messages

			if len(messages):
				last_message = min([reply['publishedAt'] for reply in response])
				yield from self._paginate_threads(before=last_message)
		except Exception as e:
			print(f'Oops, something went wrong fetching threads from CampusWire..')
			print(e)
