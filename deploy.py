#!/usr/bin/python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# deploy. Authored by Nathan Ross Powell.
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
    call( [ "git", "checkout", branch ] )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Clone. 
def getPaths():
    currentDir = os.path.dirname( os.path.realpath( __file__ ) )
    path, dirName = os.path.split( currentDir )
    return path, currentDir, dirName
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Clone. 
def copyFiles( src, dst ):
    #shutil.rmtree( dst )
    distutils.dir_util.copy_tree( src, dst )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Clone. 
def removeBranch( src ):
    shutil.rmtree( src )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Clone. 
def commitChanges( message ):
    call( [ "git", "add", "." ] )
    call( [ "git", "commit", "-m", message ] )
    call( [ "git", "push" ] )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
def moveToDeployRepro( user, repro, branch, commitMessage ):
    path, devPath, devFolder = getPaths()
    cloneFolderName = "%s-%s" % ( repro, branch )
    clonePath = os.path.join( path, cloneFolderName )
    os.chdir( path )
    if not os.path.isdir( clonePath ):
        clone( user, repro, cloneFolderName )
        os.chdir( cloneFolderName )
        checkout( branch )
        os.chdir( path )
    websitePath = os.path.join( devPath, "website" )
    buildPath = os.path.join( websitePath, "build" )
    copyFiles( buildPath, clonePath )
    os.chdir( cloneFolderName )
    commitChanges( commitMessage )
    removeBranch( clonePath )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main script.
if __name__ == "__main__":
    import settings as FBS
    try:
        commitMessage = sys.argv[ 1 ]
    except:
        print 'supply a commit message e.g. "New files"'
        commitMessage = None
    if commitMessage:
        moveToDeployRepro( FBS.USER, FBS.REPRO, FBS.BRANCH, commitMessage )
    
