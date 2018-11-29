from flask import Flask 
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_cors import CORS

from Decider.api import api
from Decider.config import config
from Decider.db.db_setup import db_session
from Decider.db.models import Token, Question, QuestionEffect

app = Flask(__name__)

# enable CORS (from everywhere, for now)
CORS(app)

# set config options
for key in config: 
    app.config[key] = config[key]

# add router middleware
app.register_blueprint(api, url_prefix="/api")

# set up flask admin
admin = Admin(app, name="Decider Admin (for Decider decisions)", template_mode='bootstrap3')
admin.add_view(ModelView(Token, db_session))
admin.add_view(ModelView(Question, db_session))
admin.add_view(ModelView(QuestionEffect, db_session))

# kill db session on server shutdown
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.run(debug=True)