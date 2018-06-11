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
    month = None
    day = None
    sign = None
    curruser=None
    urlnum=None
    if auth.user is not None:
    	curruser=db(db.user_table.user_email == auth.user.email).select().first()
    if curruser is not None:
    	month = curruser.birthday.month
    	day = curruser.birthday.day

    	if month == 1:
    		if day <= 19:
    			sign = "Capricorn"
    			urlnum = 10
    		else:
    			sign = "Aquarius"
    			urlnum = 11
    	elif month == 2:
    		if day <= 18:
    			sign = "Aquarius"
    			urlnum = 11
    		else:
    			sign = "Pisces"
    			urlnum = 12
    	elif month == 3:
    		if day <= 20:
    			sign = "Pisces"
    			urlnum = 12
    		else:
    			sign = "Aries"
    			urlnum = 1
    	elif month == 4:
    		if day <= 19:
    			sign = "Aries"
    			urlnum = 1
    		else:
    			sign = "Taurus"
    			urlnum = 2
    	elif month == 5:
    		if day <= 20:
    			sign = "Taurus"
    			urlnum = 2
    		else:
    			sign = "Gemini"
    			urlnum = 3
    	elif month == 6:
    		if day <= 20:
    			sign = "Gemini"
    			urlnum = 3
    		else:
    			sign = "Cancer"
    			urlnum = 4
    	elif month == 7:
    		if day <= 22:
    			sign = "Cancer"
    			urlnum = 4
    		else:
    			sign = "Leo"
    			urlnum = 5
    	elif month == 8:
    		if day <= 22:
    			sign = "Leo"
    			urlnum = 5
    		else:
    			sign = "Virgo"
    			urlnum = 6
    	elif month == 9:
    		if day <= 22:
    			sign = "Virgo"
    			urlnum = 6
    		else:
    			sign = "Libra"
    			urlnum = 7
    	elif month == 10:
    		if day <= 22:
    			sign = "Libra"
    			urlnum = 7
    		else:
    			sign = "Scorpio"
    			urlnum = 8
    	elif month == 11:
    		if day <= 21:
    			sign = "Scorpio"
    			urlnum = 8
    		else:
    			sign = "Sagittarius"
    			urlnum = 9
    	elif month == 12:
    		if day <= 21:
    			sign = "Saggittarius"
    			urlnum = 9
    		else: 
    			sign = "Capricorn"
    			urlnum = 10

    	else:
    		sign = None
    response.flash = T("AstroChat")
    return dict(message=T('Welcome!'),curruser=curruser, sign=sign, urlnum=urlnum)

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


