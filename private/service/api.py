import configparser
from flask import jsonify


cfp = configparser.ConfigParser()
cfp.read('sql_queries.ini')


def read_sql_query(query):
    sql_query = cfp.get('api', query)
    return {'data': [1, 2, 3]}


def get_info():
    data = read_sql_query('get_info')
    result = {
        'info': data,
        'status_code': 200
    }

    return jsonify(data)
