
from routes import bp
from setup import create_app

app = create_app()
app.register_blueprint(bp)
(app.run(debug=True))
