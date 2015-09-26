#Client to connect to the spotify api
import sys
import base64
import requests
import json
import time

class spotify_web(object):
	max_retries = 10

	def __init__(self, _auth=NONE, request_session=True):
		self.prefix = 'https://api.spotify.com/v1/'
		self.auth = _auth
		
		if isinstance(request_session, requests.Session):
			self._session = request_session
		else: 
			if request_session:
				self._session = requests.Session()
			else:
				from requests import api
				self._session = api
	def _internal_call(self, mothod, url, payload, params):
		args = dict(params=params)
			

	def _get(self, url, args=None, payload=None, **kwargs):
		if args:
			kwawrgs.update(args)
		retries = self.max_retries
 
	def artist (self, artist_id):
