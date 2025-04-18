# Course Goal Assessment App

[Video Tutorial](https://ggcedu-my.sharepoint.com/personal/ssiva_ggc_edu/_layouts/15/stream.aspx?id=%2Fpersonal%2Fssiva%5Fggc%5Fedu%2FDocuments%2FMS%5FStream%5FVideos%2FITEC%5FD2L%5FCourseGoalAssessment%2Emp4&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&ga=1&referrer=StreamWebApp%2EWeb&referrerScenario=AddressBarCopied%2Eview%2E06967dd4%2D3c86%2D47df%2D81df%2D53df17a0974e)

[Issue Tracker](https://github.com/SebastienSiva/ITEC_D2L_TOOLS/issues)

[FAQ](https://github.com/SebastienSiva/ITEC_D2L_TOOLS/blob/main/total_course_assessment/FAQ.md)


## Download The GUI
* [Windows](https://github.com/SebastienSiva/ITEC_D2L_TOOLS/raw/main/total_course_assessment/dist_zips/Windows_CG_Score.zip)
* [Mac OS](https://github.com/SebastienSiva/ITEC_D2L_TOOLS/raw/main/total_course_assessment/dist_zips/MacOS_CG_Score.zip)

Note: There may be several steps to overcome Windows/AntiVirus security. You may wish to run the gui from the command line (see below...)

Mac OS Notes: After trying to run the app and getting blocked, try going into Settings->Privacy and Security. There, under security, you will see the 'Run the App Anyways' option.

## Files Supported
The app uses 3 types of .CSV files to calculate course goal scores for a D2L section. Course goal scores are the percentage of students getting a 70% or better on course goal related assessment.

* **File_Type1** (>= 0 files): Quiz grade export CSV files with the *Question Title (a.k.a. Short Description)* or *Question Text* containing one or more course goal identifiers with exact format [GOAL X] where X is a number. Examples: [GOAL 3], [GOAL 4]

* **File_Type2** (0 or 1 file): The D2L gradebook exported as Points CSV with OrgId, FirstName, LastName. Make sure no grades are blank.

* **File_Type3** (1 file only if File_Type2 present): CSV file mapping grades to course goals according to the following format:

    GRADE_NAME,CG,CG,CG,CG,CG  
    Final Exam,CG5,CG6,CG1  
    Asg 7,CG3,CG4
    
    Note: The first row must be the header and will be skipped for processing.
    
Tips:
* Avoid using Excel (as it removes zeroes from IDs recognized as numbers).
* Rename long file names to short file names.

## Run gui from the command line

Normally you should be able to double click the GUI app icon and it will run, but in case that fails, you can open a terminal/shell and use the following commands (assuming Python3 is correctly installed).

`python -m pip install FreeSimpleGUI`

`python cg_score_gui.py`

## How to build the app
Build (on the corresponding OS) with:

`pyinstaller --noconsole --onefile cg_score_gui.py`

Note: On windows you may need to turn off realtime *Virus & Threat Protection* Settings / Windows Defender to build.



