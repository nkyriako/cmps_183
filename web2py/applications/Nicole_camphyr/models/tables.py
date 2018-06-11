import datetime
import os


def get_user_email():
    return auth.user.email if auth.user is not None else None


def get_user_name():
    return auth.user.first_name if auth.user is not None else None


def get_user_about():
    return auth.user.about if auth.user is not None else "Edit your bio!"


db.define_table('story',
                Field('user_email', default=get_user_email()),
                Field('title'),
                Field('snippets', 'text'),
                Field('lastcreated', 'boolean', default=False),
                Field('updated_on', 'datetime', update=datetime.datetime.utcnow()),
                Field('is_public', 'boolean', default=True),
                Field('storyId', 'text'),
                Field('ishead', 'boolean', default=False),
                Field('clicked', 'boolean', default=False),
                Field('num_snippets', 'integer', default=0),  # NEW
                Field('fin', 'boolean')
                )

db.define_table('user_profile',
                Field('user_email', default=get_user_email(), writable=False),
                Field('bio', 'text', requires=IS_NOT_EMPTY()),
                Field('profile_picture', 'upload',
                      uploadfolder=os.path.join(request.folder, 'static/images/prof_pics/'),
                      upload_field='upload_data'
                      ),
                Field('upload_data', 'blob'),
                Field('file_name', writable=False)
                )

db.define_table('bio_story',
                Field('user_email', default=get_user_email()),
                Field('title', 'text'),
                Field('story', 'text')
                )

db.story.user_email.writeable = False
db.story.user_email.readable = False
db.story.updated_on.writable = db.story.updated_on.readable = False
db.bio_story.user_email.writeable = False
db.bio_story.user_email.readable = False
# optimize this later
