from fman import DirectoryPaneCommand, ApplicationCommand, show_alert, FMAN_VERSION, DirectoryPaneListener, load_json, save_json, show_prompt
from fman.fs import copy, move, exists
from fman.clipboard import set_text
from fman.url import as_human_readable, basename
import subprocess
from subprocess import Popen
import os.path
import re

# static class
class Globals():
	# static array
	rememberList = []

class Autohotkey(DirectoryPaneCommand):
	def __call__(self):
		conemu_path = "E:\\fman.exe"
		current_path = self.pane.get_path()
		subprocess.call(f'"{conemu_path}" "{as_human_readable(current_path)}"')

class Duplicate(DirectoryPaneCommand):
	def __call__(self):
		paths = self.pane.get_selected_files()
		# iterate paths
		for path in paths:						
			name, ext = os.path.splitext(path)	
			# split string on underscore
			name_split = name.split("_")
			# get last element
			last_element = name_split[-1]
			
			# check if last element is a number
			if re.match(r'\d+', last_element):
				#show_alert(last_element)
				# all elements except last
				filename = name_split[:-1]
				# join elements
				filename = "_".join(filename)
				digitLength = len(last_element)
				digit = int(last_element)
				digit += 1
				digitString = str(digit)
				name = filename + "_" + digitString.zfill(digitLength)
				#show_alert(name)
				if exists(name + ext):
					show_alert("File already exists " + basename(name + ext))
					return
			else: 
				name = name + "_copy"

			copypath = name +  ext
			#show_alert(copypath)
			copy(path, copypath)
			
class FileListAddSelected(DirectoryPaneCommand):
	def __call__(self):
		paths = self.pane.get_selected_files()
		# add paths to copyPaths
		for path in paths:
			# check if path is already in copyPaths
			if path not in Globals.rememberList:
				Globals.rememberList.append(path)				

class FileListClear(DirectoryPaneCommand):
	def __call__(self):
		Globals.rememberList = []

class FileListShow(DirectoryPaneCommand):
	def __call__(self):
		# iterate paths
		output = ""
		for path in Globals.rememberList:
			output += as_human_readable(path) + "\n"

		show_alert(output)
				

class FileListCopyHere(DirectoryPaneCommand):
	def __call__(self):			
		current_path = self.pane.get_path()	
		for path in Globals.rememberList:
			baseName = basename(path)	
			copypath = current_path + "/" + baseName
			#show_alert(path + "---" + copypath)
			copy(path, copypath)
			
class FileListMoveHere(DirectoryPaneCommand):
	def __call__(self):			
		current_path = self.pane.get_path()	
		for path in Globals.rememberList:
			baseName = basename(path)	
			copypath = current_path + "/" + baseName
			#show_alert(path + "---" + copypath)
			move(path, copypath)


class CopyFolderpathToClipboard(DirectoryPaneCommand):
	def __call__(self):		
		path = self.pane.get_path()		
		set_text(as_human_readable(path))			

class CopyFolderpathPlusFilenameToClipboard(DirectoryPaneCommand):
	def __call__(self):
		folder_path = self.pane.get_path()
		selected = self.pane.get_selected_files()
		
		if not selected:
			set_text(as_human_readable(folder_path))
			return
			
		result = ""
		for path in selected:
			if result:
				result += "\n"
			result += as_human_readable(folder_path + "/" + basename(path))
			
		set_text(result)

class AddProjectFolder(DirectoryPaneCommand):
	def __call__(self):
		exe_path = "D:\\GIT\\Intern\\ProjectFolders\\ProjectFolders.exe"
		current_path = self.pane.get_path()
		#show_alert(as_human_readable(current_path))
		subprocess.call(f'"{exe_path}" "{as_human_readable(current_path)}"')		


	def get_file_paths(self):
		selection = self.pane.get_selected_files()
		if selection:
			return [as_human_readable(p) for p in selection]
		return [as_human_readable(self.pane.get_path())]
