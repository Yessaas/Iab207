from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateField, TimeField,IntegerField, SelectField
from wtforms.validators import InputRequired, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed
ALLOWED_FILE = {'PNG','JPG','png','jpg'}

#Create new destination
# class DestinationForm(FlaskForm):
#   name = StringField('Country', validators=[InputRequired()])
#   description = TextAreaField('Description', 
#             validators=[InputRequired()])
#   image = FileField('Destination Image', validators=[
#     FileRequired(message='Image cannot be empty'),
#     FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])
#   currency = StringField('Currency', validators=[InputRequired()])
#   submit = SubmitField("Create")
    
#User login
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

#User register
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    #submit button
    submit = SubmitField("Register")

#User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')

class ConcertForm(FlaskForm):
  event_name = StringField('Event Title', validators=[InputRequired()])
  event_artists = StringField('Event Artist/s', validators=[InputRequired()])
  event_status = SelectField('Status',choices=[("Open"), ("Unpublished")], validators=[InputRequired()])
  event_genres = SelectField('Genres', 
      choices=[("Pop"), ("Rock"), ("EDM"), ("Country"), ("R&B"), ("Other")],
      validators=[InputRequired()])
  event_date = DateField('Date', format='%Y-%m-%d', validators=[InputRequired()])
  event_time = TimeField('Start Time',validators=[InputRequired()])
  event_description = TextAreaField('Description',
                                    validators=[InputRequired()])
  event_image = FileField('Event Image', validators=[
      FileRequired(message='Must Add Image'),
      FileAllowed(ALLOWED_FILE, message='Only supports jpg, png, JPG, PNG')])
  event_ticket_cost = IntegerField('Cost Of Ticket', validators=[InputRequired()])
  event_total_tickets = IntegerField('Total Number Of Tickets', validators=[InputRequired()])
  event_location = StringField('Venue Location ', validators=[InputRequired()])
  event_duration = StringField('Duration', validators=[InputRequired()])
  event_submit = SubmitField("Create")

class UpdateForm(FlaskForm):
    event_name = StringField('Event Name')
    event_artists = StringField('Event Artist/s')
    event_status = SelectField('Status',choices=[("Open"), ("Unpublished"), ("Cancelled")])
    event_genres = SelectField('Genre', 
        choices=[("Pop"), ("Rock"), ("EDM"), ("Country"), ("R&B"), ("Other")],
        validators=[InputRequired()])
    event_date = DateField('Date', format='%Y-%m-%d')
    event_time = TimeField('Start Time')
    event_description = TextAreaField('Description')
    event_image = FileField('Event Image', validators=[
        FileRequired(message='Must Add Image'),
        FileAllowed(ALLOWED_FILE, message='Only supports jpg, png, JPG, PNG')])
    event_ticket_cost = IntegerField('Cost Of Ticket')
    event_total_tickets = IntegerField('Total Number Of Tickets')
    event_location = StringField('Venue Location ')
    event_duration = StringField('Duration')
    event_submit = SubmitField("Update Event")
    event_remove = SubmitField('Remove Event')

class BookingForm(FlaskForm):
    quantity = IntegerField('Number Of Tickets', validators=[InputRequired()])
    submit = SubmitField('Book')
