from app import create_app, db
from models import Material

app = create_app()

with app.app_context():
    print('Material table:', Material.__table__)
    print('Existing tables:', db.engine.table_names())