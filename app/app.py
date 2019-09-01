from flask import Flask
from flask import request
import logging
from model.user import db
from model.user import User

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eisapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# later on
db.init_app(app)
db.create_all(app=app)


def get_user(nfc_id):
    response = User.query.filter_by(nfcid=nfc_id).first_or_404()
    app.logger.debug(response)
    app.logger.debug(response.create_json())
    return str(response.create_json(True))


def create_user(nfc_id):
    response = User.query.filter_by(nfcid=nfc_id).first()
    if response is None:
        new_user = User(nfc_id)
        db.session.add(new_user)
        db.session.commit()
        app.logger.debug('User Created')
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
    app.run(host='192.168.178.22', debug=True)
