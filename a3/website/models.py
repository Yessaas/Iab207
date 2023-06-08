from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__='users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
	#password is never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)

    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='User') 
    event = db.relationship('Concert', backref='User')



# class Destination(db.Model):
#     __tablename__ = 'destinations'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80))
#     description = db.Column(db.String(200))
#     image = db.Column(db.String(400))
#     currency = db.Column(db.String(3))
#     # ... Create the Comments db.relationship
# 	# relation to call destination.comments and comment.destination
#     comments = db.relationship('Comment', backref='destination')

    
	
    # def __repr__(self): #string print method
    #     return "<Name: {}>".format(self.name)

# class Comment(db.Model):
#     __tablename__ = 'comments'
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(400))
#     created_at = db.Column(db.DateTime, default=datetime.now())
#     #add the foreign keys
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     destination_id = db.Column(db.Integer, db.ForeignKey('concerts.event_id'))


#     def __repr__(self):
#         return "<Comment: {}>".format(self.text)

class Concert(db.Model):
    __tablename__ = 'concerts'
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(80))
    event_artists = db.Column(db.String(200))
    event_status = db.Column(db.String(20))
    event_genres = db.Column(db.String(80))
    event_date = db.Column(db.Date)
    event_time = db.Column(db.Time)
    event_description = db.Column(db.String(400))
    event_image = db.Column(db.String(400))
    event_ticket_cost = db.Column(db.Integer)
    event_total_tickets = db.Column(db.Integer)
    event_location = db.Column(db.String(200))
    event_duration = db.Column(db.String(50))
    comments = db.relationship('Comment', backref='concert')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))   

    def __repr__(self): #string print method
        return "Name: {}".format(self.event_name)

class Booking(db.Model):    
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer())
    event_id = db.Column(db.Integer, db.ForeignKey('concerts.event_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    total_price = db.Column(db.Integer())
    quantity = db.Column(db.Integer())
    purchase_date = db.Column(db.DateTime, default=datetime.now())
    
    def __repr__(self): #string print method
        return "<Name: {}>".format(self.name)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('concerts.event_id'))


    def __repr__(self):
        return "<Comment: {}>".format(self.text)
