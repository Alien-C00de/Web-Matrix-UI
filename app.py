# app.py
from flask import Flask, render_template, request, url_for, flash, send_from_directory, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import subprocess
import os
import datetime
from urllib.parse import urlparse
from Tool.util.URL_Verifier import URL_Verifier
from Tool.util.config_uti import Configuration

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'a_very_secret_key_that_should_be_changed') # CHANGE THIS!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_very_secret_key_here' # Important for flash messages

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # Redirect to 'login' view if @login_required fails
login_manager.login_message_category = 'info' # Flash message category

# Path setup
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))  # Web_Matrix/
TOOL_DIR = os.path.join(BASE_DIR, 'Tool')
OUTPUT_DIR = os.path.join(TOOL_DIR, 'output')

# --- Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False) # Increased length for stronger hashes

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Forms ---
class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please use a different one or login.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()]) # Login with email
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data) # Use the method
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') # For redirecting after login if accessed a protected page
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required # This route requires the user to be logged in
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

@app.route('/report', methods=['GET', 'POST'])
@login_required # This route requires the user to be logged in
def report():
    report_file_url = None
    submitted_website = None
    submitted_mode = None
    report_html_content = None

    if request.method == 'POST':
        website_name = request.form.get('website_name').strip()
        if not (website_name.startswith("http://")) and not (website_name.startswith('https://')):
            website_name = "https://" + website_name
            
        report_mode = request.form.get('report_mode').strip()

        if not __Is_Valid_Site:
            flash('Website name is required.', 'danger')
            return render_template('report.html', error="Please enter a website name.")
        

        # Construct the command to run the external tool
        result = urlparse(website_name)
        domain = result.netloc
        timestamp = str(datetime.datetime.now().strftime("%d%b%Y_%H-%M-%S"))
        html_report = "%s_%s_%s.html" % (Configuration.REPORT_FILE_NAME, domain, timestamp)
        output_file = os.path.join(TOOL_DIR, 'output', html_report)
        tool_path = os.path.join(TOOL_DIR, 'main.py')
        

        # Run the external Python tool
        command = ['python', tool_path, '-s', website_name, '-t', timestamp, '-m', report_mode]
        
        try:
            result = subprocess.run(command, check=True)
            
            print(f"Flask: Tool STDOUT:\n{result.stdout}")
            if result.stderr:
                print(f"Flask: Tool STDERR:\n{result.stderr}")

            # Now, check if the file was actually created by the tool
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8') as f:
                    report_html_content = f.read()
                report_file_url = url_for('serve_tool_report', filename=html_report)
                flash(f'Report generated successfully for {website_name}!', 'success')
                submitted_website = website_name
                submitted_mode = report_mode
            else:
                flash(f'Tool ran, but report file not found at {output_file}. Check tool logs.', 'danger')
                print(f"Flask: Error - Tool ran, but report file not found: {output_file}")


        except subprocess.CalledProcessError as e:
            flash(f"Tool failed: {e.stderr or e.stdout}", 'danger')
            print(f"Subprocess error: {e}")
        except Exception as e:
            flash(f"Unexpected error: {str(e)}", 'danger')
            print(f"Unexpected error: {e}")

    return render_template(
                            'report.html',
                            report_file_url=report_file_url,  # 👈 Add this
                            report_html_content=report_html_content,
                            submitted_website=submitted_website,
                            submitted_mode=submitted_mode
                            )

@app.route('/Tool/output/<path:filename>')
def serve_tool_report(filename):
    return send_from_directory(OUTPUT_DIR, filename)

# --- Helper to create DB (run once from Python console or with a CLI command) ---
def create_db():
    with app.app_context():
        db.create_all()
    print("Database tables created!")

# Is the given URL is valid or not
def __Is_Valid_Site(self):
    auth = URL_Verifier(self.url)
    if auth.is_url() or auth.is_ip_address():
        # print(f"[+] Valid Website : {self.url}", flush=True)
        return True
    else:
        return False

if __name__ == '__main__':
    if not os.path.exists('users.db'): # This path is relative to where app.py is
        create_db()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    REPORTS_DIR = os.path.join(current_dir, 'static', 'reports')
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    # Make sure TERMINAL_TOOL_SCRIPT path is also correct if it's not in the same dir
    # TERMINAL_TOOL_SCRIPT = os.path.join(current_dir, 'terminal_tool.py')

    app.run(debug=True)

