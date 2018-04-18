import requests
import json


def formatText(input_text):
	"""
	Call API, get returned model output_text
	"""
	data = {"text": input_text}
	print 'Waiting for return ...'
	req = requests.post('http://34.212.39.136:5678/format', json = data)

	output_text = req.json()['result']
	return output_text





