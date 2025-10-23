from fman import DirectoryPaneCommand, ApplicationCommand, show_alert, YES, NO, FMAN_VERSION, DirectoryPaneListener, load_json, save_json, show_prompt
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

class CreateSymlink(DirectoryPaneCommand):
	def __call__(self):
		# Get selected files
		selected = self.pane.get_selected_files()
		if not selected:
			show_alert("No files selected")
			return
			
		source_url = selected[0]
		source_path = as_human_readable(source_url)
		
		# Get other pane path
		panes = self.pane.window.get_panes()
		this_pane = panes.index(self.pane)
		other_pane = panes[(this_pane + 1) % len(panes)]
		target_dir_url = other_pane.get_path()
		target_path = as_human_readable(target_dir_url) + '\\' + basename(source_url)
			
		# Determine if directory
		is_dir = os.path.isdir(source_path)
		
		# Build mklink command
		cmd = f'cmd /c mklink {"" if not is_dir else "/D"} "{target_path}" "{source_path}"'
		choice = show_alert(
			cmd + "\nDo you want to continue?",
			buttons=YES | NO,
			default_button=YES
		)
		if choice == NO:		
			return
		
		try:
			# Execute with elevation
			result = subprocess.run(cmd)
			if result.returncode == 0:
				show_alert("Symlink created successfully")
			else:
				show_alert(f"Error creating symlink: {result.stderr}")
		except Exception as e:
			show_alert(f"Error creating symlink: {str(e)}")
