import os
import sqlite3
from contextlib import closing
from flaskext.flatpages import FlatPages
from flask import   \
Flask,              \
request,            \
session,            \
g,                  \
redirect,           \
url_for,            \
abort,              \
render_template,    \
flash

#-----------------------------------------------------------------------------
# Create the app.
app = Flask( __name__ )
app.config.from_pyfile( "settings.cfg" )
pages = FlatPages( app )

#-----------------------------------------------------------------------------
# Import views.
import website.views
