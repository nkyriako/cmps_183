# Here go your api methods.

# adding new forum message
@auth.requires_login()
def add_forum():
    t_id = db.checklist.insert(
        title = request.vars.title,
        memo = request.vars.memo,
        #user_email = auth.user_email,
    )
    #t = db.checklist(t_id)
    #return response.json(dict(forum=t))

# get forum to display
def get_forum():
    forum = []
    rows2 = db(db.checklist).select()
    
    for i, r in enumerate(rows2):
	t = dict(
	    title = r.title,
            memo = r.memo,
            email = r.user_email,
	    id = r.id
        )
	forum.append(t)

    return response.json(dict(
	forum=forum
    ))

def get_user_email():
    email = auth.user.email;
    return response.json(dict(
	email=email
    ))
