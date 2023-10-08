from app import db
from app.models import Admin
import bcrypt

def create_admin():
    # Create an admin user with a hashed password
    admin = Admin.query.filter_by(id="tmota").first() # Check if admin exists
    if not admin: # If admin does not exist, create one
        admin_password = "1"  # Replace with the actual password
        hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()) # Hash the password

        admin = Admin(id="tmota", email="tmota@msudenver.edu", passwd=hashed_password, creation_date="2023-01-01", role="admin", name="Thyago Mota", title="Professor")
        db.session.add(admin) # Add admin to the database
        db.session.commit() # Commit changes to the database