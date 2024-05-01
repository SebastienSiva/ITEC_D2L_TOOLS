#!/usr/bin/env python3
import traceback, os
import FreeSimpleGUI as sg

class CG_Score_GUI:

	def __init__(self):
		self.window = None
		self.file_names = []

	def add_file(self, f):
		self.file_names.append(f)
		self.window['gui_current_files_text'].update('\n'.join(
			(os.path.basename(x) for x in self.file_names)))
	
	def error_popup(self, msg):
		sg.Window('Error...', 
			[[sg.Text(msg)], [sg.Push(), sg.Button('Ok')]]).read(close=True)			

#####################MAIN#######################
	def main(self):
		# sg.ChangeLookAndFeel('Dark') 	
		sg.theme('DefaultNoMoreNagging')
		sg.set_options(font=('Any', 12))

		try:
			upload_layout = [
				[sg.Text("Upload a D2L CSV File")],
				[
					sg.In(size=(63, 1), key='gui_file_input'),
					sg.Push(),
					sg.FileBrowse(file_types=(("CSV File", "*.csv"),), target='gui_file_input'),
					sg.Button('Upload', key='gui_upload_btn')
				],
			]
			
			current_files_layout = [
				[sg.Multiline("No Files Yet...", disabled=True, no_scrollbar=True, 
					size=(80, 5), key='gui_current_files_text')]
			]

			last_layout = [
				[
					sg.Push(), 
					sg.Button('Reset All', key='gui_rest_btn'),
					sg.Button('Quit', key='gui_quit_btn'),
				]
			]

			# Create the window
			self.window = sg.Window('Course Goal Scorer', [
				[sg.Frame("File Upload", upload_layout, expand_x=True)], 
				[sg.Frame("Processed Files", current_files_layout, expand_x=True)],
				last_layout
			])
			
			while True:
				event, values = self.window.read()
				if event == 'gui_upload_btn':
					self.add_file(values['gui_file_input'])
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
	