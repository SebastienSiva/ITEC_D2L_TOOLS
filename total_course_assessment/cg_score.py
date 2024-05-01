#!/usr/bin/env python3
from sys import *
from collections import defaultdict
import os, csv, re

grade_book_style_str = "Points Grade <Numeric MaxPoints"
quiz_grade_style_str = "Q Title"

directions = """
1.  Feed this script 0 or more D2L quiz grade export CSV files with Question Titles containing 1 or more course goal identifiers (like 'G3 G4 strings and if statements') 
2.  Optionally include the D2L gradebook (exported as Points CSV with OrgId, FirstName, LastName) and a separate CSV file mapping grades to course goals according to the following format:

GRADE_NAME,CG,CG,CG,CG,CG
final_p1,5,6,1
final_p2,5,6

Ex: python3 cg_score.py path_to_quz1_cg.csv path_to_quz2_cg.csv path_to_gradebook.csv path_to_grade_cg_map.csv

Ex: python3 cg_score.py 2140_grade_cg.csv GB_Points.csv FinalExamMC.csv

"""

def fail(s):
	print("ERORR:", s)
	exit(0)

#########################################################################################
# QUIZ FILES
#########################################################################################
def isQuizPointFile(f):
	with open(f, 'r', newline='') as csvfile:
		reader = csv.reader(csvfile)
		first_row = next(reader)
		for entry in first_row:
			if entry == quiz_grade_style_str:
				return True
	return False;	

def buildQuizCGPoints(f):
	# print(f"Processing quiz: {f}")
	quiz_points = {} # {'400.139102':{'CG1_points':17, 'CG1_max':20, 'CG2_points':11,}}
	ques_titles = {} # {'400.139102':{'G5-O6/O7-a1', 'G2   valid var', ...}}
	with open(f, 'r', newline='') as csvfile:
		dr = csv.DictReader(csvfile)
		for row in dr:
			sid = '#%s-%s_%s' % (row['Org Defined ID'], row['FirstName'], row['LastName'])
			if "400" not in sid: continue # avoid demo id

			if sid not in quiz_points:
				quiz_points[sid] = {}
				ques_titles[sid] = set()
			student_points = quiz_points[sid]
			student_questions = ques_titles[sid]
			q_title = row['Q Title']+row['Q Text']
			if q_title in student_questions: continue # question already done
			student_questions.add(q_title)
			
			for cg in re.findall(r"G\d", q_title):
				cgp = 'C' + cg + '_points'
				cgm = 'C' + cg + '_max'
				if cgp not in student_points:
					student_points[cgp] = 0.0
					student_points[cgm] = 0.0
				student_points[cgp] += float(row['Score'])
				student_points[cgm] += float(row['Out Of']) if row['Bonus?'].upper() == 'FALSE' else 0
				
	return quiz_points;


#########################################################################################
# GRADEBOOK FILE
#########################################################################################

def isGradeBookFile(f):
	with open(f, 'r', newline='') as csvfile:
		reader = csv.reader(csvfile)
		first_row = next(reader)
		for entry in first_row:
			if grade_book_style_str in entry:
				return True
	return False;	

def buildGradeBook(f):
	gradebook = {} # {'#400.139102':{'copyme_asg2.1 Points Grade <Numeric MaxPoints:10 Weight:1.08 Category:Assignments CategoryWeight:30>':8, ...}}
	with open(f, 'r', newline='') as csvfile:
		dr = csv.DictReader(csvfile)
		for row in dr:
			sid = '%s-%s_%s' % (row['OrgDefinedId'], row['First Name'], row['Last Name'])			
			if "400" not in sid: continue # avoid demo id (#)
			gradebook[sid] = {}
			for key in row:
				if grade_book_style_str in key:
					gradebook[sid][key] = row[key]
	return gradebook;


#########################################################################################
# GRADE BOOK CG MAPPING FILE
#########################################################################################
def isGradeBookCGFile(f):
	with open(f, 'r', newline='') as csvfile:
		reader = csv.reader(csvfile)
		first_row = next(reader)
		if first_row[0:2] == ["GRADE_NAME", "CG"]:
			return True
	return False;	

