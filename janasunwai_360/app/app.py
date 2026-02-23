import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from app.services.supabase_client import supabase
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from datetime import datetime, timezone
from pathlib import Path
from werkzeug.security import check_password_hash

env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET', 'supersecretkey') 

BASE_DIR = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    try:
        response = supabase.table("issues").select("*").order("created_at", desc=True).limit(3).execute()
        posts = response.data or []
    except Exception:
        posts = []

    return render_template(
        "index.html",
        site_name="Janasunwai 360",
        tagline="Building Trust Through Transparency",
        posts=posts
    )

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        admin_code = request.form.get("admin_code")
        password = request.form.get("password")

        res = supabase.table("officials").select("*").eq("admin_code", admin_code).execute()
        user_data = res.data[0] if res.data else None

        if user_data and check_password_hash(user_data['password'], password):
            session['user_id'] = user_data['id']
            session['is_official'] = True
            session['name'] = user_data['full_name']
            
            flash(f"Access Granted. Welcome {user_data['full_name']}", "success")
            return redirect(url_for('profile'))
        else:
            flash("Invalid Admin Code or Password", "error")

    return render_template("login.html")

@app.route("/logout", methods=['POST'])
def logout():
    session.clear()
    flash("Session terminated successfully", "success")
    return redirect(url_for('home'))

@app.route("/profile")
def profile():
    if not session.get('is_official'):
        return redirect(url_for('login'))
    return render_template("profile.html", current_user=session.get('name'))

@app.route("/submit_issue", methods=['GET', 'POST'])
def submit_issue():
    if request.method == 'POST':
        title = request.form.get("title")
        description = request.form.get("description")
        district = request.form.get("district")
        municipality = request.form.get("municipality")
        impact = request.form.get("priority", "medium").lower()
        image = request.files.get('attachments') 
        image_url = None

        if image and image.filename and allowed_file(image.filename):
            timestamp = int(datetime.now(timezone.utc).timestamp())
            image_filename = f"{timestamp}_{secure_filename(image.filename)}"
            local_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image.save(local_path)

            bucket_name = os.getenv('SUPABASE_STORAGE_BUCKET', 'images')
            try:
                with open(local_path, 'rb') as f:
                    supabase.storage.from_(bucket_name).upload(
                        path=image_filename, 
                        file=f,
                        file_options={"content-type": image.content_type}
                    )
                url_resp = supabase.storage.from_(bucket_name).get_public_url(image_filename)
                image_url = url_resp if isinstance(url_resp, str) else url_resp.public_url
            except Exception as e:
                flash(f'Media upload failed: {str(e)}', 'error')

        issue = {
            "title": title,
            "description": description,
            "district": district,
            "municipality": municipality,
            "impact": impact,
            "image_url": image_url,
            "status": "open",
            "is_anonymous": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        try:
            supabase.table("issues").insert(issue).execute()
            flash("Report filed successfully and anonymously.", "success")
        except Exception as e:
            flash('Submission failed: ' + str(e), 'error')
            return redirect(url_for('submit_issue'))

        return redirect(url_for("public_issue"))

    return render_template("submit_issue.html", site_name="Janasunwai 360")

@app.route("/public_issue")
def public_issue():
    q = request.args.get('q', '').strip()
    status = request.args.get('status', '').strip()

    try:
        query = supabase.table("issues").select("*")
        if q: query = query.ilike("title", f"%{q}%")
        if status: query = query.eq("status", status)

        response = query.order("created_at", desc=True).execute()
        posts = response.data or []
    except Exception as e:
        flash('Failed to fetch records: ' + str(e), 'error')
        posts = []

    return render_template("public_issue.html", posts=posts, current_user=session.get('name'))

@app.route("/official_dashboard")
def official_dashboard():
    if not session.get('is_official'):
        return redirect(url_for('login'))
    
    response = supabase.table("issues").select("*").order("created_at", desc=True).execute()
    return render_template("official_dashboard.html", posts=response.data or [])

@app.route("/update_issue/<post_id>", methods=["POST"])
def update_issue(post_id):
    if not session.get('is_official'):
        return redirect(url_for('login'))

    new_status = request.form.get("status")
    admin_notes = request.form.get("admin_notes")

    update_data = {
        "status": new_status,
        "admin_notes": admin_notes,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }

    try:
        supabase.table("issues").update(update_data).eq("id", post_id).execute()
        flash(f"Record #{post_id} updated successfully.", "success")
    except Exception as e:
        flash('Update failed: ' + str(e), 'error')

    return redirect(request.referrer or url_for('public_issue'))

@app.route("/budget_tracker")
def budget_tracker():
    return render_template(
        "budget_tracker.html", 
        total_budget=545000000, 
        total_spent=392400000
    )

@app.route("/about")
def about():
    return render_template("about.html", site_name="Janasunwai 360")

@app.route("/up_vote/<post_id>", methods=["POST"])
def upvote(post_id):
    try:
        res = supabase.table("issues").select("upvote").eq("id", post_id).single().execute()
        current = res.data.get("upvote", 0) if res.data else 0
        supabase.table("issues").update({"upvote": current + 1}).eq("id", post_id).execute()
        flash("Upvote registered.", "success")
    except Exception:
        flash("Voting failed.", "error")
    return redirect(request.referrer or url_for('public_issue'))

@app.route("/issue/<post_id>")
def issue_details(post_id):
    try:
        # Fetch the specific issue from Supabase
        res = supabase.table("issues").select("*").eq("id", post_id).single().execute()
        post = res.data
        if not post:
            flash("Issue not found.", "error")
            return redirect(url_for('public_issue'))
            
        return render_template("issue_details.html", post=post)
    except Exception as e:
        flash(f"Error loading issue: {str(e)}", "error")
        return redirect(url_for('public_issue'))

if __name__ == "__main__":
    app.run(debug=True)