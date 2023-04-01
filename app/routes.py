from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('base.html')

@main.route('/talk')
def talk():
    return render_template('talk.html')

@main.route('/game')
def test():
    return render_template('game.html')
