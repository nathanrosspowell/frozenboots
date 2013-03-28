#!/usr/bin/python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# create_branch. Authored by Nathan Ross Powell.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import shutil
import distutils.dir_util
import sys
from subprocess import call
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Clone. 
def clone( user, repro, cloneFolderName ):
    arg = "git@github.com:%s/%s.git" % ( user, repro, )
    call( [ "git", "clone", arg, cloneFolderName ] )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Clone. 
def checkout( branch ):
    call( [ "git", "checkout", "--orphan", branch ] )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Clone. 
def clear():
    call( [ "git", "rm", "-rf", "." ] )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Clone. 
def create():
    with open( "index.html", 'w' ) as file:
        file.write( "<h1>My Github Page</h1>" )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Clone. 
def getPaths():
    currentDir = os.path.dirname( os.path.realpath( __file__ ) )
    path, dirName = os.path.split( currentDir )
    return path, currentDir, dirName
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Clone. 
def commitChanges( branch ):
    call( [ "git", "add", "." ] )
    call( [ "git", "commit", "-a", "-m", "[ADD] branch %s" % ( branch, ) ] )
    call( [ "git", "push", "origin", branch ] )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
def createNewBranch( user, repro, branch):
    path, devPath, devFolder = getPaths()
    cloneFolderName = "%s-%s" % ( repro, branch )
    clonePath = os.path.join( path, cloneFolderName )
    os.chdir( path )
    if not os.path.isdir( clonePath ):
        clone( user, repro, cloneFolderName )
        os.chdir( cloneFolderName )
        checkout( branch )
        clear()
        create()
        commitChanges( branch )
    else:
        print "Folder '%s' already exsits" % ( cloneFolderName, )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main script.
if __name__ == "__main__":
    import settings as FBS
    createNewBranch( FBS.USER, FBS.REPRO, FBS.BRANCH )
    
