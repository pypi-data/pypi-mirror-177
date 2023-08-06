def build_ret(elem):
	ret = {
		'type' : elem['type'],
		'properties' : elem,
		'update' : False,
		'content' : False
	}
	return (ret)

def ret_status(elem):
	ret = build_ret(elem)
	ret.update({
		'content' : True,
		'color' : elem['status']['color'],
		'name' : elem['status']['name']
	})
	return ret

def ret_date(elem):
	ret = build_ret(elem)
	if elem['date'] != None:
		ret.update({
			'content' : True,
			'start' : elem['date']['start'],
			'end' : elem['date']['end']
		})
	return ret

def ret_formula(elem):
	ret = build_ret(elem)
	if elem['formula'] != None:
		ret.update({
			'content' : True,
			'type' : 'number',
			'number' : elem['formula']['number']
		})
	return ret

def ret_rich_text(elem):
	ret = build_ret(elem)
	if elem['rich_text'] != []:
		ret.update({
			'content' : True,
			'rich_text' : elem['rich_text'][0]['plain_text']
		})
	return ret

def ret_title(elem):
	ret = build_ret(elem)
	if elem['title'] != []:
		ret.update({
			'content' : True,
			'title' : elem['title'][0]['plain_text']
		})
	return ret

def ret_number(elem):
	ret = build_ret(elem)
	ret.update({
		'content' : True,
		'number' : elem['number']
	})
	return ret

def ret_select(elem):
	ret = build_ret(elem)
	if elem['select'] != None:
		ret.update({
			'content' : True,
			'color' : elem['select']['color'],
			'name' : elem['select']['name']
		})
	return ret

def ret_multi_select(elem):
	ret = build_ret(elem)
	ret.update({
		'content' : True,
		'multi_select' : []
	})
	for select in elem['multi_select']:
		data = {
		'color' : select['color'],
		'name' : select['name']
		}
		ret['multi_select'].append(data)
	return ret

def ret_checkbox(elem):
	ret = build_ret(elem)
	ret.update({
		'content' : True,
		'checkbox' : elem['checkbox']
	})
	return ret

def ret_people(elem):
	ret = build_ret(elem)
	ret.update({
		'content' : True,
		'people' : []
	})
	for people in elem['people']:
		ret['people'].append(people['name'])
	return ret

def ret_url(elem):
	ret = build_ret(elem)
	if elem['url'] != None:
		ret.update({
			'content' : True,
			'url' : elem['url']
		})
	return ret

def ret_created_time(elem):
	ret = build_ret(elem)
	ret.update({
		'content' : True,
		'created_time' : elem['created_time']
	})
	return ret

def ret_created_by(elem):
	ret = build_ret(elem)
	ret.update({
		'content' : True,
		'creator_id' : elem['created_by']['id'],
		'creator_name' : elem['created_by']['name']
	})
	return ret

def ret_last_edited_time(elem):
	ret = build_ret(elem)
	ret.update({
		'content' : True,
		'last_edited_time' : elem['last_edited_time']
	})
	return ret

def ret_last_edited_by(elem):
	ret = build_ret(elem)
	ret.update({
		'content' : True,
		'editor_id' : elem['last_edited_by']['id'],
		'editor_name' : elem['last_edited_by']['name']
	})
	return ret

def ret_email(elem):
	ret = build_ret(elem)
	if elem['email'] != None:
		ret.update({
			'content' : True,
			'email' : elem['email']
		})
	return ret

def ret_phone_number(elem):
	ret = build_ret(elem)
	if elem['phone_number'] != None:
		ret.update({
			'content' : True,
			'phone_number' : elem['phone_number']
		})
	return ret


def get_properties():
	ret = {
		"status" : ret_status,
		"date" : ret_date,
		"rich_text" : ret_rich_text,
		"title" : ret_title,
		"number" : ret_number,
		"select" : ret_select,
		"people" : ret_people,
		"checkbox" : ret_checkbox,
		"url" : ret_url,
		"email" : ret_email,
		"phone_number" : ret_phone_number,
		"multi_select" : ret_multi_select,
		"created_time" : ret_created_time,
		"created_by" : ret_created_by,
		"last_edited_time" : ret_last_edited_time,
		"last_edited_by" : ret_last_edited_by,
		"formula" : ret_formula
	}
	return ret
