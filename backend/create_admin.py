from app import app
from extensions import db
from models.user import User

def create_admin():
    with app.app_context():
        admin = User.query.filter_by(email="admin123@tma.com").first()
        if admin is None:
            admin = User(
                name = "Administrator",
                email = "admin123@tma.com",
                password = "admin123",
                role = "Admin",
                phone = "7758589624",
                status = "Active"
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully.")
        else:
            print("Admin user already exists.")

if __name__ == "__main__":
    create_admin()