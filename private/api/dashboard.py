from flask import Blueprint
from private.db.models.identity import DbMethods

dashboard_api = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_api.route("/<id>", methods = ["GET"])
def get_by_id(id):
    id = int(id or 0) 
    return {
        "id": id,
        'dashboards': [
            {
                'name': 'progress',
                'data': [
                    [3.4, 4.1, 4.5],
                    [3.3, 3.9, 4.1]
                ],
            },
            {
                'name': 'avg',
                'data': [4.4, 3.2, 3.5]
            }
        ]        
    }
