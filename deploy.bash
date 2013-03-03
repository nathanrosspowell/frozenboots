#!/usr/bin/env sh
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# deploy. Authored by Nathan Ross Powell.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
./freeze.py
pushd ..
if [[ ! -d frozenboots-gh-pages ]]
then
    git clone git@github.com:nathanrosspowell/frozenboots.git frozenboots-gh-pages
fi
