#!/usr/bin/env sh
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# deploy. Authored by Nathan Ross Powell.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
./freeze.py
pushd ..
if [[ ! -d frozenboots-gh-pages ]]
then
    git clone git@github.com:nathanrosspowell/frozenboots.git frozenboots-gh-pages
    pushd frozenboots-gh-pages
    git checkout gh-pages 
    popd
fi
cp -r frozenboots-flask/website/build/* frozenboots-gh-pages/
pushd frozenboots-gh-pages 
git add *
git commit -m "$@"
git push 
popd
popd
