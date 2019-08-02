from flask import Flask
from flask import request
import logging
import sqlite3
import json

app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)


def read_user_from_database(nfc_id):
    conn = sqlite3.connect('eisapp.db')
    c = conn.cursor()
    app.logger.debug('request for: {}'.format(nfc_id))
    query = "SELECT * FROM users WHERE nfcid = '{}'".format(nfc_id)
    app.logger.debug('query : {}'.format(query))
    c.execute(query)
    response = c.fetchone()
    conn.close()
    return response


def get_user(nfc_id):
    response = read_user_from_database(nfc_id)
    response_json = json.dumps({
        'name': response[0],
        'nfcid': response[1],
        'amount': response[2],
        'isok': True
    })
    app.logger.debug(response)
    app.logger.debug(response_json)
    return str(response_json)


def create_user(nfc_id):
    response = read_user_from_database(nfc_id)
    if response is None:
        conn = sqlite3.connect('eisapp.db')
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES ('{}','{}',{})".format('', nfc_id, 0))
        conn.commit()
        app.logger.debug('User Created')
        conn.close()
    else:
        app.logger.debug('User already exists')
    return "Done!"


@app.route("/register", methods=['POST'])
def register():
    bar = request.args.to_dict()
    return create_user(bar['nfcid'])


@app.route("/user", methods=['GET'])
def user():
    bar = request.args.to_dict()
    app.logger.debug(request)
    app.logger.debug(bar)
    return get_user(bar['nfcid'])


if __name__ == '__main__':
    app.run(host='192.168.137.1', debug=True)
