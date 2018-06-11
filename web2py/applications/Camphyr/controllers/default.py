# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
# ---- INSERTED FUNCTION FOR FORM ---
import random

def add_id(new_id): # adds id to list of contribution ids
    data = db(db.user_profile.user_email == get_user_email()).select().first()
    updated_list = data.contribution_id
    updated_list.append(new_id)
    data.update_record(contribution_id = updated_list)
    return


def random_id():
    rand_id = ''
    duplicate = True # boolean for whether the id is unique or not
    while (duplicate == True):
        for i in range(0, 5):
            int_or_char = random.randint(0, 1) # integer or character
            if int_or_char == 0: # if 0, integer
                rand_id = rand_id + str(random.randint(0,9))
            else: # else, character
                rand_id = rand_id + chr(random.randint(97, 122)) 
        if db(db.story.storyId == rand_id).select().first() is None: #NEW
            duplicate = False
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


def create_story():
    new_story = FORM('Title: ',
                    INPUT(_type = 'text', _name = 'title', _cols = '10', _maxlength = '200', _placeholder = 'Enter title here...'),
                    BR(),
                    BR(),
                    TEXTAREA(_name = 'bio_story', _cols = '80', _row = '50', _maxlength = '50000', _placeholder = 'Enter story here...', requires = IS_NOT_EMPTY()),
                    BR(),
                    INPUT(_type = 'submit', _name = 'submit',value='submit', _value='Submit'))
    if auth.user is None:
        response.flash = 'please log in before posting a snippet'
    elif new_story.accepts(request,session):
        db.bio_story.insert(title = request.vars.title, story = request.vars.bio_story)
        redirect(URL('default', 'user_profile'))
    elif new_story.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(new_story = new_story)


# standalone stories
def user_story():
    bio_story_title = request.vars['title_name'] # takes in argument for the title of the story
    selected_story = db(db.bio_story.title == bio_story_title).select().first()
    return dict(b_title = bio_story_title, b_text = selected_story.story)


# test function, creates text field for adding snippet onto existing story
def sample_story_page():
    fourteen_snips = False
    can_contribute = True
    openstory=db(db.story.lastcreated==True).select().first()
    if openstory is None:
        openstory_title = request.vars['story_id']
    	openstory=db(db.story.storyId==openstory_title).select().first()
    if openstory.lastcontributed == get_user_email():
        can_contribute = False
    form = FORM(TEXTAREA(_name = 'snippet', _width = '100px', _maxlength = '2500', _placeholder = 'type text here...', requires = IS_NOT_EMPTY()),
              BR(),
              DIV(INPUT(_name = 'return', _type='submit'), _class = 'return', id = 0),
              STYLE(XML('.return{position: relative}')),
              DIV(INPUT(_name = 'fin', _type = 'submit', value = 'finish', _value = 'Finish'), _class = 'finish', _id = 0),
              STYLE(XML('.finish{position: relative}'))) # creates text area w/ text area size of 3x40, max length (characters) of 200, and a placeholder text
    if auth.user is None:
        response.flash = 'please log in before posting a snippet'
    elif form.accepts(request,session):
        openstory.update_record(num_snippets = db.story.num_snippets + 1) # updates snippet counter
        openstory.update_record(lastcontributed = get_user_email())
        value = 1 # keeps track of ordering of snippet
        curr_story = db(db.story.is_public).select() # initializes current story
        for s in db(db.story.is_public).select():
            if s.storyId == openstory.storyId:
                curr_story = s
                value += 1
        if request.vars.fin:
            openstory.update_record(fin = True)
        add_id(curr_story.storyId)
        db.story.insert(title = curr_story.title, storyId = curr_story.storyId, head = False, snippets = request.vars.snippet, fin = False, address = URL('default', 'sample_story_page', vars = dict(story_id = curr_story.storyId)))
        redirect(openstory.address)
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    images = []
    links = []
    entries = []
    usernames = []
    for name in db(db.story.storyId == openstory.storyId).select():
        users_auth = db(db.auth_user.email == name.user_email).select().first()
        file_name = users_auth.file_name
        temp_image_var = URL('static', 'images/prof_pics/default_profile.jpg')
        if file_name is not None:
            temp_image_var = URL('static', 'images/prof_pics', args=file_name)
        images.append(temp_image_var)
        poster = db(db.user_profile.user_email == name.user_email).select().first()
        links.append(URL('default', 'user_profile', vars = dict(user_id = poster.id)))
        entries.append(name.snippets) # puts snippets into an array
        usernames.append(name.user_email) 
    if len(entries) >= 15:
        openstory.update_record(fin = True)
    if len(entries) == 14:
        fourteen_snips = True
    return dict(snippet = form, openstory = openstory, entries = entries, usernames = usernames, finish = openstory.fin, can_contribute = can_contribute, images = images, links = links, warning = fourteen_snips)


