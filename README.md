# PythonSiemensToolBoxLibrary

This is almost a ripoff of the https://github.com/dotnetprojects/DotNetSiemensPLCToolBoxLibrary only it is written i python.
it is a work in progres

from projectFiles import Step7ProjectV5

project = Step7ProjectV5(r"\testproject.s7p") \
  reads the program header

project.load() \
    loads the project and reads in all, programfolders, Interfaces

project.s7programFolders \
    returns all found programfolders (sources, blocks)


folders = {key:value for key, value in project.s7ProgrammFolders.items() if value.parent} \
    to find s7programFolders that are connected to a CPU we see if folder has a parent (a cpu),
    most cases only one folder is connected to a cpu

folder = s7programFolders[1] \
    select desirable folder:

folder.load() \
    loads all blocks in this folder, and returns a list of available blocks
    todo: no only contains OfflineFolder (Online, Sourses)


blocks = folder.blockOfflineFolder.blockList \
    returns all blockes in the offline folder

block = blocks["DB100] \
    returns block info on selected block

block.layout \
    returns layout of selected block
    
    
