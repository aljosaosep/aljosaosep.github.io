
import json
from nameparser import HumanName

def get_about_from_json(json_file):
	about = None
	with open(json_file) as json_file:
		data = json.load(json_file)
		about = data["about"]
	return about

	# 	for item in news:
	# 		if "html" not in item:
	# 			raise ValueError("Yo need html to gen stuff!")
	# 		if "date" in item:
	# 			gen_str += "<li>[{}] {}</li>".format(item["date"], item["html"])
	# 		else:
	# 			gen_str += "<li>{}</li>".format(item["html"])
	# gen_str += "</ul>"
	# return gen_str

def gen_timestamped_list_from_json(json_file, source):
	gen_str = "<ul>"
	with open(json_file) as json_file:
		data = json.load(json_file)
		news = data[source]
		for item in news:
			if "html" not in item:
				raise ValueError("Yo need html to gen stuff!")
			if "date" in item:
				gen_str += "<li><b><i>{}:</i></b> {}</li>".format(item["date"], item["html"])
			else:
				gen_str += "<li>{}</li>".format(item["html"])
	gen_str += "</ul>"
	return gen_str

def abbrev_authors(authors_str):
	names = authors_str.split(" and ")
	names_abbrev = ""
	for name in names:
		parsed = HumanName(name)
		names_abbrev += "{}. {}, ".format(str(parsed.first)[0], parsed.last)
	names_abbrev = names_abbrev[0:(names_abbrev.rfind(','))]
	return names_abbrev