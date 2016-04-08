import commands
import sys

def listdir(dir, cmd):
    """ Given a dir path this function runs the external command cmd"""
    print 'Command to run:', cmd
    (status, output) =commands.getstatusoutput(cmd)
    if status: # If status is not zero there is an error
        sys.stderr.write(output)
        sys.exit(1)
    print output

def main():
    listdir('.', 'ls -l') # This words
    listdir('.', 'ls -\\') # This fails

if __name__ == '__main__' :
    main()