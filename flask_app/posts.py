# posts.py
from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_app.extensions import db
from flask_app.models import Post, User



posts_bp = Blueprint("posts", __name__, template_folder="templates")

def list_posts():
    """Return all posts ordered by creation date (newest first)."""
    return Post.query.order_by(Post.created_at.desc()).all()

@posts_bp.get("/dashboard")
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc()).all()
    return render_template("index.html", posts=posts, user=User.query.get(user_id))

# API endpoints
@posts_bp.post("/api")
@jwt_required()
def create_post():
    data = request.get_json() or {}
    title = data.get("title")
    body = data.get("body")
    if not title or not body:
        return jsonify({"msg": "title and body required"}), 400
    post = Post(title=title, body=body, user_id=get_jwt_identity())
    db.session.add(post)
    db.session.commit()
    return jsonify({"id": post.id, "title": post.title, "body": post.body}), 201

@posts_bp.get("/api")
@jwt_required()
def list_posts_api():
    user_id = get_jwt_identity()
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc()).all()
    return jsonify([{"id": p.id, "title": p.title, "body": p.body} for p in posts])

@posts_bp.put("/api/<int:post_id>")
@jwt_required()
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != get_jwt_identity():
        return jsonify({"msg": "forbidden"}), 403
    data = request.get_json() or {}
    post.title = data.get("title", post.title)
    post.body = data.get("body", post.body)
    db.session.commit()
    return jsonify({"id": post.id, "title": post.title, "body": post.body})

@posts_bp.delete("/api/<int:post_id>")
@jwt_required()
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != get_jwt_identity():
        return jsonify({"msg": "forbidden"}), 403
    db.session.delete(post)
    db.session.commit()
    return jsonify({"msg": "deleted"})
