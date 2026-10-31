#!/usr/bin/env python3
# Builds ITEC_Course_Goal_Assessment.html by embedding ../total_course_assessment/cg_score.py into template.html,
# so the web app always runs the same scoring code as the CLI and desktop GUI.
import os, json, re, base64

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'total_course_assessment', 'cg_score.py')

with open(SRC, encoding='utf-8') as f: py = f.read()
with open(os.path.join(HERE, 'template.html'), encoding='utf-8') as f: page = f.read()

# Embedded as a JS string literal; '</' is escaped so the source can't close the <script> tag.
page = page.replace('__CG_SCORE_PY__', json.dumps(py).replace('</', '<\\/'))

# Inline the guide's screenshots so the page stays a single file.
def inline_image(m):
	path = os.path.join(HERE, m.group(1))
	mime = 'image/png' if path.endswith('.png') else 'image/jpeg'
	with open(path, 'rb') as f: data = base64.b64encode(f.read()).decode()
	return 'src="data:%s;base64,%s"' % (mime, data)
page = re.sub(r'src="(guide_images/[^"]+)"', inline_image, page)

with open(os.path.join(HERE, 'ITEC_Course_Goal_Assessment.html'), 'w', encoding='utf-8') as f: f.write(page)
print('Wrote ITEC_Course_Goal_Assessment.html')
