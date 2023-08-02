from flask import render_template, request, Blueprint
bp = Blueprint('error', __name__)


def not_found_error(error):
    return render_template('404.html'), 404