import markdown
from yaml import safe_load
import bibtexparser
from pylatexenc.latex2text import LatexNodes2Text
import generator_utils as gut
import re

# === Load Markdown Content ===
def load_markdown_with_metadata(file_path):
    """Load Markdown content and extract frontmatter metadata using regex for robust splitting."""
    metadata = {}
    body = ""
    full_content = ""

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            full_content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return {}, ""
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return {}, ""

    # Use regex to find the frontmatter delimiters (---) at the start of the file
    # re.DOTALL allows . to match newlines, \s* matches whitespace including newlines
    match = re.match(r"^---\s*\n(.*?)---\s*\n(.*)", full_content, re.DOTALL)

    if match:
        # Delimiters found, extract text between the --- (frontmatter) and text after the second --- (body)
        frontmatter_text = match.group(1).strip() # Text between --- and ---
        body = match.group(2).strip()             # Text after the second ---

        try:
            # Attempt to parse the extracted frontmatter text as YAML
            parsed_yaml = safe_load(frontmatter_text)
            # Ensure the parsed result is actually a dictionary, otherwise treat as empty metadata
            if isinstance(parsed_yaml, dict) and parsed_yaml is not None:
                 metadata = parsed_yaml
            else:
                 print(f"Warning: Frontmatter in {file_path} parsed, but is not a YAML dictionary (it's {type(parsed_yaml).__name__}). Treating as empty metadata.")
                 metadata = {}

        except Exception as e:
            # If YAML parsing fails, print an error and treat the whole file as the body
            print(f"Error parsing YAML frontmatter in {file_path}: {e}")
            body = full_content # Fallback: treat entire file as body if YAML is invalid
            metadata = {} # No valid metadata found

    else:
        # No frontmatter delimiters found at the start, treat entire content as body
        body = full_content
        metadata = {} # No metadata found

    # Convert the determined body content (which might be the full content if no valid frontmatter) to HTML
    # Use strip() on body before parsing markdown to handle potential leading/trailing whitespace
    html_body = markdown.markdown(body, extensions=["extra", "toc"])

    return metadata, html_body # Return the parsed metadata and the HTML from the body


# Load main content
metadata, main_content_html = load_markdown_with_metadata("content.md")

# === Access Meta Constants ===
caption = metadata.get('meta', {}).get('caption', 'Website Title')
title = metadata.get('meta', {}).get('title', 'My Page')
css_link = metadata.get('meta', {}).get('css_link', '')
profile_picture_html = metadata.get('meta', {}).get('profile_picture', '')
links_html = metadata.get('meta', {}).get('links', '')

# === Extract Dynamic Sections ===
news_items = metadata.get("news", [])
talks = metadata.get("talks", [])
service = metadata.get("service", [])
research_topics = metadata.get("research_topics", [])

# === Render Generic Sections ===
def render_section(title, items):
    """Render a section with a list of items, dynamically handling fields and styling dates."""
    if not items: # Don't render the section if there are no items
        return ""
    section_id = title.lower().replace(" ", "-")
    html = f'<h2 id="{section_id}">{title}</h2><ul>'
    for item in items:
        if isinstance(item, dict):
            # Extract date if present and render it with bold and italic
            date = item.get("date", "")
            date_html = f"<b><i>{date}:</i></b>" if date else ""

            # Dynamically construct the content excluding the date
            content_parts = [
                str(value)
                for key, value in item.items()
                if key != "date" # Skip the date field for the main content
            ]
            content = " ".join(content_parts)
            # Process as Markdown and strip unnecessary tags
            # Added `strip()` to remove potential leading/trailing whitespace from markdown output
            content_html = markdown.markdown(content, extensions=["extra"]).replace("<p>", "").replace("</p>", "").strip()

            # Combine the date and content inline
            html += f"<li>{date_html} {content_html}</li>"
        else:
            # Handle plain string items (process as markdown just in case)
            html += f"<li>{markdown.markdown(str(item), extensions=['extra']).strip()}</li>" # Ensure item is string
    html += "</ul>"
    return html

