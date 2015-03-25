from app import create_app, db
from app.models import Usuario


if __name__ == "__main__":
    app = create_app("deployment")
    with app.app_context():
        db.create_all()
        if Usuario.query.filter_by(nombre='omar').first() is None:
            Usuario.registra('omar', 'muppets')
        app.run()
