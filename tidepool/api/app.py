"""tidepool/api/app.py"""

import logging
import time

from flask import Flask, jsonify, g
from flask_cors import CORS

from tidepool import TidepoolRepository
from tidepool.settings.manager import settings

logger = logging.getLogger(__name__)

api_app = Flask(__name__)
CORS(api_app)


@api_app.before_request
def before_request():
    g.start_time = time.time()


@api_app.after_request
def after_request(response):
    logger.debug(f"API elapsed: {time.time() - g.start_time}")
    return response


@api_app.route("/api", methods=["GET"])
def root():
    return jsonify({"repository_name": settings.REPOSITORY_NAME})


@api_app.route("/api/items", methods=["GET"])
def items():
    # TODO: this needs pagination, simple filtering, and sorting
    #   - this could drive a very simple datatables interface
    tr = TidepoolRepository()
    items = [item.to_dict() for item in tr.get_items()]
    return jsonify(items)


@api_app.route("/api/items/<item_uuid>", methods=["GET"])
def items_item(item_uuid: str):
    # TODO: standardize this; maybe embed as @before_request
    tr = TidepoolRepository()
    item = tr.get_item(item_uuid=item_uuid)
    return jsonify(item.to_dict())


@api_app.route("/api/items/<item_uuid>/delete", methods=["GET"])
def items_item_delete(item_uuid: str):
    # TODO: standardize this; maybe embed as @before_request
    tr = TidepoolRepository()
    item = tr.get_item(item_uuid=item_uuid)
    tr.delete_item(item=item)
    return jsonify(
        {
            "item_uuid": item_uuid,
            "action": "delete",
            "success": True,
        }
    ), 200


@api_app.route("/api/items/<item_uuid>/files", methods=["GET"])
def items_item_files(item_uuid: str):
    tr = TidepoolRepository()
    item = tr.get_item(item_uuid=item_uuid)
    return jsonify([file.to_dict() for file in item.files])


@api_app.route("/api/items/<item_uuid>/files/<file_uuid>", methods=["GET"])
def items_item_files_file(item_uuid: str, file_uuid: str):
    tr = TidepoolRepository()
    item = tr.get_item(item_uuid=item_uuid)
    file = item.get_file(file_uuid=file_uuid)
    return jsonify(file.to_dict())


# TODO: support streaming
@api_app.route("/api/items/<item_uuid>/files/<file_uuid>/data", methods=["GET"])
def item_file_data(item_uuid: str, file_uuid: str):
    tr = TidepoolRepository()
    item = tr.get_item(item_uuid=item_uuid)
    file = item.get_file(file_uuid)
    file_data = tr.read_file_data(file)
    response = api_app.response_class(
        response=file_data,
        status=200,
        mimetype=file.mimetype,
    )
    response.headers["Content-Disposition"] = f'inline; filename="{file.filename}"'
    return response


if __name__ == "__main__":
    api_app.run(
        host=settings.API_HOST,
        port=settings.API_PORT,
        debug=settings.API_DEBUG,
    )
