
'''
    Defines all variables for app.config
'''


from pathlib import Path
from werkzeug.exceptions import HTTPException

import os

from flask import (render_template, request, Blueprint, Response,
                   make_response, jsonify)

error_handler = Blueprint("error_handler", __name__)

_root_path = Path(__file__).parent.parent.resolve()

RETURN_CAT = os.environ.get("RETURN_CAT_ON_ERROR", default="true").lower()

@error_handler.app_errorhandler(HTTPException)
def handleHTTPException(e: HTTPException) -> Response:
    return handleCats(e.description, e.code)


def handleCats(desc: str, code: int) -> Response:
    '''
        Handles if exceptions must be shown as an http cat error.
    '''

    if RETURN_CAT == "true":
        return make_response(render_template("error.html", code=code), code)
    else:
        return make_response({"error": desc}, code)
