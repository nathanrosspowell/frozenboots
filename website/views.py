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
index_html = "base.html"
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
def compute( x, type, y ):
    return eval( "x %s y " % ( type, ) )
app.jinja_env.tests.update( compute = compute )
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
# Helpers.
def create_navbar_structure():
    navbar = {}
    mainDir = directory()
    isMd = lambda x: os.path.splitext( x )[ 1 ] in ( ".md", ".markdown", )
    name = lambda x: os.path.splitext( x )[ 0 ] 
    for root, dirs, files in os.walk( mainDir ):
        baseDir = root.replace( mainDir, "" ).replace( "/", "" )
        navbar[ baseDir ] = [ name( file ) for file in files if isMd( file ) ]
    return navbar
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helpers.
def create_navbar():
    navbar = {}
    getPage = lambda x, y: pages.get_or_404( os.path.join( x, y ) )
    getTitle = lambda x, y: getPage( x, y ).meta.get( "title", x )
    for key, value in create_navbar_structure().items(): 
        alphaSort = [] 
        dateSort = []
        for item in value:
            path = os.path.join( key, item )
            itemMeta = pages.get_or_404( path ).meta
            title = itemMeta.get( "title", item )
            sort = itemMeta.get( "published", title )
            data = {
                "title" : title,
                "path" : path,
                "sort" : sort,
            }
            if sort != title: 
                dateSort.append( data )    
            else:
                alphaSort.append( data )
        sorter = lambda k: k[ "sort" ]
        sortedAlpha = sorted( alphaSort ,key = sorter  ) 
        sortedDates = sorted( dateSort, key = sorter, reverse = True )
        navbar[ key ] = sortedDates + sortedAlpha 
    return navbar
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def base_render_template( template, **kwargs ):
    wdatetime = get_w3c_date()
    date = makedate( wdatetime[ :10 ].replace( "-", "/" ) )
    stime = wdatetime[ 11:19 ]
    addition = wdatetime[ 19: ]
    kwargs[ "date" ] = date
    kwargs[ "year" ] = date[ :4 ]
    timezone = get_time_zone()
    if timezone.upper() == "GMT":
        kwargs[ "time" ] = "%s %s" % ( 
            stime, 
            timezone,
        ) 
    else:
        kwargs[ "time" ] = "%s %s. Which is %s UTC/GMT" % ( 
            stime, 
            timezone,
            get_gmt_time(), 
        ) 
    navbar = create_navbar()
    navbarTuples = sorted( navbar.iteritems(), key = operator.itemgetter( 0 ) )
    kwargs[ "navbar" ] = navbarTuples
    kwargs[ "title" ] = app.config[ "TITLE" ]
    kwargs[ "google_analytics" ] = app.config[ "GOOGLE_ANALYTICS" ]
    article = kwargs.get( "article", False )
    if article:
        articlePath = kwargs.get( "article_path", "" )
        if "/" in articlePath:
            navKey, navValue = articlePath.split( "/" )
            kwargs[ "menu_selected" ] = navKey 
        else:
            navKey = ""
            navValue = articlePath
            kwargs[ "menu_selected" ] = articlePath 
        tuples = navbar[ navKey ]
        navIndex = -1
        for i, navDict in enumerate( tuples ):
            if navDict[ "path" ] == articlePath:
                navIndex = i
                break
        prev = None
        next = None
        if -1 < navIndex < len( tuples ):
            if 0 < navIndex:
                prev = pages.get_or_404( tuples[ navIndex - 1 ][ "path" ] )
            if navIndex + 1 < len( tuples ):
                next = pages.get_or_404( tuples[ navIndex + 1 ][ "path" ] )
        kwargs[ "previous_article" ] = prev
        kwargs[ "next_article" ] = next
    return render_template( template, **kwargs )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def article_page( template, page_path ):
    pageMd = pages.get_or_404( page_path )
    pageMeta = pageMd.meta
    if pageMeta.get( "comments", False ):
        comment_id = "/%s/" % pageMd
        comment_title = pageMeta.get( "title", "No Title" )
    else:
        comment_id = None
        comment_title = None
    return base_render_template( template,
            article = pageMd,
            article_path = page_path,
            comment_override_id = comment_id,
            comment_override_title = comment_title,
    )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Redirects.
@app.route('/')
def index():
    return base_render_template( index_html )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route( "/<path:page_path>/" )
def page( page_path ):
    return article_page( "article.html", page_path )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route( "/feeds/atom.xml" )
def atom():
    blogs = [ post for post in all_pages( directory(), "blog" ) ]
    with open( "website/feed_content.txt", 'r' ) as feed_cache:
        cache_blogs = feed_cache.readlines()
    changed = False
    if len( blogs ) != len( cache_blogs ):
        changed = True
    if not changed:
        for index, blog in enumerate( blogs ):
            if blog.path != cache_blogs[ index ].strip():
                changed = True
                break
    if changed:
        w3c_update = get_w3c_date()
        with open( "website/feed_content.txt", 'w' ) as new_feed:
            new_feed.writelines( [ blog.path+"\n" for blog in blogs ] )
        with open( "website/feed_time.txt", 'w' ) as new_time:
            new_time.write( w3c_update )
    else:
        with open( "website/feed_time.txt", 'r' ) as cache_time:
            w3c_update = cache_time.read().strip()
    return base_render_template( atom_xml,
        pages = blogs,
        w3c_update = w3c_update
    ), 200, {'Content-Type': 'application/atom+xml; charset=utf-8'}
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
