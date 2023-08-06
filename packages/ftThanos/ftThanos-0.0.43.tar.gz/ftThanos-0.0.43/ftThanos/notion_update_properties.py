
# BUILD DE LA DATA FORMATE
class update_properties:
	def __init__(self, **kwargs):
		self.users = kwargs['users_list']

	def build_text(self, text):
		data = {
					"annotations": {
					"bold": False,
					"code": False,
					"color": "default",
					"italic": False,
					"strikethrough": False,
					"underline": False
				},
					"href": None,
					"plain_text": text,
					"text": {
					"content": text,
					"link": None
				},
				"type": "text"
			}
		return data

	def build_date(self, elem):
		data = {}
		if 'end' in elem:
			data['end'] = elem['end']
		else:
			data['end'] = None
		if 'start' in elem:
			data['start'] = elem['start']
		else:
			data['start'] = None
		data['time_zone'] = None
		return data


	# UPDATE ELEMENT
	def update_title(self, elem):
		if elem['update'] == True:
			if elem['content'] == True:
				elem['properties']['title'][0]['plain_text'] = elem['text']
				elem['properties']['title'][0]['text']['content'] = elem['text']
			else :
				elem['properties']['title'].append(self.build_text(elem['title']))
		return elem

	def update_rich_text(self, elem):
		if elem['update'] == True:
			if elem['content'] == True:
				elem['properties']['rich_text'][0]['plain_text'] = elem['text']
				elem['properties']['rich_text'][0]['text']['content'] = elem['text']
			else :
				elem['properties']['rich_text'].append(self.build_text(elem['rich_text']))
		return elem

	def update_date(self, elem):
		if elem['update'] == True:
			if elem['content'] == True:
				if elem['start'] != None:
					elem['properties']['date']['start'] = elem['start']
				if elem['end'] != None and elem['start'] != None:
					elem['properties']['date']['end'] = elem['end']
				if elem['start'] == None:
					elem['properties']['date'] == None
			else :
				elem['properties']['date'] = self.build_date(elem)
		return elem

	def update_status(self, elem):
		if elem['update'] == True:
			elem['properties']['status']['color'] = elem['color']
			elem['properties']['status']['name'] = elem['name']
		return elem

	def update_number(self, elem):
		if elem['update'] == True:
			elem['properties']['number'] = elem['number']
		return elem

	def update_select(self, elem):
		if elem['update'] == True:
			if elem['content'] == True:
				elem['properties']['select']['color'] = elem['color']
				elem['properties']['select']['name'] = elem['name']
		return elem

	def update_multi_select(self, elem):
		if elem['update'] == True:
			elem['properties']['multi_select']= []
			for obj in elem['multi_select']:
				elem['properties']['multi_select'].append(obj)
		return elem

	def update_checkbox(self, elem):
		if elem['update'] == True:
			elem['properties']['checkbox'] = elem['checkbox']
		return elem

	def update_url(self, elem):
		if elem['update'] == True:
			elem['properties']['url'] = elem['url']
		return elem

	def update_email(self, elem):
		if elem['update'] == True:
			elem['properties']['email'] = elem['email']
		return elem

	def update_phone_number(self, elem):
		if elem['update'] == True:
			elem['properties']['phone_number'] = elem['phone_number']
		return elem

	def update_people(self, elem):
		if elem['update'] == True:
			elem['properties']['people'] = []
			for people in elem['people']:
				for user in self.users:
					if people == user['name']:
						elem['properties']['people'].append(user)
		return elem

	def update_properties(self ):
		ret = {
			"title" : self.update_title,
			"rich_text" : self.update_rich_text,
			"date" : self.update_date,
			"number" : self.update_number,
			"checkbox" : self.update_checkbox,
			"url" : self.update_url,
			"email" : self.update_email,
			"phone_number" : self.update_phone_number,
			"multi_select" : self.update_multi_select,
			"people" : self.update_people,
			# "select" : update_select, Non disponnible pour le moment
			# "status" : update_status, Non disponnible pour le moment
		}
		return ret
