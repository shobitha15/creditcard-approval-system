from flask import Blueprint, render_template
main_bp=Blueprint("main",__name__)
@main_bp.route("/")
def home(): return render_template("home.html")
@main_bp.route("/about")
def about(): return render_template("about.html")
@main_bp.route("/contact")
def contact(): return render_template("contact.html")
@main_bp.app_errorhandler(404)
def missing(_): return render_template("404.html"),404
