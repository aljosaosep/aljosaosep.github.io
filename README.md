# Aljosa's Academic Webpage Generator

This repository provides a Python-based generator to create a professional academic webpage. Content is specified in a combination of Markdown and BibTeX, making it easy to manage and update.

## Features

- **Markdown-based content**: Easily define sections such as news, students, talks, teaching, and service.
- **BibTeX integration**: Automatically generate a publications list with support for thumbnails and additional links.
- **Customizable metadata**: Define your webpage's title, CSS, and other static elements in Markdown frontmatter.
- **Modern HTML output**: Generates clean, responsive HTML with LaTeX-style aesthetics.

---

## Requirements

To use this generator, you need:

- **Python 3.7+**
- Python libraries:
  - `markdown`
  - `PyYAML`
  - `bibtexparser`
  - `pylatexenc`
- A content Markdown file (`content.md`) for text and metadata.
- A BibTeX file (`pubs/papers.bib`) for publications.
- Thumbnail images for publications stored in the `img/thumb/` directory.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/academic-webpage-generator.git
   cd academic-webpage-generator
   ```

2. Install the required Python packages:
   ```bash
   pip install markdown PyYAML bibtexparser pylatexenc
   ```

3. Place your content files:
   - `content.md` in the root directory.
   - `pubs/papers.bib` in the `pubs/` directory.
   - Thumbnail images in the `img/thumb/` directory.

---

## Content Structure

### 1. Markdown Content (`content.md`)

The main content is written in Markdown with frontmatter metadata for static elements. Below is an example structure:

```yaml
---
meta:
  caption: "Aljosa's Web Corner"
  title: "Aljosa Osep, Ph.D."
  css_link: "https://latex.now.sh/style.min.css"
  profile_picture: "<img src='img/aljosa.jpg' alt='Profile Picture' width='200' align='left' style='padding:10px;'>"
  links: >
    <br><b>
    <a href="rss_2020_camready.html">Research Statement</a>
    <a href="https://twitter.com/AljosaOsep">Twitter</a>
    <a href="https://scholar.google.com/scholar?hl=en&q=aljosa+osep">Scholar</a>
    </b>
news:
  - date: "June 2024"
    title: "I joined NVIDIA as a Senior Research Scientist!"
  - date: "March 2024"
    title: >
      Our [paper](https://arxiv.org/abs/2403.13129) on *Learning to segment anything in Lidar (SAL)*
      was featured at GTC2024! Check out the [presentation](https://youtu.be/LLSuUBObttE?si=WvQFphni5vX7Es5I).
students:
  - name: "Xindi Wu"
    affiliation: "CMU, 2022"
    next_step: "→ <i>Princeton</i>"
talks:
  - date: "June 2024"
    title: >
      CVPR 2024 Area Chair Panel, invited talk: Learning To Understand The World From Video,
      [Slides](https://docs.google.com/presentation/d/1JCy1TARAlcT0HIT07uRUic1iPsMejIDqYckeRTOvzn8/edit?usp=sharing)
teaching:
  - date: "Summer 2022"
    title: >
      Lecturer for [IN2375: Computer Vision III: Detection, Segmentation and Tracking (CV3DST)](https://dvl.in.tum.de/teaching/cv3dst-ss22/) (TU Munich)
service:
  - title: >
      Area Chair (AC) for ICLR, CVPR, ECCV, ICCV, WACV, ACCV.
---
```

- **Metadata (`meta`)**: Static elements like title, CSS, and profile picture.
- **Sections (`news`, `students`, etc.)**: Each section is an array of items with optional `date` and `title`.

---

### 2. BibTeX File (`pubs/papers.bib`)

The `papers.bib` file stores publication data. Below is an example entry:

```bibtex
@inproceedings{sample2024,
  author = {John Doe and Jane Smith},
  title = {An Example Paper},
  booktitle = {Proceedings of the Great Conference},
  year = {2024},
  paper = {https://example.com/paper.pdf},
  code = {https://github.com/example/repo},
  thumb = {example_thumb.jpg}
}
```

- **Required Fields**:
  - `author`: Names of the authors.
  - `title`: Title of the paper.
  - `booktitle` or `journal`: Publication venue.
  - `year`: Year of publication.
- **Optional Fields**:
  - `paper`, `code`, `video`, etc.: Links to related resources.
  - `thumb`: Filename of the thumbnail in `img/thumb/`.

---

## Directory Structure

Ensure the following structure for your files:
```
academic-webpage-generator/
├── content.md          # Markdown content
├── pubs/
│   └── papers.bib      # BibTeX publications
├── img/
│   └── thumb/          # Thumbnails for publications
├── generator.py        # Main script
├── generator_utils.py  # Utility functions
└── index.html          # Generated webpage
```

---

## Running the Generator

1. Run the Python script:
   ```bash
   python generator.py
   ```

2. Open the `index.html` file in your browser to view the generated webpage.

---

## Customization

- **Styling**: Modify the `css_link` in `content.md` to use a different CSS stylesheet.
- **Content**: Update the sections in `content.md` to reflect your achievements and activities.
- **Thumbnails**: Place `.jpg` files in `img/thumb/` and reference them in your BibTeX entries.

---

## Troubleshooting

- **Missing Thumbnails**: Ensure thumbnails are in `img/thumb/` and referenced in `papers.bib`.
- **Broken Links**: Verify that all URLs in Markdown and BibTeX are correct.
- **HTML Rendering Issues**: Check for unclosed HTML tags or invalid Markdown.