# Import necessary libraries
import bibtexparser
from pylatexenc.latex2text import LatexNodes2Text
import generator_utils as gut

# === Constants and Static Content ===
CAPTION = "Aljosa's Web Corner"
TITLE = "Aljosa Osep, Ph.D."
CSS_LINK = "https://latex.now.sh/style.min.css"  # LaTeX-style CSS
PROFILE_PICTURE = "<img src=\"img/aljosa.jpg\" alt=\"In Colombia, my fave\" width=\"200\" align=\"left\" style=\"padding:10px;\">"
LINKS = (
    "<br><b>"
    "<a href=\"rss_2020_camready.html\">Research Statement</a> "
    "<a href=\"https://twitter.com/AljosaOsep\">Twitter</a> "
    "<a href=\"https://scholar.google.de/scholar?hl=en&as_sdt=0%2C5&q=aljosa+osep&oq=a\">Scholar</a>"
    "</b>"
)

# === Dynamic Content Generation ===
# Load content from JSON files
description = gut.get_about_from_json(json_file='content.json')
news = gut.gen_timestamped_list_from_json(json_file='content.json', source='news')
talks = gut.gen_timestamped_list_from_json(json_file='content.json', source='talks')
students = gut.gen_timestamped_list_from_json(json_file='content.json', source='students')
teaching = gut.gen_timestamped_list_from_json(json_file='content.json', source='teaching')
service = gut.gen_timestamped_list_from_json(json_file='content.json', source='service')

# === Publications Generation ===
bib_file = 'pubs/papers.bib'
with open(bib_file) as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

publications_html = "<div class=\"thebibliography\">"
linkable_keys = ["paper", "video", "poster", "page", "code", "blog", "teaser"]

for entry in bib_database.entries:
    # Parse and abbreviate author names
    authors = LatexNodes2Text().latex_to_text(entry.get("author", ""))
    authors = gut.abbrev_authors(authors)

    # Determine publication type (booktitle or journal)
    pub_type = entry.get("booktitle", entry.get("journal", ""))

    # Generate links for additional resources
    additional_links = "".join(
        f'<a href=\"{entry[key]}\" target=\"_blank\">{key}</a> '
        for key in linkable_keys if key in entry
    )

    # Handle thumbnails
    thumb_file = entry.get("thumb", "default.jpg")  # Default to "default.jpg" if "thumb" is not in the entry
    thumb_url = f"img/thumb/{thumb_file}"  # Prepend the directory path

    # Generate publication entry
    pub_html = (
        f'<div><div style=\"float: left; margin: 5px 20px 10px 0px;\">'
        f'<img src=\"{thumb_url}\" width=\"200\" height=\"200\" style=\"border-radius: 8px;\" />'
        f'</div><div>'
        f'<p class=\"bibitem\"><span class=\"biblabel\"></span> {authors}: <b>{entry.get("title", "")}</b>, {pub_type}, {entry.get("year", "")}.<br>{additional_links}</p>'
        f'</div></div><br clear=\"all\" />'
    )

    publications_html += pub_html

publications_html += "</div>"

# === HTML Page Assembly ===
head = (
    f'<!DOCTYPE html><html lang=\"en\"><head><title>{CAPTION}</title>'
    f'<link rel=\"stylesheet\" href=\"{CSS_LINK}\" /></head>'
)
body = (
    f'<body>'
    f'<h1>{TITLE}</h1>'
    f'{PROFILE_PICTURE}'
    f'<p>{description}</p>'
    f'{LINKS}'
    f'<h2>News</h2>{news}'
    f'<h2>Students Supervised</h2>{students}'
    f'<h2>Service</h2>{service}'
    f'<h2>Talks</h2>{talks}'
    f'<h2>Teaching</h2>{teaching}'
    f'<h2>Publications</h2>{publications_html}'
    f'</body></html>'
)

final_html = f'{head}{body}'

# === Write to File ===
output_file = "index.html"
with open(output_file, "w") as file:
    print(f"Output: {output_file}")
    file.write(final_html)