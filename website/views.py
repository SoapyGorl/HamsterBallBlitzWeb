from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods = ['GET', 'POST'])
def home():
    All_Notes = Note.query.all()
    All_Notes.reverse()
    All_Notes_data = []
    for SingleNote in All_Notes:
        All_Notes_data.append(SingleNote.data)
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Comment is too short', category = 'error')
        elif note in All_Notes_data:
            pass
        else:
            new_note = Note(data = note, user_id = current_user.id, username = current_user.username)
            flash('Comment has been added', category = 'success')
            db.session.add(new_note)
            db.session.commit()
            All_Notes = Note.query.all()
            All_Notes.reverse()
    return render_template("home.html", user = current_user, All_Notes = All_Notes)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})
