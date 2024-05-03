#!/usr/bin/env python3
import traceback, os, webbrowser
import FreeSimpleGUI as sg
from cg_score import *


class CG_Score_GUI:

	def __init__(self):
		self.window = None
		self.cgs = CG_Score()

	def add_files(self, files):
		for f in files.split(";"):
			self.add_file(f) 

	def add_file(self, f):
		first_file = self.cgs.hasNoFiles()

		r = self.cgs.process_file(f)
		if r.startswith("ERROR"): 
			self.error_popup(r)
		else:
			file_box = self.window['gui_current_files_text']
			file_data = "%s: %s" % (r, os.path.basename(f))
			if first_file: file_box.update(file_data)	
			else: file_box.update(file_box.get() + '\n' + file_data)

			stats_box = self.window['gui_stats_text']
			r = self.cgs.processGradeBook()
			if r != "": stats_box.update(r)
			else:
				self.window['gui_process_btn'].update(disabled=False)
				stats_box.update("Ready To Process")

	def process_files(self):
		stats_box = self.window['gui_stats_text']
		self.show_filter_students()
		self.cgs.calc_num_students_pass()
		stats_box.update(self.cgs.get_stats_str())
		self.window['gui_process_btn'].update(disabled=True)
		self.window['gui_browse_files_btn'].update(disabled=True, button_color="grey")
		
	
	def show_filter_students(self):
		unignore = []
		for sid in self.cgs.ignored_students:
			s = ""
			for reason in self.cgs.ignored_students[sid]: s += ('\t- ' + reason + '\n')
			event, values = sg.Window("Remove Student",
				[
					[sg.Text(sid + " issues:", size=40)],
					[sg.Text(s)],
					[sg.Push(), sg.Text('Remove ' + sid + '?'), sg.Button('Keep'), sg.Button('Remove')]
				]).read(close=True)
			if event == 'Keep': unignore.append(sid)
		
		for sid in unignore: del self.cgs.ignored_students[sid]

		self.cgs.filter_students()
	
	
	def error_popup(self, msg):
		sg.Window('Error...', 
			[[sg.Text(msg)], [sg.Push(), sg.Button('Ok')]]).read(close=True)			

#####################MAIN#######################
	def main(self):
		# sg.ChangeLookAndFeel('Dark') 	
		sg.theme('DefaultNoMoreNagging')
		sg.set_options(font=('Any', 12))

		try:
			"""
			upload_layout = [
				[sg.Text("Upload a D2L CSV File")],
				[
					sg.In(size=(63, 1), key='gui_file_input'),
					sg.Push(),
					sg.FilesBrowse(file_types=(("CSV File", "*.csv"),), target='gui_file_input'),
					sg.Button('Upload', key='gui_upload_btn')
				],
			]
			"""
			
			current_files_layout = [
				[sg.Multiline("No Files Yet...", disabled=True, no_scrollbar=True, 
					size=(80, 4), key='gui_current_files_text')],
				[sg.Push(),
					sg.In(size=(1, 1), key='gui_file_input', visible=False, change_submits=True),
					sg.FilesBrowse('Add Files...', file_types=(("CSV File", "*.csv"),), 
						key='gui_browse_files_btn', target='gui_file_input'),
					sg.Button('Process', key='gui_process_btn', 
						disabled=True, disabled_button_color="grey")]
			]
			
			stats_layout = [
				[sg.Multiline("No Yet...", disabled=True, no_scrollbar=True, 
					size=(80, 10), key='gui_stats_text')]
			]

			last_layout = [
				[
					sg.Push(), 
					sg.Button('ReStart', key='gui_reset_btn'),
					sg.Button('Help', key='gui_help_btn'),
					sg.Button('Quit', key='gui_quit_btn'),
				]
			]

			# Create the window
			self.window = sg.Window('Course Goal Scorer', [
				#[sg.Frame("File Upload", upload_layout, expand_x=True)], 
				[sg.Frame("Files To Process", current_files_layout, expand_x=True)],
				[sg.Frame("Data Analysis", stats_layout, expand_x=True)],
				last_layout
			])
			
			while True:
				event, values = self.window.read()
				if event == 'gui_file_input':
					self.add_files(values['gui_file_input'])
				elif event == 'gui_process_btn':
					self.process_files()
				elif event == 'gui_reset_btn':
					self.cgs = CG_Score()
					self.window.close()
					self.main()
				elif event == 'gui_help_btn':
					webbrowser.open(DOCUMENTATION)
				elif event == 'gui_quit_btn' or event == sg.WIN_CLOSED:
					break		
			self.window.close()
			
		except (FileNotFoundError, IOError) as e:
			self.error_popup(str(e) + "\nApp Must Be Restart...")
		except BaseException as e:
			self.error_popup(traceback.format_exc() + "\nApp Must Be Restart...")


if __name__ == "__main__":
	sgui = CG_Score_GUI()
	sgui.main()
	