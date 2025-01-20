import json
from nameparser import HumanName

def get_about_from_json(json_file):
    """
    Retrieve the "about" section from a JSON file.

    Args:
        json_file (str): Path to the JSON file.

    Returns:
        str: The "about" section content.
    """
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            return data.get("about", "")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(f"Error reading or parsing {json_file}: {e}")

def gen_timestamped_list_from_json(json_file, source):
    """
    Generate a timestamped HTML list from a JSON file.

    Args:
        json_file (str): Path to the JSON file.
        source (str): The key in the JSON file to extract items from.

    Returns:
        str: HTML unordered list as a string.
    """
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            items = data.get(source, [])

            if not items:
                return "<ul><li>No items available.</li></ul>"

            html_list = "<ul>"
            for item in items:
                html = item.get("html", "")
                date = item.get("date", "")

                if not html:
                    raise ValueError(f"Missing 'html' in item: {item}")

                if date:
                    html_list += f"<li><b><i>{date}:</i></b> {html}</li>"
                else:
                    html_list += f"<li>{html}</li>"

            html_list += "</ul>"
            return html_list
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(f"Error reading or parsing {json_file}: {e}")

def abbrev_authors(authors_str):
    """
    Abbreviate a list of author names.

    Args:
        authors_str (str): Author names in a single string, separated by 'and'.

    Returns:
        str: Abbreviated author names.
    """
    if not authors_str:
        return ""

    names = authors_str.split(" and ")
    abbrev_names = []

    for name in names:
        parsed_name = HumanName(name)
        abbreviated = f"{parsed_name.first[0]}. {parsed_name.last}" if parsed_name.first and parsed_name.last else name
        abbrev_names.append(abbreviated)

    return ", ".join(abbrev_names)