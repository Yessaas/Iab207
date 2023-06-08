from flask import Blueprint, render_template, request, redirect,url_for
from .models import Concert

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    concerts = Concert.query.all()    
    return render_template('index.html', destinations=concerts)

@mainbp.route('/search')
def search():
    if request.args['search']:
        print(request.args['search'])
        dest = "%" + request.args['search'] + '%'
        concerts = Concert.query.filter(Concert.event_genres.like(dest)).all()
        return render_template('index.html', destinations=concerts)
    else:
        return redirect(url_for('main.index'))