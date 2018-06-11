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
import json

import requests


def index_2():
	return dict(message=T('Welcome!'))
# Homepage
def index():
	curruser=None
	month = None
	day = None
	sign = None
	base_year_url = "http://horoscope-api.herokuapp.com/horoscope/year/"
	base_month_url = "http://horoscope-api.herokuapp.com/horoscope/month/"
	base_week_url = "http://horoscope-api.herokuapp.com/horoscope/week/"
	base_day_url = "http://horoscope-api.herokuapp.com/horoscope/today/"
	user_year_url = None
	user_month_url = None
	user_week_url = None
	user_day_url = None
	year_horoscope = None
	year_horoscope = None
	month_horoscope = None
	week_horoscope = None
	day_horoscope = None
	if auth.user is not None:
		curruser=db(db.user_table.user_email == auth.user.email).select().first()
	if curruser is not None:
		month = curruser.birthday.month
		day = curruser.birthday.day
		sign = get_sign(month, day).get('sign')
		print sign
	if sign is not None:
		user_year_url = base_year_url + sign
		user_month_url = base_month_url + sign
		user_week_url = base_week_url + sign
		user_day_url = base_day_url + sign
		year_horoscope = requests.get(user_year_url).json()
		year_horoscope = year_horoscope.get('horoscope')
		month_horoscope = requests.get(user_month_url).json().get('horoscope')
		week_horoscope = requests.get(user_week_url).json().get('horoscope')
		day_horoscope = requests.get(user_day_url).json().get('horoscope')
	return dict(message=T('Welcome!'), curruser=curruser, sign=sign, 
    	year_horoscope=year_horoscope, month_horoscope=month_horoscope, 
    	week_horoscope=week_horoscope, day_horoscope=day_horoscope)

def get_sign(month, day):
	sign = None
	if month == 1:
		if day <= 19:
			sign = "Capricorn"
		else:
			sign = "Aquarius"
	elif month == 2:
		if day <= 18:
			sign = "Aquarius"
		else:
			sign = "Pisces"
	elif month == 3:
		if day <= 20:
			sign = "Pisces"
		else:
			sign = "Aries"
	elif month == 4:
		if day <= 19:
			sign = "Aries"
		else:
			sign = "Taurus"
	elif month == 5:
		if day <= 20:
			sign = "Taurus"
		else:
			sign = "Gemini"
	elif month == 6:
		if day <= 20:
			sign = "Gemini"
		else:
			sign = "Cancer"
	elif month == 7:
		if day <= 22:
			sign = "Cancer"
		else:
			sign = "Leo"
	elif month == 8:
		if day <= 22:
			sign = "Leo"
		else:
			sign = "Virgo"
	elif month == 9:
		if day <= 22:
			sign = "Virgo"
		else:
			sign = "Libra"
	elif month == 10:
		if day <= 22:
			sign = "Libra"
		else:
			sign = "Scorpio"
	elif month == 11:
		if day <= 21:
			sign = "Scorpio"
		else:
			sign = "Sagittarius"
	elif month == 12:
		if day <= 21:
			sign = "Saggittarius"
		else: 
			sign = "Capricorn"
	else:
		sign = None
	return dict(sign=sign)

# ForumPage
def forum():
    return dict(table=None)


# User's personal page to see their chart, bio, and other things
def about_me():

    q = (db.user_table.user_email == auth.user.email)
    cl = db(q).select().first()

    chart_positions = find_positions(cl.birthday.day, cl.birthday.month, cl.birthday.year)

    return dict(cl=cl, positions=chart_positions)


# function that returns a dict of chart positions in degrees based on birthday
# current positions: sun
# TODO: moon, ascendant
def find_positions(day, month, year):
    sun_position = (30 * ((month - 4) % 12)) + day + 9
    return dict(sun=sun_position)


# User can edit profile here
def edit_profile():
    q = (db.user_table.user_email == auth.user.email)
    cl = db(q).select().first()

    if cl is not None:
        return dict(table=cl)
    else:
        # redirect(URL('default', 'index'))
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
        if request.vars > 0:
            # out_message = request.vars
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
        # out_message = "hold on"
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
