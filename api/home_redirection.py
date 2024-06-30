
'''
    Sets up a redirection for the home page ("/").
'''

from flask import Blueprint, redirect, url_for

bp = Blueprint("apidocs", __name__)


@bp.get('/')
def hello():
    '''
        redirection to apidocs.
    '''

    return redirect(url_for("flasgger.apidocs"), code=302)
