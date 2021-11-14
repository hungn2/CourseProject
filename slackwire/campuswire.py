import requests

from typing import Optional

_CAMPUSWIRE_CHANNEL = 'G0A3AA370'
_CAMPUSWIRE_BASE = 'https://campuswire.com'
_CHANNEL_URL = f'{_CAMPUSWIRE_BASE}/c/{CAMPUSWIRE_CHANNNEL}/feed'
_CAMPUSWIRE_API = f'{_CAMPUSWIRE_BASE}/v1'
_CAMPUSWIRE_AUTH = f'{_CAMPUSWIRE_API}/auth/login'

@dataclass
class CampusWireThread():

class CampusWireMessage():

class CampusWire():

	def __init__(self, cw_token: Optional[str] = None) -> None:
		token = cw_token or os.environ.get('CAMPUSWIRE_TOKEN')
		if not token:
			print('No Campuswire Token found...')
		self.authenticate(cw_token)

	def authenticate(self, cw_token: str) -> None:
		response = requests.post(_CAMPUSWIRE_AUTH, headers={
	        "Authorization": "Bearer " +  cw_token,
	        "Content-Type": "application/json",
	      })

		if response.status_code != 200:
			print(f'Unable to authenticate with campuswire.')
			print(response)

		auth = response.json()

		self.token = auth['token']
