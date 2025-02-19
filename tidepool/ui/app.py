"""tidepool/ui/app.py"""

import json
import logging

from flask import Flask, render_template, request, g, redirect, url_for
import requests

from tidepool.settings.manager import settings

logger = logging.getLogger(__name__)

ui_app = Flask(__name__)


# TODO: move to utility
# TODO: consider calling flask app directly somehow?
# QUESTION: if both apps under blueprints, is it posisble we can skip the prefix handling?
@ui_app.before_request
def before_request():
    api_path = request.path.removeprefix("/ui")

    if "/static/" in api_path:
        return

    api_url = f"{settings.API_BASE_URI}/{api_path}".removesuffix("/")
    logger.debug(api_url)
    api_response = requests.get(api_url)
    logger.debug(f"API response: {api_response.status_code}")
    try:
        g.api = api_response.json()
    except:
        print(api_response.content)


@ui_app.route("/ui", methods=["GET"])
def root():
    return render_template(
        "index.html",
        api=g.api,
        api_json=json.dumps(g.api, indent=4),
    )


@ui_app.route("/ui/items", methods=["GET"])
def items():
    return render_template(
        "items.html",
        api=g.api,
        api_json=json.dumps(g.api, indent=4),
    )


@ui_app.route("/ui/items/<item_uuid>", methods=["GET"])
def items_item(item_uuid: str):
    return render_template(
        "item.html",
        api=g.api,
        api_json=json.dumps(g.api, indent=4),
    )


@ui_app.route("/ui/items/<item_uuid>/delete", methods=["GET"])
def items_item_delete(item_uuid: str):
    logger.info(f"deleting item: {item_uuid}")
    return redirect(url_for("items"))


@ui_app.route("/ui/items/<item_uuid>/files/<file_uuid>", methods=["GET"])
def items_item_files_file(item_uuid: str, file_uuid: str):
    return render_template(
        "file.html",
        api=g.api,
        api_json=json.dumps(g.api, indent=4),
    )


if __name__ == "__main__":
    ui_app.run(
        host=settings.UI_HOST,
        port=settings.UI_PORT,
        debug=settings.UI_DEBUG,
    )
