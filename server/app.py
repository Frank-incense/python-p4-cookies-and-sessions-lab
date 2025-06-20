#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Article, User

app = Flask(__name__)
CORS(app)

app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = Article.query.all()

    if len(articles) > 0:
        res = make_response(jsonify([article.to_dict() for article in articles]), 200)
        return res
    
    return make_response('', 404)

@app.route('/articles/<int:id>')
def show_article(id):
    key = 'page_views'
    if key not in session:
        session[key] = 0
    
    session[key] += 1

    if session[key] > 3:
        return make_response({'message': 'Maximum pageview limit reached'}, 401)
    
    article = Article.query.filter_by(id=id).first()
    if article:
        res = make_response(jsonify(article.to_dict()), 200)
        return res
    
    else:
        return make_response({'message': 'Article not found'}, 404) 
        
    


if __name__ == '__main__':
    app.run(port=5000,debug=True)
