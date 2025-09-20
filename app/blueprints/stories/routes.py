from flask import render_template, redirect, url_for, flash
from . import stories_bp
from .forms import CommentForm

# Fake in-memory comments for now
comments = []

@stories_bp.route("/stories", methods=["GET", "POST"])
def stories():
    form = CommentForm()
    if form.validate_on_submit():
        comments.append({"username": form.username.data, "comment": form.comment.data})
        flash("Comment posted!", "success")
        return redirect(url_for("stories.stories"))

    # Example YouTube embeds
    videos = [
        "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "https://www.youtube.com/embed/VIDEO_ID2"
    ]
    return render_template("stories/stories.html", form=form, comments=comments, videos=videos)