# === Render Research Topics Section (Simplified) ===
def render_research_topics_section(research_data):
    """
    Generates HTML for the research topics section with hover popups.
    Simplified version assuming correct structure in research_data.
    """

    # Extract description and the list of topics - ASSUMING keys and structure exist
    # If 'description' is missing or None, this will raise a KeyError.
    # If 'topics' is missing or None, this will raise a KeyError.
    description = research_data['description']
    topics_list = research_data['topics']

    # Still include the outermost check to avoid rendering the whole container if empty
    if not description and not topics_list:
        return ""

    html = '<div class="research-topics-container">\n'
    html += '    <h2 id="research">Research</h2>\n'

    # Add the description paragraph if the description field is not an empty string
    # We keep this check because an empty string is valid YAML but shouldn't create a <p>
    if description:
        # Convert the description markdown to HTML
        # .strip() removes leading/trailing whitespace from the string itself
        description_html_content = markdown.markdown(description.strip(), extensions=["extra"]).strip()
        # Wrap the markdown output in a paragraph tag
        html += f'    <p>{description_html_content}</p>\n\n'


    if topics_list:
        html += '    <div class="topics-grid">\n'
        for topic in topics_list:
            topic_title = topic['title']
            image_filename = topic['image']
            image_path = f"img/thumb/{image_filename}"
            papers = topic['papers']

            # Start individual topic container
            html += '        <div class="topic-container">\n'
            # Topic visible part (image and title)
            html += '            <div class="topic">\n'
            # Add image tag - ASSUMING path and filename are valid and image exists
            # No default image logic included here. If the image file is missing, the browser will show a broken image icon.
            html += f'                 <img src="{image_path}" alt="{topic_title} image" />\n' # Simplified image tag

            html += f'                <strong>{topic_title}</strong>\n'
            html += '            </div>\n' # Close topic div

            # Popup hidden part (list of papers)
            html += '            <div class="popup">\n'
            html += f'                <h3>Relevant Papers: {topic_title}</h3>\n'

            # Add paper list - ASSUMING papers list is iterable and items are dictionaries
            html += '                <ul>\n'
            for paper in papers: # ASSUMING paper is a dictionary
                # Extract paper data - ASSUMING keys exist
                # If 'title' or 'link' are missing, this will raise a KeyError.
                paper_title = paper['title']
                paper_link = paper['link']
                html += f'                    <li><a href="{paper_link}" target="_blank">{paper_title}</a></li>\n'
            html += '                </ul>\n'
            html += '            </div>\n' # Close popup div
            html += '        </div>\n' # Close topic-container
        html += '    </div>\n' # Close topics-grid
    html += '</div>\n' # Close research-topics-container

    return html

# Render each section
news_html = render_section("News", news_items)
talks_html = render_section("Talks", talks)
service_html = render_section("Service", service)
research_topics_html = render_research_topics_section(research_topics)

# === Navigation Bar ===
_icon_github = (
    '<svg role="img" viewBox="0 0 24 24" width="20" height="20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">'
    '<title>GitHub</title>'
    '<path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285'
    '-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744'
    '.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776'
    '.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303'
    '-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405'
    ' 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61'
    '-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57'
    'C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/>'
    '</svg>'
)
_icon_twitter = (
    '<svg role="img" viewBox="0 0 24 24" width="20" height="20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">'
    '<title>Twitter</title>'
    '<path d="M21.543 7.104c.015.211.015.423.015.636 0 6.507-4.954 14.01-14.01 14.01v-.003A13.94 13.94 0 0 1 0'
    ' 19.539a9.88 9.88 0 0 0 7.287-2.041 4.93 4.93 0 0 1-4.6-3.42 4.916 4.916 0 0 0 2.223-.084A4.926 4.926'
    ' 0 0 1 .96 9.167v-.062a4.887 4.887 0 0 0 2.235.616A4.928 4.928 0 0 1 1.67 3.148a13.98 13.98 0 0 0 10.15'
    ' 5.144 4.929 4.929 0 0 1 8.39-4.49 9.868 9.868 0 0 0 3.128-1.196 4.941 4.941 0 0 1-2.166 2.724A9.828'
    ' 9.828 0 0 0 24 4.555a10.019 10.019 0 0 1-2.457 2.549z"/>'
    '</svg>'
)
_icon_scholar = (
    '<svg role="img" viewBox="0 0 24 24" width="20" height="20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">'
    '<title>Google Scholar</title>'
    '<path d="M5.242 13.769L0 9.5 12 0l12 9.5-5.242 4.269C17.548 11.249 14.978 9.5 12 9.5c-2.977 0-5.548'
    ' 1.748-6.758 4.269zM12 10a7 7 0 1 0 0 14 7 7 0 0 0 0-14z"/>'
    '</svg>'
)

