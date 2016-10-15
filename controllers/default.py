# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

"""===Gets Username's First and Last Name==="""
def get_user_name_from_email(email):
    """Returns a string corresponding to the user first and last names,
    given the user email."""
    u = db(db.auth_user.email == email).select().first()
    if u is None:
        return 'None'
    else:
        return ' '.join([u.first_name, u.last_name])


def index():
    """
    === Returns 'post' from the Database order by last created ===
    === Also returns 'author' from get user name from email function ===
    """
    return dict(posts=db().select(orderby=~db.post.created_on), author = get_user_name_from_email)


@auth.requires_login()
def edit():
    """
    === Create / Edit / Delete post functions here ===
    """
    if request.args(0) is None:
        # request.args[0] would give an error if there is no argument 0.
        form_type = 'create'
        # Creates a form for adding a new checklist item.
        form = SQLFORM(db.post)
    else:
        # Authenticates edit with original poster
        q = ((db.post.user_email == auth.user.email) &
             (db.post.id == request.args(0)))
        cl = db(q).select().first()
        if cl is None:
            session.flash = T('Not Authorized')
            redirect(URL('default', 'index'))

        # Update the last opened date.
        cl.updated_on = datetime.datetime.utcnow()
        cl.update_record()

        # Edit form

        is_edit = (request.vars.edit == 'true')
        form_type = 'edit' if is_edit else 'view'
        form = SQLFORM(db.post, record=cl, deletable=is_edit, readonly=not is_edit)

    # Edit page buttons
    button_list = []
    if form_type == 'edit':
        button_list.append(A('Cancel', _class='btn btn-warning',
                             _href=URL('default', 'edit', args=[cl.id])))
    elif form_type == 'create':
        button_list.append(A('Cancel', _class='btn btn-warning',
                             _href=URL('default', 'index')))
    elif form_type == 'view':
        button_list.append(A('Edit', _class='btn btn-warning',
                             _href=URL('default', 'edit', args=[cl.id], vars=dict(edit='true'))))
        button_list.append(A('Back', _class='btn btn-primary',
                             _href=URL('default', 'index')))

    # Edit post flashes update
    if form.process().accepted:
        if form_type == 'create':
            session.flash = T('Post added.')
        else:
            session.flash = T('Post edited.')
        redirect(URL('default', 'index'))
    elif form.errors:
        session.flash = T('Please enter correct values.')
    return dict(form=form, button_list=button_list)


def user():
    """
    === Returns user authorization ===
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


