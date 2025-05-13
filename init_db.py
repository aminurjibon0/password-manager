from app import create_app, db
from app.models import User, PasswordEntry  # Ensure models are registered

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Database initialized successfully.")