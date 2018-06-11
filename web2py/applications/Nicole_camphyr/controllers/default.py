# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
# ---- INSERTED FUNCTION FOR FORM ---
import random


def random_id():
    rand_id = ''
    for i in range(0, 5):
        int_or_char = random.randint(0, 1)  # integer or character
        if int_or_char == 0:  # if 0, integer
            rand_id = rand_id + str(random.randint(0, 9))
        else:  # else, character
            rand_id = rand_id + chr(random.randint(97, 122))
    return rand_id


def display_form():
    form = FORM('Your name:', INPUT(_name='name'), INPUT(_type='submit'))
    return dict(form=form)


# add a story
def add_story():
    form = SQLFORM(db.story)
    if form.process().accepted:
        session.flash = T("Story has been added.")
    elif form.errors:
        session.flash = T("ERROR: Story has not been added. ")
    return dict(form=form)


# ~~~~~~~~~~~~~~~~~~~~~~~~NEW~~~~~~~~~~~~~~~~~~~~
def create_story():
    new_story = FORM('Title: ',
                     INPUT(_type='text', _name='title', _cols='10', _placeholder='Enter title here...'),
                     BR(),
                     BR(),
                     TEXTAREA(_name='bio_story', _cols='80', _row='50', _placeholder='Enter story here...',
                              requires=IS_NOT_EMPTY()),
                     BR(),
                     INPUT(_type='submit', _name='submit'))
    if auth.user is None:
        response.flash = 'please log in before posting a snippet'
    elif new_story.accepts(request, session):
        db.bio_story.insert(title=request.vars.title, story=request.vars.bio_story)
        redirect(URL('default', 'user_profile'))
    elif new_story.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(new_story=new_story)


def user_story():
    bio_story_title = request.vars['title_name']  # takes in argument for the title of the story
    selected_story = db(db.bio_story.title == bio_story_title).select().first()
    return dict(b_title=bio_story_title, b_text=selected_story.story)


# ~~~~~~~~~~~~~~~~~~~~~~~~END~~~~~~~~~~~~~~~~~~~~~


# test function, creates text field for adding snippet onto existing story
def sample_story_page():
    openstory = db(db.story.lastcreated == True).select().first()
    if openstory is None:
        openstory_title = request.vars['title_name']
        openstory = db(db.story.title == openstory_title).select().first()
    form = FORM(TEXTAREA(_name='snippet', _cols='20', _rows='23', _maxlength='200', _placeholder='type text here...',
                         requires=IS_NOT_EMPTY()),
                BR(),
                DIV(INPUT(_name='return', _type='submit'), _class='return', id=0),
                STYLE(XML('.return{position: relative}')),
                DIV(INPUT(_name='fin', _type='submit', value='finish', _value='Finish'), _class='finish', _id=0),
                STYLE(XML(
                    '.finish{position: relative; left: 400px; bottom: 57px}')))  # creates text area w/ text area size of 3x40, max length (characters) of 200, and a placeholder text
    if auth.user is None:
        response.flash = 'please log in before posting a snippet'
    elif form.accepts(request, session):
        openstory.update_record(num_snippets=db.story.num_snippets + 1)  # updates snippet counter
        value = 1  # keeps track of ordering of snippet
        curr_story = db(db.story.is_public).select()  # initializes current story
        for s in db(db.story.is_public).select():
            if s.title == openstory.title:
                curr_story = s
                value += 1
        if request.vars.fin:
            openstory.update_record(fin=True)
        db.story.insert(title=curr_story.title, storyId=curr_story.storyId, head=False, snippets=request.vars.snippet,
                        fin=False)  # adds to db with title, 'HELLO!'. (temporary)
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    entries = []
    usernames = []
    for name in db(db.story.title == openstory.title).select():
        entries.append(name.snippets)  # puts snippets into an array
        usernames.append(name.user_email)
    if len(entries) >= 15:
        openstory.update_record(fin=True)
    # db(db.story.clicked==True).update(clicked=False)
    return dict(snippet=form, openstory=openstory, entries=entries, usernames=usernames, finish=openstory.fin)


