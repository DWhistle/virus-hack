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
                'name': 'rose',
                'data': [10, 20, 40]
            }
        ]        
    }
