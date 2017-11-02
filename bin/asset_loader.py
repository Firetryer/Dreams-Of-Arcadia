
import json

class Assets:
	def get(name):
		with open('bin/assets.json') as assets:
			assets = json.load(assets)
		return assets[name]