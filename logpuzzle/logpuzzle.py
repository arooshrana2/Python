#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def read_urls(filename):
        """Returns a list of the puzzle urls from the given log file,
        extracting the hostname from the filename itself.
        Screens out duplicate urls and returns the urls sorted into
        increasing order."""
        l = set([])
	print filename
	with open(filename, 'r') as f:
		for i in f:
			search = re.search(r'/puzzle/', i)
			if search:
				j = re.search(r'/\S*', re.search(r'GET\s\S*', i).group()).group()
				#print j
				l.add(j)
        # +++your code here+++
	ll = list(l)
	l = sorted(ll, key=lambda x : x.split('-')[-1])
	#print '\n'.join(l)
        return l

def download_images(img_urls, dest_dir):
	"""Given the urls already in the correct order, downloads
	each image into the given directory.
	Gives the images local filenames img0, img1, and so on.
	Creates an index.html in the directory
	with an img tag to show each local image file.
	Creates the directory if necessary.
	"""
	if not os.path.exists(os.path.abspath(dest_dir)):
		os.makedirs(dest_dir)
	os.chdir(dest_dir)
	j = 0
	for i in img_urls:
		urllib.urlretrieve('http://code.google.com'+i,'img'+str(j)+'.jpg')
		j+=1
	
 	with open('index.html', 'w') as index:
		index.write('<HTML>\n<BODY>\n')
	j = 0
	with open('index.html', 'a') as index:
		for i in img_urls:
			index.write(r'<img src="img'+str(j)+'.jpg">')
			j+=1
		index.write('</BODY>\n</HTML>')
	# +++your code here+++
  

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])
  if todir:
    download_images(img_urls, todir)
  else:
    pass#print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
