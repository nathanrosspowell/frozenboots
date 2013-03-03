#!/usr/bin/python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# views. Authored by Nathan Ross Powell.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import datetime
import operator
import urllib2
import time
from time_stamp import                      \
get_w3c_date,                               \
get_time_zone,                              \
get_gmt_time
from flaskext.markdown import Markdown
from website import                         \
app,                                        \
pages
from flask import                           \
Flask,                                      \
request,                                    \
session,                                    \
g,                                          \
redirect,                                   \
url_for,                                    \
abort,                                      \
render_template,                            \
flash
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Markdown set up.
Markdown(app)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up. 
index_html = "boilerplate.html"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Jinja2 additions.
def getkey( d, key ):
    e = "_ERROR_"
    r = d.get( key, e )
    if r == e:
        print "\tDEBUG: asked for", key
        print "\tDEBUG: dic:", dic
        return "0"
    return r
app.jinja_env.globals.update( getkey = getkey )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def compare( x, type, y ):
    return eval( "x %s y " % ( type, ) )
app.jinja_env.tests.update( compare = compare )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def makedate( value ):
    ret = ""
    year = ""
    month = ""
    day = ""
    for i, part in enumerate( value.split( "/" ) ):
        if i == 0:
            year = part
        elif i == 1:
            month = ", %s" % getdate( part, "month" )
        elif i == 2:
            day = getdate( part, "day" )
    return "%s%s %s" % ( year, month, day )
app.jinja_env.globals.update( makedate = makedate )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getdate( value, type ):
    if type == "month":
        return [ "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ][ int( value ) - 1 ]
    elif type == "day":
        day = str( int( value ) )
        post = "th"
        if day != "11" and day != "12" and day != "13":
            if day[ -1 ] == "1":
                post = "st"
            elif day[ 0 ] == "2":
                post = "nd"
            elif day[ 0 ] == "3":
                post = "rd"
        return "%s%s" % ( day, post, )

    return "_ERROR_"
app.jinja_env.globals.update( getdate = getdate )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def equalto( x, y ):
    return x == y
app.jinja_env.tests.update( equalto = equalto )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_tagged_blogs( tag ):
    if tag not in get_tags()[ 0 ]:
        return []
    return [ post for post in tag_pages( tag) ]
app.jinja_env.globals.update( get_tagged_blogs = get_tagged_blogs )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helpers.
def directory():
    return os.path.join( app.config[ "ROOT_DIR" ],
        app.config[ "FLATPAGES_ROOT" ]
    )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def base_render_template( template, **kwargs ):
    wdatetime = get_w3c_date()
    date = makedate( wdatetime[ :10].replace( "-", "/" ) )
    stime = wdatetime[ 11:19 ]
    addition = wdatetime[ 19: ]
    kwargs[ "date" ] = date
    timezone = get_time_zone()
    if timezone.upper() == "GMT":
        kwargs[ "time" ] = "%s %s" % ( 
            stime, 
            timezone,
        ) 
    else:
        kwargs[ "time" ] = "%s %s which is %s UTC/GMT" % ( 
            stime, 
            timezone,
            get_gmt_time(), 
        ) 
    kwargs[ "credits" ] = pages.get_or_404( "menu/credits-short" )
    kwargs[ "bio" ] = pages.get_or_404( "menu/bio" )
    return render_template( template, **kwargs )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def article_page( template, page_list, *args, **kwargs ):
    pages_list = list( pages.get_or_404( name ) for name in page_list )
    title = pages_list[ 0 ]
    if pages_list[ 0 ].meta.get( "comments", False ):
        comment_id = "/%s/" % page_list[ 0 ]
        comment_title = title.meta.get( "title", "No Title" )
    else:
        comment_id = None
        comment_title = None
    return base_render_template( template,
            pages = pages_list,
            comment_override_id = comment_id,
            comment_override_title = comment_title,
            *args,
            **kwargs
    )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Key word arg helpers.
def code_kwargs( page_path, page ):
    readme = page.meta.get( "readme", None )
    if readme:
        responce = urllib2.urlopen( readme )
        readme = responce.read()
    kwargs = {
        "readme" : readme, 
    }
    return kwargs
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def blog_kwargs( page_path, page ):
    kwargs = {}
    blogs = [ post for post in all_pages( directory(), "blog" ) ]
    length = len( blogs )
    index = -1
    for blog in blogs:
        if blog.path == page.path:
            index = blogs.index( blog )
            break
    if index > -1:
        prevBlog  = index - 1
        if prevBlog >= 0:
            kwargs[ "nextBlog" ] = blogs[ prevBlog ]
        nextBlog = index + 1
        if nextBlog < length:
            kwargs[ "prevBlog" ] = blogs[ nextBlog ]
    return kwargs
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Redirects.
@app.route('/')
def index():
    return article_page( index_html, ( "menu/home-page", ) )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route( "/<path:page_path>/" )
def page( page_path ):
    page = pages.get_or_404( page_path )
    template = page.meta.get( "template", blog_post_html )
    spliturl = page_path.split( "/" )
    kwargs = {}
    if len( spliturl ) > 1:
        if spliturl[ 0 ] == "blog":
            kwargs = blog_kwargs( page_path, page )
        elif spliturl[ 0 ] == "code":
            kwargs = code_kwargs( page_path, page )
    return blog(
        template = template,
        page_list = [ page ],
        **kwargs
    )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Error pages.
@app.errorhandler( 404 )
def page_not_found( e ):
    return base_render_template( "error.html", details = e, error="404" )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route( "/404.html" )
def error404():
    return base_render_template( "error.html", error="404" )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.errorhandler( 403 )
def page_not_found( e ):
    return base_render_template( "error.html", details = e, error="403" )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route( "/403.html" )
def error403():
    return base_render_template( "error.html", error="403" )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.errorhandler( 410 )
def page_not_found( e ):
    return base_render_template( "error.html", details = e, error="410" )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route( "/410.html" )
def error410():
    return base_render_template( "error.html", error="410" )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.errorhandler( 500 )
def page_not_found( e ):
    return base_render_template( "error.html", details = e, error="500" )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route( "/500.html" )
def error500():
    return base_render_template( "error.html", error="500" )