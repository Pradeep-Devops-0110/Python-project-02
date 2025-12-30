# app.py
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_app.extensions import db, migrate, jwt
from flask_app.config import get_config
from flask_app.auth import auth_bp, current_user_optional
from flask_app.posts import posts_bp, list_posts
from flask_app.models import Post




def create_app(config_name="prod"):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(posts_bp, url_prefix="/posts")

    @app.get("/")
    @current_user_optional
    def index(user):
        posts = list_posts()
        return render_template("index.html", posts=posts, user=user)

    @app.post("/search")
    def search():
        q = request.form.get("q", "").strip()
        results = Post.query.filter(Post.title.ilike(f"%{q}%")).order_by(Post.created_at.desc()).all()
        return render_template("index.html", posts=results, user=None)
    
    @app.get("/api/posts")
    def api_posts():
        posts = list_posts()
        return {"posts": [post.to_dict() for post in posts]}

    return app

if __name__ == "__main__":
    app = create_app("dev")
    app.run(host="0.0.0.0", port=5000)
