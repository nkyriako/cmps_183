#Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime
import os

def get_user_email():
    return auth.user.email if auth.user is not None else None

db.define_table('user_table',
		Field('user_email', default=get_user_email()),
                Field('birthday', 'date'),
                Field('profile_picture', 'upload', uploadfolder=os.path.join(request.folder, 'static/images/profile_pics/')),
                Field('bio'),
                Field('banner', 'text', default='Red')
                )

	

db.user_table.user_email.writable = db.user_table.user_email.readable = False
db.user_table.id.writable = db.user_table.id.readable = False
db.user_table.profile_picture.autodelete = True

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