# ---- example index page ----
def index():
    # make this different later:
    form = None
    currstory = None
    db(db.story.lastcreated==True).update(lastcreated=False)
    if auth.user is None:
        response.flash = 'please log in before adding a story'
    else:
        if db(db.user_profile.user_email == get_user_email()).select().first() is None:
            db.user_profile.insert()
        form=FORM('Story title:', TEXTAREA(_name='story', _cols='30', _rows='3', _maxlength='200', _placeholder='Type title here...', requires=IS_NOT_EMPTY()),
              BR(),
              'Start your story:',
              TEXTAREA(_name='snippet', _rows='4', _cols='50', _maxlength='2500', _placeholder='Add snippet here...'),
              INPUT(_type='submit',value='submit', _value='Submit'))
        if form.accepts(request,session):
            idstr = random_id()
            add_id(idstr)
            db.story.insert(title = request.vars.story, lastcreated=True, ishead=True, snippets = request.vars.snippet, num_snippets = 0, storyId = idstr, fin = False, address = URL('default', 'sample_story_page', vars = dict(story_id = idstr)))
            redirect(URL('default', 'sample_story_page'))
    stories = db(db.story.is_public).select()  # type: string?
    #db(db.story.clicked==True).update(clicked=False)
    return dict(message=T('Welcome to Camphyr!'), stories=stories, story=form, currstory=currstory)

def onclickstories():
    printstories=db(db.story.is_public).select()
    return dict(printstories=printstories)

def backbutton():
    openstory=db(db.story.lastcreated).select().first()
    openstory.update_record(lastcreated=False)
    redirect(URL('default', 'index'))
    return dict(openstory=openstory)

def clicking():
	name=request.vars.name
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
#---START---
def user_profile():
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


#edits user profile
@auth.requires_login()
def edit_profile():
    #record = db.user_profile(request.args(0))
    record = db(db.user_profile.user_email == get_user_email()).select().first()
    form = SQLFORM(db.user_profile, record, deletable=False,
                   upload=URL('static', 'images', 'prof_pics'),
                   showid = False)
    form.add_button('Back to Profile', URL('default', 'user_profile'))
    # submit = form.element("input", _type="submit")
    # submit["_onclick"] = "return confirm('Are you sure?');"
    au = auth.user
    if form.process().accepted:
        response.flash = 'form accepted'

        # update db
        auth_table = db(db.auth_user.email == get_user_email()).select().first()
        bio = request.vars.bio
        data = request.vars.upload_data
        filename = form.vars.profile_picture
        auth_table.update_record(
            file_name=filename,
            about=bio,
            upload_data=data
        )

        # update auth
        auth.user.update(
            about=request.vars.bio,
            file_name=filename,
            upload_data=data
        )
        redirect(URL('default', 'user_profile'))
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form, user=record, au=au) #, submit=submit)
    #Alex note: commented this out as the above comment left "submit" undefined

#edit user form requires image download helper (redundant and may not be necessary)
def download():
    return response.download(request, db)

#---END---

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def searches():
    words_to_remove = ["and", "to", "the", "a", "an", "I", "you", "me", "is", "are",
                        "with", "how", "who", "what", "where", "when", "why", "by",
                        "can", "may", "as", "they", "their", "them", "he", "she",
                        "his", "her", "it", "him"]

    #Get the string the user entered
    search = request.vars.search                    #search is variable user entered in index.html search bar
    search = search.rstrip()                        #remove excess whitespaces on right side
    search = search.lstrip()                        #remove excess whitespaces on left side
    search_string = ("%s" % search)                 #turn searchinput into a string

