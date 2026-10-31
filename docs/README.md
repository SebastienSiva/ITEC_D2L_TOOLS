# ITEC Course Goal Assessment (web app)

The same tool as `total_course_assessment/`, running in a web browser. Nothing to install.

It runs the real `cg_score.py` in the browser using [Pyodide](https://pyodide.org) (Python compiled to WebAssembly).
**CSV files are read and processed on the user's computer and are never uploaded.**

## Use
Hosted at https://sebastiensiva.github.io/ITEC_D2L_TOOLS/ (GitHub Pages, served from this `docs/` folder on `main`).

Open `index.html` (double-click, or host it on any web space), add the CSV files, click **Check files**,
review flagged students, then **Calculate scores**. File formats are described in
[the main README](../total_course_assessment/README.md).

Each time it opens, the page downloads its engine from jsDelivr (~10 MB; usually cached by the browser), so it needs an internet connection. Professors just double-click the file. They never see or install Python.

## Edit / build
Scoring logic lives only in `../total_course_assessment/cg_score.py`. After changing it (or `template.html`), rebuild:

`python build.py`

This embeds `cg_score.py` into `template.html` and writes the self-contained `index.html`.

## Hosting
`index.html` is a single static file; any web server (e.g. GGC web space) works, with no PHP or database.
To avoid depending on jsDelivr, download the Pyodide release and change the `pyodide.js` URL in `template.html`.

## How-to guide and screenshots
The "how to use" link opens a guide built into the page (`#how-to`). It follows Dr. Siva's video tutorial
(`../ITEC_D2L_CourseGoalAssessment.mp4`). Its images live in `guide_images/`, and `build.py` embeds them so the page stays one file.

- `d2l_*.jpg`: cropped from the tutorial video. **Every crop was checked to contain no student names, IDs or grades.**
  The video itself does show real student data in places (the gradebook CSV, the "Remove student" dialogs, the D2L grade lists),
  so take any new screenshots from it with care.
- `app_*.png`: screenshots of this page using the fake `sample_data/`.
