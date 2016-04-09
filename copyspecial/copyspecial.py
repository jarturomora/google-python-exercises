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

"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them
def get_special_paths(dir):
  """Returns a list of the absolute paths of the special files in the given
  directory. We'll say that a "special" file is one where the name contains
  the pattern __w__ somewhere, where the w is one or more word chars."""
  # Get all the files in the given dir
  files = os.listdir(dir)
  files = '\n'.join(files) + '\n'
  # Gell all the files with the patten "__foo__" in any part of the filename
  pattern = r'.*__.*__.*'
  special_files = re.findall(pattern, str(files))
  result = ''
  for file in sorted(special_files):
    result += os.path.abspath(file) + '\n'
  return result

def create_directory(dir):
  """Creates the full path of a given directory"""
  if not '/' in dir:
      os.mkdir(dir)
  else:
    dirs = dir.split('/')
    new_dir = ''
    for d in dirs:
      if d != '':
        new_dir += d + '/'
        os.mkdir(new_dir)
  print "INFO: The Directory '%s' was successfully created." % dir
  return

def copy_to(paths, dir):
  """Given a list of paths, copies all the special files into the given
  directory."""
  # Validate if the destination directory exists, if not we create it
  if not os.path.exists(dir):
    create_directory(dir)
  # Copy the files from the origin directory to the destination path.
  try:
    special_files = get_special_paths(paths)
    special_files = special_files.split('\n')
    del special_files[-1]
    for f in special_files:      
      shutil.copy(f, dir)
    print """
          INFO: All the files in the directory '%s' were copied to '%s'
          """ % (paths, dir)
  except:
    print "Unexpected error:", sys.exc_info()[0]  
  return

def zip_to(paths, zippath):
  """Given a list of paths, zip those files up into the given zipfile."""
  files = ' '.join(paths)
  command = "zip -j %s %s" % (zippath, files)
  print "Command I'm going to do: ", command
  if os.path.exists(os.path.dirname(zippath)) or os.path.dirname(zippath) == '':    
    (status, output) = commands.getstatusoutput(command)
    if status:
      print "Unexpected error: ", output
    else:
      print "zip result: ", output
  else:
    print "zip I/O error: No such file or directory"
    print "zip error: Could not create output file (%s)" % zippath
  return

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
  # Call your functions
  if todir != '':
    copy_to(args[0], todir)
  elif tozip != '':
    zip_to(args[0:], tozip)
  else:
    print get_special_paths(args[0])
  
if __name__ == "__main__":
  main()
