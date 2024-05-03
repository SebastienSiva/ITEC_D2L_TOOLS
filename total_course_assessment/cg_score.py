#!/usr/bin/env python3
from sys import *
from collections import defaultdict
import os, csv, re

GRADE_BOOK_SEARCH_TAG = "Points Grade <Numeric MaxPoints"
QUIZ_GRADE_SEARCH_TAG = "Q Title"

CMD_LINE_HELP = """
The script used 3 types of files to calculate course goal scores for a D2L section. Course goal scores are the percentage of students getting a 70% or better on course goal related assessment.

File_Type1* (>= 0 files): Quiz grade export CSV files with Question Titles containing 1 or more course goal identifiers (like 'G3 G4 strings and if statements')

File_Type2 (0 or 1 file): The D2L gradebook exported as Points CSV with OrgId, FirstName, LastName.

File_Type3 (1 file only if File Type2 present): CSV file mapping grades to course goals according to the following format:

GRADE_NAME,CG,CG,CG,CG,CG
final_p1,5,6,1
final_p2,5,6

Feed this script 0 command line arguments and it will automatically search the directory for the files described above.

Optionally include the files explicitly as command line arguments.

Ex: python3 cg_score.py path_to_quz1_cg.csv path_to_quz2_cg.csv path_to_gradebook.csv path_to_grade_cg_map.csv

Ex: python3 cg_score.py 2140_grade_cg.csv GB_Points.csv FinalExamMC.csv
"""

def fail(s):
	print(s)
	exit(0)