# ---- example index page ----
def index():
    # make this different later:
    form = None
    currstory = None
    db(db.story.lastcreated == True).update(lastcreated=False)
    if auth.user is None:
        response.flash = 'please log in before adding a story'
    else:
        form = FORM(TEXTAREA(_name='story', _cols='30', _rows='3', _maxlength='200', _placeholder='type text here...',
                             requires=IS_NOT_EMPTY()),
                    BR(),
                    TEXTAREA(_name='snippet', _rows='4', _cols='50', _maxlength='2500',
                             _placeholder='Add snippet here...'),
                    INPUT(_type='submit'))
        if form.accepts(request, session):
            idstr = random_id()
            db.story.insert(title=request.vars.story, lastcreated=True, ishead=True, snippets=request.vars.snippet,
                            num_snippets=0, storyId=idstr, fin=False)
            redirect(URL('default', 'sample_story_page'))
    stories = db(db.story.is_public).select()  # type: string?
    # db(db.story.clicked==True).update(clicked=False)
    return dict(message=T('Welcome to Camphyr!'), stories=stories, story=form, currstory=currstory)


def onclickstories():
    printstories = db(db.story.is_public).select()
    return dict(printstories=printstories)


def backbutton():
    openstory = db(db.story.lastcreated).select().first()
    openstory.update_record(lastcreated=False)
    redirect(URL('default', 'index'))
    return dict(openstory=openstory)


def clicking():
    name = request.vars.name
    name.update_record(clicked=True)
    return dict()


# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status': 'success', 'email': auth.user.email})


# ---- Smart Grid (example) -----
@auth.requires_membership('admin')  # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html'  # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)


# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu()  # add the wiki to the menu
    return auth.wiki()


# ---- Action for login/register/etc (required for auth) -----
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


# The following three functions are from Nicole's implementation of the profile page --Alex
# ---START---
def user_profile():
    '''
    When integrating:
        - bio_story_title and selected story were not changed
        - pretty much everything besides that was changed so I suggest you just copy this entire method
        - we are getting user id from the db user_profile records, not the auth.user
        - make sure everything in the return dicts are there for the HTML
    '''

    if request.vars.user_id is None:
        q = (db.user_profile.user_email == auth.user.email)
        cl = db(q).select().first()
        if cl:
            user_id = cl.id
        else:
            record = db.user_profile.insert(
                                            user_email=get_user_email(),
                                            bio="Write an about me page here!"
                                            )
            user_id = record.id
    else:
        user_id = request.vars.user_id

    # takes in argument for the title of the story
    bio_story_title = request.vars['title_name']
    selected_story = db(db.bio_story.title == bio_story_title).select().first()

    q = (db.user_profile.id == user_id)
    cl = db(q).select().first()

    # search auth by user email for name
    users_auth = db(db.auth_user.email == cl.user_email).select().first()
    username = users_auth.first_name

    # JUST ADDED:
    bio = users_auth.about

    if users_auth.file_name is not None:
        filename = users_auth.file_name
        print filename
    else:
        filename = "default_profile.jpg"

    if cl is None:
        cl = None
    if selected_story is None:
        return dict(cl=cl, username=username, file_name=filename, b_title=None, b_text=None, bio=bio)
    else:
        return dict(cl=cl,
                    username=username,
                    file_name=filename,
                    b_title=bio_story_title,
                    b_text=selected_story.story,
                    users_auth=users_auth,
                    bio=bio
                    )


# edits user profile
@auth.requires_login()
def edit_profile():
    record = db.user_profile(request.args(0))
    form = SQLFORM(db.user_profile, record, deletable=True,
                   upload=URL('static', 'images', 'prof_pics'))
    form.add_button('Back to Profile', URL('default', 'user_profile'))

    # submit = form.element("input", _type="submit")
    # submit["_onclick"] = "return confirm('Are you sure?');"
    au = auth.user
    if form.process().accepted:
        response.flash = 'form accepted'

        # update db
        filename = form.vars.profile_picture
        auth_table = db(db.auth_user.email == get_user_email()).select().first()

        '''
        INTEGRATION: I CHANGED EITHER UPDATE RECORD OR UPDATE, CANT REMEMBER WHICH
        '''
        auth_table.update_record(
            file_name=filename,
            about=request.vars.bio,
            upload_data=request.vars.upload_data
        )

        # update auth
        auth.user.update(
            about=request.vars.bio,
            file_name=filename,
            upload_data=request.vars.upload_data
        )

    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form, user=record, au=au)  # , submit=submit)
    # Alex note: commented this out as the above comment left "submit" undefined


# edit user form requires image download helper (redundant and may not be necessary)
def download():
    return response.download(request, db)


# ---END---

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
