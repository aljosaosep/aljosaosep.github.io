# Import necessary libraries
import markdown
from yaml import safe_load
import bibtexparser
from pylatexenc.latex2text import LatexNodes2Text
import generator_utils as gut

# === Load Markdown Content ===
def load_markdown_with_metadata(file_path):
    """Load Markdown content and extract frontmatter metadata."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Split frontmatter (YAML) and body (Markdown)
    if content.startswith("---"):
        _, frontmatter, body = content.split("---", 2)
        metadata = safe_load(frontmatter)
    else:
        metadata = {}
        body = content
    html_body = markdown.markdown(body, extensions=["extra", "toc"])
    return metadata, html_body

# Load main content
metadata, main_content_html = load_markdown_with_metadata("content.md")

# === Access Meta Constants ===
caption = metadata['meta']['caption']
title = metadata['meta']['title']
css_link = metadata['meta']['css_link']
profile_picture = metadata['meta']['profile_picture']
links = metadata['meta']['links']

# === Extract Dynamic Sections ===
news_items = metadata.get("news", [])
students = metadata.get("students", [])
talks = metadata.get("talks", [])
teaching = metadata.get("teaching", [])
service = metadata.get("service", [])

# === Render Sections ===
def render_section(title, items):
    """Render a section with a list of items, dynamically handling fields and styling dates."""
    html = f"<h2>{title}</h2><ul>"
    for item in items:
        if isinstance(item, dict):
            # Extract date if present and render it with bold and italic
            date = item.get("date", "")
            date_html = f"<b><i>{date}:</i></b>" if date else ""
            
            # Dynamically construct the content excluding the date
            content_parts = [
                str(value)
                for key, value in item.items()
                if key != "date"  # Skip the date field for the main content
            ]
            content = " ".join(content_parts)
            # Process as Markdown and strip unnecessary tags
            content_html = markdown.markdown(content, extensions=["extra"]).replace("<p>", "").replace("</p>", "")
            
            # Combine the date and content inline
            html += f"<li>{date_html} {content_html}</li>"
        else:
            # Handle plain string items
            html += f"<li>{markdown.markdown(item, extensions=['extra']).strip()}</li>"
    html += "</ul>"
    return html

# Render each section
news_html = render_section("News", news_items)
students_html = render_section("Students Supervised", students)
talks_html = render_section("Talks", talks)
teaching_html = render_section("Teaching", teaching)
service_html = render_section("Service", service)

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
    f'<!DOCTYPE html><html lang="en"><head><title>{caption}</title>'
    f'<link rel="stylesheet" href="{css_link}" /></head>'
)
body = (
    f'<body>'
    f'<h1>{title}</h1>'
    f'{profile_picture}'
    f'{main_content_html}'
    f'{links}'
    f'{news_html}'
    f'{students_html}'
    f'{talks_html}'
    f'{teaching_html}'
    f'{service_html}'
    f'<h2>Publications</h2>{publications_html}'
    f'</body></html>'
)

final_html = f'{head}{body}'

# === Write to File ===
output_file = "index.html"
with open(output_file, "w", encoding="utf-8") as file:
    print(f"Output: {output_file}")
    file.write(final_html)