class CG_Score:

	def __init__(self):
		self.grade_book = None
		self.grade_book_cgs = None
		self.students = defaultdict(lambda: defaultdict(int)) # {'#400.139102':{'CG1_points':17, 'CG1_max':20, ...}, '#400.222222':{'CG1_points':12, ...}}
		self.ignored_students = defaultdict(list) # {'#400.139102':['Zero for Asg1', 'Zero for Asg2'], ...}
		self.num_students_pass = defaultdict(int) # {CG1:13, CG2:14, ...}

	
	def hasNoFiles(self):
		return (self.grade_book == None and self.grade_book_cgs == None 
			and len(self.students) == 0)

	def readyToProcess(self):
		return ((self.grade_book != None and self.grade_book_cgs != None)
			or len(self.students) > 0)
			
	
	#################################################################################
	# QUIZ FILES
	#################################################################################
	def isQuizPointFile(self, f):
		with open(f, 'r', newline='') as csvfile:
			reader = csv.reader(csvfile)
			first_row = next(reader)
			for entry in first_row:
				if entry == QUIZ_GRADE_SEARCH_TAG:
					return True
		return False;	

	def processQuizPointFile(self, f):
		CG_points = {} # {'400.139102':{'CG1_points':17, 'CG1_max':20, 'CG2_points':11,}}
		ques_titles = {} # {'400.139102':{'G5-O6/O7-a1', 'G2   valid var', ...}}
		with open(f, 'r', newline='') as csvfile:
			dr = csv.DictReader(csvfile)
			for row in dr:
				sid = '#%s-%s_%s' % (row['Org Defined ID'], row['FirstName'], row['LastName'])
				if "400" not in sid: continue # avoid demo id

				if sid not in CG_points:
					CG_points[sid] = {}
					ques_titles[sid] = set()
				student_points = CG_points[sid]
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


		self.check_student_mismatch(CG_points.keys(), f)

		for sid in CG_points:
			student_points = CG_points[sid]
			for key in student_points:
				self.students[sid][key] += student_points[key]


	#################################################################################
	# GRADEBOOK FILE
	#################################################################################
	def isGradeBookFile(self, f):
		with open(f, 'r', newline='') as csvfile:
			reader = csv.reader(csvfile)
			first_row = next(reader)
			for entry in first_row:
				if GRADE_BOOK_SEARCH_TAG in entry:
					return True
		return False;	

	def buildGradeBook(self, f):
		gradebook = {} # {'#400.139102':{'copyme_asg2.1 Points Grade <Numeric MaxPoints:10 Weight:1.08 Category:Assignments CategoryWeight:30>':8, ...}}
		with open(f, 'r', newline='') as csvfile:
			dr = csv.DictReader(csvfile)
			for row in dr:
				sid = '%s-%s_%s' % (row['OrgDefinedId'], row['First Name'], row['Last Name'])			
				if "400" not in sid: continue # avoid demo id (#)
				gradebook[sid] = {}
				for key in row:
					if GRADE_BOOK_SEARCH_TAG in key:
						gradebook[sid][key] = row[key]
		
		self.check_student_mismatch(gradebook.keys(), f)
		return gradebook;

	def processGradeBook(self):
		if bool(self.grade_book) != bool(self.grade_book_cgs):
			return "ERROR: Requires both gradebook and gradebook_cg_map or neither."
		elif self.grade_book == None: return ""
		
		for sid in self.grade_book:
			self.students[sid] = defaultdict(int)
			for header in self.grade_book[sid]:
				if GRADE_BOOK_SEARCH_TAG in header:
					grade_name = header[0:header.find(GRADE_BOOK_SEARCH_TAG) - 1]
					if grade_name in self.grade_book_cgs:
						r = re.search(r"MaxPoints:(\d+)", header)
						if not r: return ("ERROR: MaxPoints not found in", header)
						grade_max = float(r.group(1))
						grade_points = float(self.grade_book[sid][header])
						if grade_points == 0:
							self.ignored_students[sid].append('0 for ' + grade_name)
						for cg in self.grade_book_cgs[grade_name]:
							self.students[sid][cg+'_points'] += grade_points
							self.students[sid][cg+'_max'] += grade_max
		return ""		


	#########################################################################################
	# GRADE BOOK CG MAPPING FILE
	#########################################################################################
	def isGradeBookCGMapFile(self, f):
		with open(f, 'r', newline='') as csvfile:
			reader = csv.reader(csvfile)
			first_row = next(reader)
			if first_row[0:2] == ["GRADE_NAME", "CG"]:
				return True
		return False;	

	def buildGradeBookCGs(self, f):
		gradebook_cgs = {}
		with open(f, 'r', newline='') as csvfile:
			reader = csv.reader(csvfile); next(reader)
			for row in reader:
				gradebook_cgs[row[0]] = ['CG' + x for x in row[1:]]
		return gradebook_cgs
		

	#########################################################################################
	# FILE ANALYSYS
	#########################################################################################
		
	def process_file(self, f):
		if self.isGradeBookFile(f):
			if(not self.grade_book):	
				self.grade_book = self.buildGradeBook(f)
				return "GRADE BOOK"
			else: return "ERROR: 2 Grade Book Files"
		elif self.isGradeBookCGMapFile(f):
			if(not self.grade_book_cgs):	
				self.grade_book_cgs = self.buildGradeBookCGs(f)
				return "GRADE BOOK COURSE GOAL MAP"
			else: return ("ERROR: 2 Grade Book Course Goal Mapping Files")
		elif self.isQuizPointFile(f):
			self.processQuizPointFile(f)
			return "QUIZ FILE"
		else: return "ERROR: UNRECOGNISED FILE"	

	def check_student_mismatch(self, new_students, f_name):
		old_students = self.students.keys()
		if len(old_students) == 0:
			return
		# print("SPECIAL", new_students - old_students)
		for sid in new_students - old_students:
			self.ignored_students[sid].append("Unexpected new student " + sid + " found in " + f_name)
		for sid in old_students - new_students:
			self.ignored_students[sid].append("Student " + sid + " missing in " + f_name)
	
					
	def filter_students(self):
		filtered_students = {k:v for k, v in self.students.items() if k not in self.ignored_students}
		self.students = filtered_students
	
	def calc_num_students_pass(self):
		for scores in self.students.values():
			for key in scores:
				if '_points' in key:
					points = scores[key]
					max_points = scores[key.replace('_points', '_max')]
					if max_points > 0 and points / max_points >= 0.7:
						self.num_students_pass[key[0:-len('_points')]] += 1;
						
	def get_stats_str(self):
		s = "TOTAL STUDENTS: %s\n" % (len(self.students))
		header = 'PERCENT OF STUDENTS GETTING >= 70% ON EACH COURSE GOAL'
		s += ("\n%s\n%s\n") % (header, '*' * 80)
		for cg in sorted(self.num_students_pass.keys()):
			p = round(100 * self.num_students_pass[cg] / len(self.students), 0)
			s += (cg + ": " + str(p) + '%\n')
		
		header = 'ALL STUDENT COURSE GOAL SCORES'
		s += ("\n%s\n%s\n") % (header, '*' * 80)
		for sid, points in self.students.items():
			cg_names = [c.replace('_points', '') for c in sorted(points.keys()) if '_points' in c]
			cg_scores = ["%s %s/%s" % (c, round(points[c + '_points'], 1), points[c + '_max']) 
				for c in cg_names]
			s += (sid[sid.find('-')+1:] + ' ' + ', '.join(cg_scores)) + '\n'

		return s

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
	
	cgs = CG_Score()
	
	# search through argv files.
	for f in file_names:
		r = cgs.process_file(f)
		if r.startswith("ERROR"): fail(r)
		print(r, "FILE:", f)
	print()
	
	r = cgs.processGradeBook()
	if r.startswith("ERROR"): fail(r)
	
	unignore = []
	for sid in cgs.ignored_students:
		print("Ignored Student: " + sid + " has:")
		for reason in cgs.ignored_students[sid]:
			print('\t' + reason)
		if input("Ignore " + sid + " for analysis ([y] or n)? ") == 'n': unignore.append(sid)
	for sid in unignore:
		del cgs.ignored_students[sid]
	
	cgs.filter_students()

	cgs.calc_num_students_pass()
	
	print(cgs.get_stats_str())
