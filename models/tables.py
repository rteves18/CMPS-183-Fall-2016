# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime

db.define_table('post',
                Field('user_email', default=auth.user.email if auth.user_id else None),
                Field('title'),
                Field('post', 'text'),
                Field('last_opened', 'datetime', update=datetime.datetime.utcnow()),
                Field('created_on', 'datetime', default=datetime.datetime.utcnow()),
                Field('updated_on', 'datetime', update=datetime.datetime.utcnow()),
                )

# I don't want to display the user email by default in all forms.
db.post.id.readable = db.post.id.writable = False
db.post.user_email.readable = db.post.user_email.writable = False
db.post.created_on.readable = db.post.created_on.writable = False
db.post.updated_on.readable = db.post.updated_on.writable = False
db.post.last_opened.readable = db.post.last_opened.writable = False
db.post.title.requires = IS_NOT_EMPTY()

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
