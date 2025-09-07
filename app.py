from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField, MultipleFileField
from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename
from src.data.data_refining.data_cleaning import cleanLocation


# Optional: Add a directory for uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configurations
app = Flask(__name__, template_folder=r"C:\Users\esian\Desktop\Kafe\templates")
app.config['SECRET_KEY'] = "supersecret"
app.config['UPLOAD_FOLDER'] = r"C:\Users\esian\Desktop\Kafe\src\data\raw_data"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# uplaoding class
class uploader_file(FlaskForm):
    file = MultipleFileField("File", validators=[
        FileRequired(),
        FileAllowed(['csv', 'xlsx'], 'Only CSV and XLSX files are allowed!')
    ])
    submit = SubmitField("Submit")

# Homepage
@app.route('/', methods=["GET", "POST"])
def home():
    form = uploader_file()

    # Check if the form was submitted and if the data is valid
    if form.validate_on_submit():
        uploaded_files = form.file.data
        
        
        for upload_file in uploaded_files:
            if upload_file:
               # Create a secure filename to prevent security issues
                filename = secure_filename(upload_file.filename)
                
               # Save the file to the specified UPLOAD_FOLDER
                upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    return render_template("home.html", form=form)

# Getting geolocation
@app.route('/get-location', methods=["POST"])
def save_location():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    # Process or store the location data as needed
    print(f"Received location: Latitude={latitude}, Longitude={longitude}")

    # return json for js
    return jsonify({"message": "Location received successfully"}), 200
    


if __name__ == "__main__":
    app.run(debug=True)
 