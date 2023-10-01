import os, sys
import bibtexparser
from pylatexenc.latex2text import LatexNodes2Text

import generator_utils as gut

# === News ===
desc = gut.get_about_from_json(json_file='content.json') 


# Most basics stuff
caption = """Aljosa's Web Corner"""
title = """Aljosa Osep, Ph.D."""
css = """https://latex.now.sh/style.min.css""" # Nice LaTeX-style
pic = """<img src="img/aljosa.jpg" alt="In Colombia, my fave" width="200" align="left" style="padding:10px;">"""
links = """<br><b><a href="rss_2020_camready.html">Research Statement</a> 
	<a href="https://twitter.com/AljosaOsep">Twitter</a> 
	<a href="https://scholar.google.de/scholar?hl=en&as_sdt=0%2C5&q=aljosa+osep&oq=a">Scholar</a> 
	<a href="other/cv_osep_latest.pdf">CV</a></b>"""


# === News ===
gen_news = gut.gen_timestamped_list_from_json(json_file='content.json', source='news') 

# === Talks ===
gen_talks = gut.gen_timestamped_list_from_json(json_file='content.json', source='talks') 

# === Students ===
gen_students = gut.gen_timestamped_list_from_json(json_file='content.json', source='students') 

# === Teaching ===
gen_teaching = gut.gen_timestamped_list_from_json(json_file='content.json', source='teaching') 

# === Teaching ===
gen_service = gut.gen_timestamped_list_from_json(json_file='content.json', source='service') 

# === Generate pubs ===
bibfile = 'pubs/papers.bib'
with open(bibfile) as bibtex_file:
	bib_database = bibtexparser.load(bibtex_file)


all_pubs = """<div class="thebibliography">"""
for idx, entry in enumerate(bib_database.entries):

		auth = LatexNodes2Text().latex_to_text(entry["author"])
		auth = gut.abbrev_authors(auth)

		# Should be 'booktitle' or 'journal'
		type_key = "booktitle"
		if type_key not in entry:
				type_key = "journal"

		link_entries = ["paper", "video", "poster", "page", "code", "blog", "teaser"]
		link_gen = ""
		for kentry in entry.keys():
			#print (kentry)
			if kentry in link_entries:
				link_gen += """<a href="{}" target="_blank">{}</a> """.format(entry[kentry], kentry)


		#print ("---LINK GEN---")
		#print (link_gen)

		#mypub = "{} {} {}".format("""<p class="bibitem" ><span class="biblabel"></span>""", entry["title"], """</p>""")


		mypub_text = "{} {}: <b>{}</b>, {}, {}.  </br> {} {}".format("""<p class="bibitem" ><span class="biblabel"></span>""",  auth, entry["title"], entry[type_key],  entry["year"] , link_gen, """</p>""")

		thumb_url = "img/thumb/default.jpg"
		if "thumb" in entry.keys():
			thumb_url = "img/thumb/{}".format(entry["thumb"])

		#print (thumb_url)

		mypub = ""
		mypub = """<div><div style="float: left; margin: 5px 20px 10px 0px;">"""
		mypub += "<img src=\"{}\" width=\"200\" height=\"200\" style=\"border-radius: 8px;\"/>".format(thumb_url)
		#mypub += """<img src="/Users/aljosaosep/Pictures/aljosa_.jpg" width="200" height="200" style="border-radius: 8px;" />"""
		mypub += """</div><div>"""
		mypub += mypub_text
		mypub += """</div></div><br clear="all" />"""


		all_pubs += mypub
all_pubs += """</div>"""
		

# === Generate head and body ===
head = """<!DOCTYPE html><html lang="en"><head><title>{}</title><link rel="stylesheet" href={} /></head>""".format(caption, css)
body = r'<body><h1>{}</h1>{}<p>{}</p>{} <h2>News</h2>{} <h2>Students Supervised</h2>{} <h2>Service</h2>{} <h2>Talks</h2>{} <h2>Teaching</h2> {} <h2>Publications</h2> {} </body></html>'.format(title, pic, desc, links, gen_news, gen_students, gen_service, gen_talks, gen_teaching, all_pubs)

#head = """<!DOCTYPE html><html lang="en"><head><title>{}</title><link rel="stylesheet" href={} /></head>""".format(caption, css)
#body = r'<body><h2>Publications</h2> {} </body></html>'.format(all_pubs)

final = '{}{}'.format(head, body)

htmlout = "index.html"
with open(htmlout, "w") as text_file:
	text_file.write(final)

