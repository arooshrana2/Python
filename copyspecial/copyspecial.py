#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import commands
from zipfile import ZipFile
"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them
def get_special_paths(path):
	#print path
	#ls = os.popen('ls -f').readlines()
	ls = os.listdir(path)
	#print ls
	paths = []
	#regex = re.compile(r'\n')
		
	for i in ls:
		#print i
		#if os.path.isfile(i):
		regex =  re.search(r'__\w+__', i)
		if regex:
			paths.append(os.path.abspath(os.path.join(path, i)))
	#print "PATHS", paths	
	return paths
	
def copy_to(paths, todir):
	if not os.path.exists(os.path.abspath(todir)):
		os.makedirs(todir)
	for i in paths:
		shutil.copy(i, os.path.abspath(todir))

def zip_to(paths, tozip):
	if not os.path.exists(os.path.abspath(tozip)):
		os.makedirs(os.path.abspath(tozip))
	'''zf = ZipFile('%s.zip' %(tozip), 'w')
	for i in paths:
		abs_src = os.path.abspath(i)
		for dirname, subdirs, files in os.walk(i):
			for filename in files:
				absname = os.path.abspath(os.apth.join(dirname, filename))
				arcname = absname[len(abs_src) + 1:]
				zf.write(absname, arcname)
	zf.close()'''
	
	#os.chdir(os.path.abspath(tozip))
	print os.getcwd()
	zipFile = ZipFile('Folder.zip', 'w')
	with zipFile as z:
		for i in paths:
			new_file = os.path.join(os.getcwd(), i.split('/')[-1])
			print "NEW FILE :-> ", new_file
			if os.path.isfile(i):
				z.write(i.split('/')[-1])
			else:
				print i, ' --> not available'
	shutil.move(zipFile, tozip)
	
def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if len(args) == 0:
    print "error: must specify one or more dirs"
    sys.exit(1)

  # +++your code here+++
  paths = get_special_paths(args[0])
  if todir != '':
    copy_to(paths, todir)
  if tozip != '':
    zip_to(paths, tozip)
  # Call your functions
  
if __name__ == "__main__":
  main()