nav_html = (
    '<div style="clear:both;"></div>\n'
    '<nav class="section-nav">\n'
    '  <span class="nav-sections">\n'
    '    <a href="#research">Research</a>\n'
    '    <a href="#news">News</a>\n'
    '    <a href="#talks">Talks</a>\n'
    '    <a href="#service">Service</a>\n'
    '    <a href="#publications">Publications</a>\n'
    '  </span>\n'
    '  <span class="nav-icons">\n'
    f'    <a href="https://github.com/aljosaosep" target="_blank" title="GitHub">{_icon_github}</a>\n'
    f'    <a href="https://twitter.com/AljosaOsep" target="_blank" title="Twitter">{_icon_twitter}</a>\n'
    f'    <a href="https://scholar.google.de/scholar?hl=en&as_sdt=0%2C5&q=aljosa+osep&oq=a" target="_blank" title="Google Scholar">{_icon_scholar}</a>\n'
    '  </span>\n'
    '</nav>\n'
)

# === Publications Generation ===
bib_file = 'pubs/papers.bib'
try:
    with open(bib_file, encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
except FileNotFoundError:
    print(f"Warning: BibTeX file not found at {bib_file}. Publications section will be empty.")
    bib_database = type('obj', (object,), {'entries': []})() # Create a dummy object with empty entries
except Exception as e:
     print(f"Error reading BibTeX file {bib_file}: {e}")
     bib_database = type('obj', (object,), {'entries': []})()


publications_html = "<div class=\"thebibliography\">"
linkable_keys = ["paper", "video", "poster", "page", "code", "blog", "teaser"]

for entry in bib_database.entries:
    # Parse and abbreviate author names
    # Added error handling for missing 'author' key
    authors = LatexNodes2Text().latex_to_text(entry.get("author", "N/A"))
    try:
        authors = gut.abbrev_authors(authors) # Assuming gut is correctly imported and has abbrev_authors
    except NameError:
         print("Warning: generator_utils not found or abbrev_authors missing. Using full author list.")
         pass # Use the raw authors if gut.abbrev_authors isn't available


    # Determine publication type (booktitle or journal) - Added default 'N/A'
    pub_type = entry.get("booktitle", entry.get("journal", "N/A"))

    # Generate links for additional resources
    additional_links = "".join(
        f'<a href=\"{entry[key]}\" target=\"_blank\">{key}</a> '
        for key in linkable_keys if key in entry and entry[key].strip() # Check link is not empty
    )

    # Handle thumbnails - Added check for empty thumb value
    thumb_file = entry.get("thumb", "default.jpg")
    if not thumb_file.strip(): # If thumb value is empty or just whitespace
         thumb_file = "default.jpg" # Use default if specified thumb is empty

    thumb_url = f"img/thumb/{thumb_file}" # Prepend the directory path

    # Generate publication entry
    publications_html += '<div>\n'
    publications_html += '    <div style="float: left; margin: 5px 20px 10px 0px;">\n'
    publications_html += f'        <img src="{thumb_url}" width="200" height="200" style="border-radius: 8px;" />\n'
    publications_html += '    </div>\n'
    publications_html += '    <div>\n'
    publications_html += f'        <p class="bibitem"><span class="biblabel"></span> {authors}: <b>{entry.get("title", "No Title")}</b>, {pub_type}, {entry.get("year", "N/A")}.<br>{additional_links}</p>\n'
    publications_html += '    </div>\n'
    publications_html += '</div><br clear="all" />\n'


publications_html += "</div>"


# === HTML Page Assembly ===
head = (
    '<!DOCTYPE html>\n'
    '<html lang="en">\n'
    '<head>\n'
    f'    <title>{caption}</title>\n'
    f'    <link rel="stylesheet" href="{css_link}" />\n'
    '    <link rel="stylesheet" href="style_research.css" />\n'
    '</head>\n'
)

body = (
    '<body>\n'
    f'<h1>{title}</h1>\n'
    f'{profile_picture_html}\n'
    f'{main_content_html}\n'
    f'{links_html}\n'
    f'{nav_html}\n'
    f'{research_topics_html}\n'
    f'{news_html}\n'
    f'{talks_html}\n'
    f'{service_html}\n'
    f'<h2 id="publications">Publications</h2>{publications_html}\n'
    '</body>\n'
    '</html>'
)

final_html = f'{head}{body}' # Combine head and body

# === Write to File ===
output_file = "index.html"
try:
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(final_html)
    print(f"Successfully generated {output_file}")
except Exception as e:
    print(f"Error writing to file {output_file}: {e}")