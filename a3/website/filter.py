from flask import Blueprint, render_template, redirect, url_for
from .models import Concert

bp = Blueprint('filter', __name__)

@bp.route('/genres/<genre>')
def genres(genre):
    if genre!= None:
        concerts = Concert.query.filter(Concert.event_genres.like(genre)).all()
        return render_template('index.html', destinations=concerts)
    else: 
        return redirect(url_for('main.index'))