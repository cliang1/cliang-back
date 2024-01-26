from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)

# Configure SQLAlchemy database URI and track modifications
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set a secret key for session management
app.config['SECRET_KEY'] = 'SECRET_KEY'

# Initialize SQLAlchemy database object
db = SQLAlchemy(app)

# Create the table if it doesn't already exist
with app.app_context():
    db.create_all()

# Define User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    uid = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.Date)

    def __init__(self, name, uid, password, dob=None):
        self.name = name
        self.uid = uid
        self.password = generate_password_hash(password)
        self.dob = dob

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'uid': self.uid,
            'dob': self.dob.strftime('%Y-%m-%d') if self.dob else None
        }



# Add a route for a simple welcome page
@app.route('/api/data', methods=['GET'])
def get_data():
    # Implement logic to fetch and return data
    return jsonify({'data': 'Hello from the backend!'})

@app.route('/api/data', methods=['POST'])
def create_data():
    # Implement logic to create a new resource
    return jsonify({'message': 'Resource created successfully'})

# Route to create a new user
@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    uid = data.get('uid')
    password = data.get('password')
    dob = datetime.strptime(data.get('dob'), '%Y-%m-%d') if data.get('dob') else None

    user = User(name=name, uid=uid, password=password, dob=dob)
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify(user.serialize()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'User with this UID already exists'}), 400

# Function to initialize users
def init_users():
    with app.app_context():
        u1 = User(name='Thomas Edison', uid='toby', password='123toby', dob=datetime(1847, 2, 11))
        u2 = User(name='Nikola Tesla', uid='niko', password='123niko')
        u3 = User(name='Alexander Graham Bell', uid='lex', password='123lex')
        u4 = User(name='Eli Whitney', uid='whit', password='123whit')
        u5 = User(name='Indiana Jones', uid='indi', password= '123ind', dob=datetime(1920, 10, 21))
        u6 = User(name='Marion Ravenwood', uid='raven', password= '123rav', dob=datetime(1921, 10, 21))

        users = [u1, u2, u3, u4, u5, u6]

        for user in users:
            try:
                db.session.add(user)
                db.session.commit()
                print(f"Created new UID: {user.uid}")
            except IntegrityError:
                db.session.rollback()
                print(f"Record exists for UID: {user.uid} or error.")

# Function to check credentials
def check_credentials(uid, password):
    with app.app_context():
        user = User.query.filter_by(uid=uid).first()
        if user is None:
            return False
        return user.check_password(password)

# Run the Flask app
if __name__ == '__main__':
    # Uncomment the line below for the first run to initialize users
    init_users()
    app.run(debug=True)
