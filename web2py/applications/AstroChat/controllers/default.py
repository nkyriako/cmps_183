# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

from datetime import datetime
import datetime
import os

# Homepage
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("AstroChat")
    return dict(message=T('Welcome!'))

# ForumPage
def forum():
    return dict(table=None)


# User can edit profile here
def edit_profile():
    q = (db.user_table.user_email == auth.user.email)
    cl = db(q).select().first()
    
    if cl is not None:
        return dict(table=cl)
    else:
    #redirect(URL('default', 'index'))
        return dict(table=None)

def get_pic():
    q = (db.user_table.user_email == auth.user.email)
    cl = db(q).select().first().profile_picture
    return dict(pic=cl)

def submit():
    q = (db.user_table.user_email == auth.user.email)
    cl = db(q).select().first()

    # Already in the table (editing)    
    if cl is not None:
    	cl.update_record(birthday=request.vars.birthday, 
                         profile_picture=request.vars.picture,
                         bio=request.vars.bio,
      			 banner=request.vars.banner
                        )                  
   	if request.vars>0:
		#out_message = request.vars
                redirect(URL('default', 'index'))
    	else:
		out_message = "no post"
        response.flash = ("profile edited")
 
    # Not in the table yet (adding)
    else:
        db.user_table.insert(birthday=request.vars.birthday,
                             profile_picture=request.vars.picture,
                             bio=request.vars.bio,
			     banner=request.vars.banner
			    )			
	#out_message = "hold on"
        redirect(URL('default', 'index'))
        response.flash = ("profile added to table")
    return dict(message=out_message)   

def serve_file():
    filename = request.args(0)
    path = os.path.join(request.folder, 'uploads', filename)
    return response.stream(path)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