def buildGradeBookCGs(f):
	gradebook_cgs = {}
	with open(f, 'r', newline='') as csvfile:
		reader = csv.reader(csvfile); next(reader)
		for row in reader:
			gradebook_cgs[row[0]] = ['CG' + x for x in row[1:]]
	return gradebook_cgs



#########################################################################################
# MAIN
#########################################################################################
if __name__ == "__main__":
	file_names = []
	if len(argv) >= 2:
		file_names = argv[1:]
	else:
		for f in os.listdir("."):
			if os.path.isfile(f) and f[-4:].upper() == '.CSV':
				file_names.append(f)
	
	grade_book = None
	grade_book_cgs = None
	quiz_cg_points = []

	# search through argv files.
	for f in file_names:
		if isGradeBookFile(f):
			if(not grade_book):	
				grade_book = buildGradeBook(f)
				print(f"USING {f} AS GRADE BOOK")
			else: fail("2 grade book files.")
		elif isGradeBookCGFile(f):
			if(not grade_book_cgs):	
				grade_book_cgs = buildGradeBookCGs(f)
				print(f"USING {f} AS GRADE BOOK COURSE GOAL MAP")
			else: fail("2 grade book course goal mapping files.")
		elif isQuizPointFile(f):
			print(f"USING {f} AS A QUIZ FILE")
			quiz_cg_points.append(buildQuizCGPoints(f))
		else: print(f"NOTE SKIPPING: {f} is unrecognized file.")

	if bool(grade_book) != bool(grade_book_cgs):
		fail("Need both gradebook and gradebook_cg_map or neither.")

	print()
	
	# BUILD STUDENT COURSE GOAL MAP (initialize on the fly if no gradebook given)
	students = defaultdict(lambda: defaultdict(int)) # {'#400.139102':{'CG1_points':17, 'CG1_max':20, ...}, '#400.222222':{'CG1_points':12, ...}}
	skip_students = set()

	# GRADE BOOK
	if grade_book:
		for sid in grade_book:
			students[sid] = defaultdict(int)
			for header in grade_book[sid]:
				if grade_book_style_str in header:
					grade_name = header[0:header.find(grade_book_style_str) - 1]
					if grade_name in grade_book_cgs:
						r = re.search(r"MaxPoints:(\d+)", header)
						if not r: fail("MaxPoints not found in", header)
						grade_max = float(r.group(1))
						grade_points = float(grade_book[sid][header])
						if grade_points == 0:
							if input(sid + " has zero for " + grade_name + 
								".\nType 'y' to remove: ") == 'y': 
								skip_students.add(sid)
								break
						for cg in grade_book_cgs[grade_name]:
							students[sid][cg+'_points'] += grade_points
							students[sid][cg+'_max'] += grade_max
	
	# QUIZZES
	for quiz in quiz_cg_points:
		for sid in quiz:
			if sid in skip_students: continue
			student_points = quiz[sid]
			for key in student_points:
				students[sid][key] += student_points[key]
	
	filtered_students = {k:v for k, v in students.items() if k not in skip_students}


	num_students_pass = defaultdict(int) # {CG1:13, CG2:14, ...}
	for scores in filtered_students.values():
		for key in scores:
			if '_points' in key:
				points = scores[key]
				max_points = scores[key.replace('_points', '_max')]
                                # Bonus questions can result in max points of 0
				if max_points > 0 and points / max_points >= 0.7:
					num_students_pass[key[0:-len('_points')]] += 1;
	
	print("\nALL STUDENT COURSE GOAL SCORES")
	for sid, points in filtered_students.items():
		cgs = [c.replace('_points', '') for c in sorted(points.keys()) if '_points' in c]
		cg_scores = ["%s %s/%s" % (c, round(points[c + '_points'], 1), points[c + '_max']) 
			for c in cgs]
		print(sid[sid.find('-')+1:], ", ".join(cg_scores)) # [(cg, points[cg]) for cg in cgs])
	
	
	print("\nPERCENT OF STUDENTS GETTING >= 70% ON EACH COURSE GOAL")
	for cg in sorted(num_students_pass.keys()):
		p = round(100 * num_students_pass[cg] / len(filtered_students), 0)
		print(cg + ": " + str(p) + '%')
	
	print("\nTOTAL STUDENTS:", len(filtered_students)) 
			
