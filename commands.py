# run the server
"export FLASK_APP = filename.py"
"flask run"

# Change the port
"flask run -p 9000"

# debug mode = on
"export FLASK_DEBUG=1"


# SQLALCHEMY ORM
"db.create_all()"
"Model.query.all()"
"Model.query.filter_by()"
"db.session.add(model_instance)"
"db.session.commit()"
"db.session.rollback()"