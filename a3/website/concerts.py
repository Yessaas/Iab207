from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Comment, Concert, Booking
from .forms import CommentForm, ConcertForm, UpdateForm, BookingForm
from . import db, app
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_login import login_required, current_user

bp = Blueprint('concert', __name__, url_prefix='/destinations')

# @bp.route('/concert_details/<concert_id>')
# def concert_details(concert_id):
#     # Assuming you have a way to get the concert details
#     concerts = Concert.query.get(concert_id)
#     comments = Comment.query.filter_by(concert_id=concert_id).order_by(Comment.created_at.desc()).all()
#     form = CommentForm()
#     return render_template('concert_details.html', concerts=concerts, comments=comments, form=form)


@bp.route('/<id>')
def show(id):
    concert = Concert.query.filter_by(event_id=id).first()

    commentForm = CommentForm()    
    return render_template('destinations/show.html', concerts=concert, form=commentForm)
@bp.route('/mybookings')
@login_required
def mybookings():
    tickets = Booking.query.filter_by(user_id=current_user.id)
    concert = Concert.query.all()

    commentForm = CommentForm()    
    return render_template('destinations/mybookings.html', tickets=tickets, concert=concert, form=commentForm)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
	print('Method type: ', request.method)
	concertForm = ConcertForm()
	if concertForm.validate_on_submit():
		db_file_path = check_upload_file(concertForm)
		event = Concert(event_name=concertForm.event_name.data,
						event_artists=concertForm.event_artists.data,
						event_status=concertForm.event_status.data,
						event_genres=concertForm.event_genres.data,
						event_date=concertForm.event_date.data,
						event_time=concertForm.event_time.data,
						event_description=concertForm.event_description.data,
						event_image=db_file_path,
						event_ticket_cost=concertForm.event_ticket_cost.data,
						event_total_tickets=concertForm.event_total_tickets.data,
						event_duration=concertForm.event_duration.data,
						event_location=concertForm.event_location.data,
						user_id=current_user.id
						)


		db.session.add(event)

		db.session.commit()
		print('Created new concert succesfully')
		# Redirect if form is valid to reload page
		return redirect(url_for('concert.create'))
	return render_template('destinations/create.html', form=concertForm)

@bp.route('/myevents', methods=['GET', 'POST'])
@login_required
def myevents():
    concerts = Concert.query.all()
    return render_template('destinations/myevents.html', event=concerts)

@bp.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
# here the form is created  form = CommentForm()
	print('Method type: ', request.method)
	eventOb = Concert.query.filter_by(event_id=id).first()
	updateForm = UpdateForm()
	editevent = Concert.query.get(id)
	if request.method == 'GET':
		updateForm.event_name.data = editevent.event_name
		updateForm.event_artists.data = editevent.event_artists
		updateForm.event_status.data = editevent.event_status
		updateForm.event_genres.data = editevent.event_genres
		updateForm.event_date.data = editevent.event_date
		updateForm.event_time.data = editevent.event_time
		updateForm.event_description.data = editevent.event_description
		updateForm.event_image = editevent.event_image
		updateForm.event_ticket_cost.data = editevent.event_ticket_cost
		updateForm.event_total_tickets.data = editevent.event_total_tickets
		updateForm.event_duration.data = editevent.event_duration
		updateForm.event_location.data = editevent.event_location
	db.session.delete(eventOb)
	if updateForm.event_remove.data:
		db.session.delete(eventOb)
		db.session.commit()
		return redirect(url_for('concert.myevents'))
	elif updateForm.validate_on_submit():
		db_file_path = check_upload_file(updateForm)
		eventOb = Concert(event_name=updateForm.event_name.data,
							event_artists=updateForm.event_artists.data,
							event_status=updateForm.event_status.data,
							event_genres=updateForm.event_genres.data,
							event_date=updateForm.event_date.data,
							event_time=updateForm.event_time.data,
							event_description=updateForm.event_description.data,
							event_image=db_file_path,
							event_ticket_cost=updateForm.event_ticket_cost.data,
							event_total_tickets=updateForm.event_total_tickets.data,
							event_duration=updateForm.event_duration.data,
							event_location=updateForm.event_location.data,
							user_id=current_user.id)
		db.session.add(eventOb)
		db.session.commit()
		flash('Your event has been edited', 'success')
		return redirect(url_for('concert.myevents'))
	return render_template('destinations/edit.html', event=eventOb, form=updateForm)

@bp.route('/book/<id>', methods=['GET', 'POST'])
@login_required
def book(id):
    book = Concert.query.filter_by(event_id=id).first()
    tickets = Booking.query.count()
    bookingForm = BookingForm()
    concertName = book.event_name
    if bookingForm.validate_on_submit():
        if book.event_total_tickets == 0:
            flash('Sold Out')
            return redirect(url_for('concert.book', id=book.event_id))
        elif bookingForm.quantity.data > book.event_total_tickets:
            flash(
                'Order can not be placed, number of tickets entered excceeds available tickets')
            return redirect(url_for('concert.book', id=book.event_id))

        total_price = bookingForm.quantity.data * book.event_ticket_cost
        book.event_total_tickets = book.event_total_tickets - bookingForm.quantity.data

        tickets = int(tickets + 1)
        booking = Booking(total_price=total_price,
                          quantity=bookingForm.quantity.data,
                          purchase_date=datetime.now(),
                          order_id=tickets,
                          user_id=current_user.id,
                          event_id=id,)

        db.session.add(booking)
        db.session.commit()
        flash("Booking Successfull for " + str(concertName) + " " + "for total Price $" +
              str(total_price) + "," + " " + "Your Order ID is "+str(tickets))
        return redirect(url_for('concert.mybookings', id=book.event_id))
    return render_template('destinations/book.html', book=book, form=bookingForm)

def check_upload_file(form):
  #get file data from form  
  fp=form.event_image.data
  filename=fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH=os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path=os.path.join(BASE_PATH,'static/image',secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path='/static/image/' + secure_filename(filename)
  #save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path

@bp.route('/<concert>/comment', methods = ['GET', 'POST'])  
@login_required
def comment(destination):  
    form = CommentForm()  
    #get the destination object associated to the page and the comment
    destination_obj = Concert.query.filter_by(event_id=destination).first()  
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data,  
                        destination=destination_obj,
                        user=current_user) 
      #here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 

      #flashing a message which needs to be handled by the html
      #flash('Your comment has been added', 'success')  
      print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('concert.show', id=destination))
    