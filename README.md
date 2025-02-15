# fman-xd-plugins

A collection of utility commands for the [fman](https://fman.io) file manager.

## Features

### File Path Commands

- **Copy folderpath to clipboard**: Copies the current folder path to clipboard
- **Copy folderpath + filename to clipboard**: Copies the current folder path combined with any selected filenames to clipboard
  - If files are selected: Combines folder path with each selected filename
  - If no files selected: Just copies the folder path

### File List Operations

- **File List Add Selected**: Adds selected files/folders to a temporary list for batch operations
- **File List Clear**: Clears the temporary file list
- **File List Show**: Displays all paths currently stored in the file list
- **File List Copy Here**: Copies all files from the list to the current folder
- **File List Move Here**: Moves all files from the list to the current folder

### File Management

- **Duplicate**: Creates a copy of selected files with intelligent naming
  - For files with numeric suffixes (e.g., "file_001.txt"): Increments the number
  - For other files: Adds "\_copy" to the filename

### External Tools Integration

- **Autohotkey**: Opens the current path in fman.exe
- **Add Project Folder**: Integrates with ProjectFolders.exe for project management
