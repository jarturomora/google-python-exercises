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
import collections

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
  # +++your code here+++
  # Define server name    
  server = 'http://' + filename.split('_')[1]
  images_urls = {}

  logfile = open(filename)
  pattern = r'\.*"GET (\S*/puzzle\S*)(-)(\S*.jpg)'  
  for logentry in logfile:
    image = re.search(pattern, logentry)
    if image and server + image.group(3) not in images_urls.values():
      img_url = server + image.group(1) + image.group(2) + image.group(3)      
      images_urls[image.group(3)] = img_url

  logfile.close()
  images_urls = collections.OrderedDict(sorted(images_urls.items())) 

  return images_urls

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++
  # Verify if destination directory exists. We supose the directory is created
  # in the same location where the script is run
  if not os.path.exists(dest_dir):
    os.mkdir(dest_dir)
    print "INFO: The '%s' directory didn't exist so it was created." % dest_dir
  # Download images
  i = 0
  html_file = """<verbatim>
<html>
<body>
  """
  print """
  **********************************************************
  We are going to start downloading the images of the puzzle
  **********************************************************
  """
  for img, url in img_urls.items():
    print 'Downloading image: ', url , '...'
    dest_image = dest_dir + '/img' + str(i) + '.jpg'    
    urllib.urlretrieve(url, dest_image)
    print "    The image '%s' was successfully downloaded :-)\n" % img
    html_file += "<img src='" + 'img' + str(i) + ".jpg'>"
    i += 1
  print '\nINFO: All the images were successfully downloaded'
  html_file += '\n</body>\n</html>'
  index_html = open(dest_dir + '/index.html', 'w')
  index_html.write(html_file)
  index_html.close()
  print 'INFO: The index.html file was created.'
  return

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
    print '\n'.join(img_urls.values())

if __name__ == '__main__':
  main()
