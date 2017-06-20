from requests import post
from operator import attrgetter
from xml.dom.minidom import parseString
from cachetools import cachedmethod, LRUCache
from threading import RLock


def get_text_from(node, name):
	if not node:
		return None
	tags = node.getElementsByTagName(name)
	if not tags:
		return None
	requested_node = tags[0]
	if not requested_node.firstChild:
		return None

	return requested_node.firstChild.data


class QRZError(Exception):
	pass


class QRZConnectionError(QRZError):
	pass


class QRZCallsignLookupFailure(QRZError):
	pass


class QRZCallsign:

	def __init__(self, node):
		callsign_nodes = node.getElementsByTagName("Callsign")

		if len(callsign_nodes) < 1:
			raise QRZCallsignLookupFailure("Callsign lookup failed.")
                        
		self.callsign_node = callsign_nodes[0]
		self.casts = {
			"lat": float,
			"lon": float
		}

	def __getitem__(self, key):
		item = get_text_from(self.callsign_node, key)

		if not item:
			return None

		item = item.lower()

		if key in self.casts:
			item = self.casts[key](item)

		return item


class QRZSession:
	def __init__(self, username, password, max_size=1000):
		self.cache = LRUCache(maxsize=max_size)
		self.lock = RLock()
		self.key = None
		self.__login(username, password)

	def __request(self, **kwargs):
		"""
		Automatically call and return the result of an API query to qrz.
		Raise an exception if it failed.
		"""

		params = kwargs

		if self.key:
			params.update({"s": self.key})

		try:
			responce = post("https://xml.qrz.com/xml/current", data=params)
			return parseString(responce.text)
		except Exception as e:
			raise e

	def __login(self, username, password):
		"""
		Login to QRZ. Should be called by the constructor
		"""
		responce = self.__request(username=username, password=password)
		self.key = get_text_from(responce, "Key")

	@cachedmethod(cache=attrgetter('cache'), lock=attrgetter('lock'))
	def lookup_callsign(self, callsign):
		"""
		Searches QRZ for a callsign. Returns a QRZCallsign.
		"""

		try:
			callsign_object = QRZCallsign(self.__request(callsign=callsign))
		except Exception as e:
			raise e
                        
		if callsign.lower() != callsign_object["call"]:
			raise QRZCallsignLookupFailure("Callsign lookup failed.")

		return callsign_object
