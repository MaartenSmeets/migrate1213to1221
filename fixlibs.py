import os
import sys
from shutil import copyfile

compositebasepath = sys.argv[1]
librarypath = sys.argv[2]

print "Composite base path: "+str(compositebasepath)
print "Library path: "+str(librarypath)


def get_filepaths(directory):
    return os.popen("find "+str(directory)).readlines()

# Run the above function and store its results in a variable.   
full_file_paths = get_filepaths(compositebasepath)
print "Files to process: "+str(full_file_paths)
copylibs=False
for filename in full_file_paths:
	print "Checking file: "+str(filename.rstrip())
	if str(filename.rstrip()).endswith(".bpel"):
		print "BPEL found: "+str(filename.rstrip())
		if 'bpelx:exec' in open(filename.rstrip()).read():
			print "Found Java embedding"
			copylibs = True
			break

if copylibs:
	libdir = str(compositebasepath)+"/SOA/SCA-INF/lib"
	if not os.path.isdir(libdir):
		print "Creating directory: "+libdir
		os.makedirs(libdir)
	for file in get_filepaths(librarypath):
		if str(file).rstrip().endswith(".jar"):
			print "Copying library from: "+str(file.rstrip())+" to "+libdir
			shutil.copy(file.rstrip(), libdir)
		else:
			print "Ignoring file: "+str(file).rstrip()
else:
	print "No Java embedding found"