# ------------------------ Look for exact matches ----------------
    #query = db.story.title == ("%s" % search)       #query stories with the same title
    #s = db(query)                                   #s = query table
    #rows = s.select()                               #rows is every row in s , starting at the top

    #create table of titles with same search_string input (case insensitive)
    rows = db(db.story.title.lower() == search_string.lower()).select()     #create table

    list1 = []                                      #create an empty list to hold rows with queried title
    length = 0                                      #initiate length to 0. hold number of titles with queried name
    for row in rows:                                #loop through all titles with queried name
        list1.append(row)                           #append the row to the list
        length = length + 1                         #increment number of titles by 1
    stories = list1                                 #put list into stories

#--------------------------- look for related stories

    related_stories=[]                                      #list to hold final results of related stories

    #---- if title is substring of search string ----
    query = db.story                                        #query database
    s = db(query)                                           #s = database table
    rows = s.select()                                       #rows = rows in database table
    for row in rows:                                        #iterate through every row
        if row.title is None:                               #if title is invalid
            row.delete_record()                             #delete invalid title
        elif row.title.lower() in search_string.lower():    #if the title is in search string
            related_stories.append(row)                     #append it to related_stories

    #---- if search string is substring of title ----
    if search_string in words_to_remove:                        #if search_string is generic words
        print("do nothing")                                     #do nothing
    else:                                                       #else if is non-generic
        query = db.story                                        #query the database
        s = db(query)                                           #s = database table
        rows = s.select()                                       #rows = rows in datatable
        for row in rows:                                        #iterate through the rows
            if row.title is None:                               #if row is invalid
                row.delete_record()                             #delete the row
            elif search_string.lower() in row.title.lower():    #if search string is in title
                related_stories.append(row)                     #append to related_stories

    #---- If each individual word is a substring of a title ----

    #instantiate variables to use for building words
    word = ""                                       #create empty string
    words = []                                      #list to hold words in search string

    #create list of each word in search string
    for c in search:                                #for loop to iterate through search string
        if c == " ":                                #if there is a space
            words.append(word)                      #append the word to list2
            word = ""                               #clear the word
        else:                                       #if there isn't a space
            char_to_string = ("%s" % c)             #convert char to string so it can be appended to word
            word += char_to_string                  #append c to word to slowly build a word
    words.append(word)                              #append the last built word to words[]

    #remove uneccessary words
    for word in words:                              #iterate through list of words
        if word in words_to_remove:                 #if a word is to be removed
            words.remove(word)                      #remove it

    #query database to see if each individual word is a substring in a title
    for i in range(0, len(words)):                          #for every individual word in the search string
        query = db.story                                    #query database for every title
        s = db(query)                                       #s = query table
        rows = s.select()                                   #row is each row in table
        for row in rows:                                    #iterate through each row
            if row.title is None:                           #is the title is invalid
                row.delete_record()                         #delete row
            elif words[i].lower() in row.title.lower():     #else if the individual word is a substring of a title
                related_stories.append(row)                 #add title to results list


    # ---- Remove Duplicates ----
    nonduplicated_story_ids = []                        #create list to hold all unique story ids
    unique_related_stories = []                         #create list of all unique stories
    for story in related_stories:                       #iterate through every story
        if story.id in nonduplicated_story_ids:         #if story is a duplicate
            continue                                    #do nothing
        else:                                           #if the story is no a duplicate
            unique_related_stories.append(story)        #add story id to list of noduplciated ids
            nonduplicated_story_ids.append(story.id)    #add story to list of non duplicated stories
    related_stories = unique_related_stories            #make ralted stories the list of all nonduplkicated stories

    #related_stories.reverse()                           #reverse the list of related stories

    if search_string == "":                             #if nothing was entered
        stories = []                                    #stories should be empty
        related_stories = []                            #related_stories should be empty
        length = 0                                      #length should be 0

    return dict(message=T('Results'),stories=stories, related_stories=related_stories, length=length, search=search) #load variables for searches.html

# ------------------------------------------------------------------------------
# -------------------- END OF RAYMOND'S CODE -----------------------------------
# ------------------------------------------------------------------------------
