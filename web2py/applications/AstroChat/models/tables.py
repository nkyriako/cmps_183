#Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime

def get_user_email():
    return auth.user.email if auth.user is not None else None

db.define_table('user_table',
		Field('user_email', default=get_user_email()),
                Field('birthday', 'datetime'),
                Field('birth_sign')
                )

db.user_table.user_email.writeable = db.user_table.user_email.readable = False
db.user_table.id.writeable = db.user_table.id.readable = False
db.user_table.birth_sign.writeable = db.user_table.birth_sign.readable = False

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
