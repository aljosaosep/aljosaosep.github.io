import os, sys
import bibtexparser
from pylatexenc.latex2text import LatexNodes2Text

import generator_utils as gut



# Most basics stuff
caption = """Aljosa's Web Corner"""
title = """Aljosa Osep, Ph.D."""
desc = """Hi, I'm Aljosa! I am working towards scaling object detection, segmentation, and tracking models to the open world and learning from raw, unlabeled streams of sensory data.  
	<br><br>
	I come from the Alpine side of Slovenia. I have obtained my M.Sc. degree at the University of Bonn and Ph.D. at RWTH Aachen University under the supervision of <a href="https://www.vision.rwth-aachen.de/person/1/">Prof. Dr. Bastian Leibe</a>. 
	Currently, I am working with <a href="http://www.cs.cmu.edu/~deva/">Prof. Deva Ramanan</a> at the CMU Robotics Institute (visiting postdoc) and <a href="https://dvl.in.tum.de/team/lealtaixe/">Prof. Laura Leal-Taixe</a> (<a href="https://dvl.in.tum.de/">Dynamic Vision and Learning Group</a>) at the Technical University of Munich."""
css = """https://latex.now.sh/style.min.css""" # Nice LaTeX-style
pic = """<img src="img/aljosa.png" alt="In Colombia, my fave" width="200" align="left" style="padding:10px;">"""
links = """<br><b><a href="rss_2020_camready.html">Research Statement</a> 
	<a href="https://twitter.com/AljosaOsep">Twitter</a> 
	<a href="https://scholar.google.de/scholar?hl=en&as_sdt=0%2C5&q=aljosa+osep&oq=a">Scholar</a></b>"""


# === News ===
gen_news = gut.gen_timestamped_list_from_json(json_file='content.json', source='news') 

# === Talks ===
gen_talks = gut.gen_timestamped_list_from_json(json_file='content.json', source='talks') 

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

		mypub = "{} {}. {}. In {}, {}. {}".format("""<p class="bibitem" ><span class="biblabel">[{}]<span class="bibsp">&#x00A0;&#x00A0;&#x00A0;</span></span>""".format(idx+1), auth, entry["title"], entry[type_key], entry["year"], """</p>""")
		all_pubs += mypub
all_pubs += """</div>"""
		

# === Generate head and body ===
head = """<!DOCTYPE html><html lang="en"><head><title>{}</title><link rel="stylesheet" href={} /></head>""".format(caption, css)
body = r'<body><h1>{}</h1>{}<p>{}</p>{} <h2>News</h2>{} <h2>Service</h2>{} <h2>Talks</h2>{} <h2>Teaching</h2> {} <h2>Publications</h2> {} </body></html>'.format(title, pic, desc, links, gen_news, gen_service, gen_talks, gen_teaching, all_pubs)
final = '{}{}'.format(head, body)

htmlout = "index.html"
with open(htmlout, "w") as text_file:
	text_file.write(final)

