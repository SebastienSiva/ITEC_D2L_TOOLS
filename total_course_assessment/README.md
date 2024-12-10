# Course Goal Assessment App

## Download The GUI
* [Windows](https://github.com/SebastienSiva/ITEC_D2L_TOOLS/raw/main/total_course_assessment/dist_zips/Windows_CG_Score.zip)
* [Mac OS](https://github.com/SebastienSiva/ITEC_D2L_TOOLS/raw/main/total_course_assessment/dist_zips/MacOS_CG_Score.zip)

Note: There may be several steps to overcome Windows/AntiVirus security. You may wish to run the gui from the command line (see below...)

Mac OS Notes: After trying to run the app and getting blocked, try going into Settings->Privacy and Security. There, under security, you will see the 'Run the App Anyways' option.

## Files Supported
The app uses 3 types of files to calculate course goal scores for a D2L section. Course goal scores are the percentage of students getting a 70% or better on course goal related assessment.

* **File_Type1** (>= 0 files): Quiz grade export CSV files with the *Question Title (a.k.a. Short Description)* or *Question Text* containing 1 or more course goal identifiers with exact format [GOAL X] where X is a number. Examples: [GOAL 3], [GOAL 4]

* **File_Type2** (0 or 1 file): The D2L gradebook exported as Points CSV with OrgId, FirstName, LastName.

* **File_Type3** (1 file only if File_Type2 present): CSV file mapping grades to course goals according to the following format:

    GRADE_NAME,CG,CG,CG,CG,CG  
    Final Exam,CG5,CG6,CG1  
    Asg 7,CG3,CG4
    
    Note: The first row must be the header and will be skipped for processing.
    
Note: We recommend you rename long file names to short file names.

## Command Line Options

1.  Feed this script 0 command line arguments and it will automatically search the directory for the files described above.

2.  Optionally include the files explicitly as command line arguments.

Ex: python3 cg_score.py path_to_quz1_cg.csv path_to_quz2_cg.csv path_to_gradebook.csv path_to_grade_cg_map.csv

Ex: python3 cg_score.py 2140_grade_cg.csv GB_Points.csv FinalExamMC.csv


[Video Tutorial](https://ggcedu-my.sharepoint.com/:v:/g/personal/ssiva_ggc_edu/EVO5HIB7c0dNhDJctyECUpEBp-8Sq5dzMNLDvScqeoeuOw?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=EXA3vG)


## Run gui from the command line
`pip install FreeSimpleGUI`

`python cg_score_gui.py`

## How to build the app
Build (on the corresponding OS) with:

`pyinstaller --noconsole --onefile cg_score_gui.py`

Note: On windows you may need to turn off Windows Defender to build.



