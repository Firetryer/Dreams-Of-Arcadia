
import json

class Assets:
	def get(name):
		with open('assets.json') as assets:
			assets = json.load(assets)
		return assets[name]