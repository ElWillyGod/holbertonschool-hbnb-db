
'''
    Defines all variables for app.config
'''


from pathlib import Path
from werkzeug.exceptions import HTTPException

from flask import render_template, request, Blueprint

error_handler = Blueprint("error_handler", __name__)

_root_path = Path(__file__).parent.parent.resolve()

@error_handler.app_errorhandler(HTTPException)
def handle_exception(e):
    if request.headers.get('Content-Type') == 'application/json':
        return e
    return render_template("error.html", code=e.code), e.code
