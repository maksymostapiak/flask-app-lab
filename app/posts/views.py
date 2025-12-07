from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort, session
from app import db
from .models import Post
from .forms import PostForm
from app.users.models import User
from app.posts.models import Tag

posts_bp = Blueprint("posts", __name__, url_prefix="/posts", template_folder='templates',static_folder="static")

@posts_bp.route("/", methods=["GET"])
def posts():
    posts = Post.query.filter_by(is_active=True).order_by(Post.posted.desc()).all()
    return render_template("posts/posts.html", posts=posts)

@posts_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    authors = User.query.all()
    form.author_id.choices = [(a.id, a.username) for a in authors]
    all_tags = Tag.query.all()
    form.tags.choices = [(t.id, t.name) for t in all_tags]
    if form.validate_on_submit():
        author = session.get("user", "Anonymous")
        post = Post(title=form.title.data, content=form.content.data,
                    is_active=form.is_active.data, user_id=form.author_id.data, posted=form.posted.data)
        selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        post.tags.extend(selected_tags)
        db.session.add(post)
        db.session.commit()
        flash("Post added successfully", "success")
        return redirect(url_for("posts.posts"))
        
    return render_template("posts/add_post.html", form=form)

@posts_bp.route("/<int:id>", methods=["GET"])
def detail(id):
    post = Post.query.get_or_404(id)
    return render_template("posts/detail_post.html", post=post)

@posts_bp.route("/<int:id>/update", methods=["GET", "POST"])
def update_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm()

    authors = User.query.all()
    form.author_id.choices = [(a.id, a.username) for a in authors]

    all_tags = Tag.query.all()
    form.tags.choices = [(t.id, t.name) for t in all_tags]

    if request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
        form.is_active.data = post.is_active
        form.author_id.data = post.user_id
        form.posted.data = post.posted
        form.tags.data = [t.id for t in post.tags]

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.is_active.data
        post.user_id = form.author_id.data
        post.posted = form.posted.data

        selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        post.tags = selected_tags

        db.session.commit()

        flash("Post updated", "success")
        return redirect(url_for("posts.detail", id=post.id))

    return render_template("posts/add_post.html", form=form, post=post)

@posts_bp.route("/<int:id>/delete", methods=["GET", "POST"])
def delete_post(id):
    post = Post.query.get_or_404(id)

    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted", "info")
        return redirect(url_for("posts.posts"))

    return render_template("posts/confirm_delete.html", post=post)
