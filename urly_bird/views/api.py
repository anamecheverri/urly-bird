import base64
import json

from flask import Blueprint, jsonify, request, abort, url_for
from flask.ext.login import login_user

from ..models import Links, User
from ..forms import LinkAddForm, LinkUpdateForm
from ..extensions import login_manager, db


api = Blueprint("api", __name__)


def json_response(code, data):
    return (json.dumps(data), code, {"Content-Type": "application/json"})


@api.app_errorhandler(401)
def unauthorized(request):
    return ("", 401, {"Content-Type": "application/json"})


@login_manager.request_loader
def authorize_user(request):
    # Authorization: Basic username:password
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        api_key = base64.b64decode(api_key).decode("utf-8")
        email, password = api_key.split(":")

        user = User.query.filter_by(email=email).first()
        if user.check_password(password):
            return user

    return None


def require_authorization():
    user = authorize_user(request)
    if user:
        login_user(user)
    else:
        abort(401)


@api.route("/", methods=["GET", "POST"])
def links():
    if request.method == "POST":
        return create_link()

    links = Links.query.all()
    links = [link.to_dict() for link in links]
    return jsonify({"links": links})


def create_link():
    """Creates a new link from a JSON request."""
    require_authorization()
    body = request.get_data(as_text=True)
    data = json.loads(body)
    form = LinkAddForm(data=data, formdata=None, csrf_enabled=False)
    if form.validate():
        link = Links(**form.data)
        db.session.add(link)
        db.session.commit()
        return (json.dumps(link.to_dict()), 201, {"Location": url_for(".link", id=link.id)})
    else:
        return json_response(400, form.errors)


@api.route("/links/<int:id>")
def link(id):
    link = Links.query.get_or_404(id)
    return jsonify(link.to_dict())