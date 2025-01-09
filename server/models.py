from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_author(self, key, address):
        if address == "":
            raise ValueError("Name must not be empty")
        
        count = db.session.query(func.count(Author.name)).filter(Author.name == address).all()
        if count[0][0] > 0: 
            raise ValueError("Duplicate name found")
        return address
    
    @validates('phone_number')
    def validate_phone_number(self, key, address):
        cleaned_number = int("".join(filter(str.isdigit, address)))
        if len(str(cleaned_number)) != 10:
            raise ValueError("Phone number must be 10 digits")
        return address

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, address):
        if len(str(address)) < 250:
            raise ValueError("Post must me longer than 250 characters")
        return address

    @validates('summary')
    def validate_summary(self, key, address):
        if len(str(address)) > 250:
            raise ValueError("Post summary must be shorter than 250 characters")
        return address

    @validates('category')
    def validate_category(self, key, address):
        if address != "Fiction" and address != "Non-Fiction":
            raise ValueError("Post category must be either Fiction or Non-Fiction")
        return address
    
    @validates('title')
    def validate_title(self, key, address):
        find_list = ["Won't Believe", "Secret", "Top", "Guess"]
        match = [address.find(word) != -1 for word in find_list]
        if not any(match):
            raise ValueError("Title must contain click bait words")
        return address


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
