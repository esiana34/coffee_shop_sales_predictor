from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import SubmitField, MultipleFileField
from flask import Flask, render_template, request, session
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from src.data.data_refining.data_cleaning import calendarSetup

# --- Setup ---
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model and encoder
model = joblib.load("model/model.pkl")
encoder = joblib.load("model/encoder.pkl")

# Configurations
app = Flask(__name__,
            template_folder=r"C:\Users\esian\Desktop\Kafe\templates",
            static_folder=r"C:\Users\esian\Desktop\Kafe\static")
CORS(app)
app.config['SECRET_KEY'] = "supersecret"
app.config['UPLOAD_FOLDER'] = r"C:\Users\esian\Desktop\Kafe\src\data\raw_data"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# --- File Upload Form ---
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

    if form.validate_on_submit():
        uploaded_files = form.file.data
        for upload_file in uploaded_files:
            if upload_file:
                filename = secure_filename(upload_file.filename)
                upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template("upload.html", form=form)


# --- Save Geolocation ---
@app.route("/get-location", methods=["POST"])
def get_location():
    data = request.get_json()
    session["latitude"] = data.get("latitude")
    session["longitude"] = data.get("longitude")
    return {"message": "Location saved to session"}


# prediction tab
@app.route('/predict', methods=["POST"])
def predict():
    if request.method == "GET":
        # show empty upload form
        return render_template('predict.html', prediction_text='', result_df=pd.DataFrame())

    try:
        latitude = getattr(g, 'latitude', None)
        longitude = getattr(g, 'longitude', None)

    cal = calendarSetup(latitude, longitude)
    df = cal.run_full_pipeline()

        if not os.path.exists(cleaned_file):
            return render_template(
                'predict.html',
                prediction_text='Cannot predict future items without data.',
                result_df=pd.DataFrame()
            )


    # select features 
    feature_cols = [
        "day_of_week", "is_holiday",
        "sales_lag_1", "sales_lag_2", "sales_lag_3", "sales_lag_7",
        "temperature_2m_max", "temperature_2m_min", "precipitation_sum",
        "item_encoded"
    ]

    X = df[feature_cols]

    # Predict
    y_pred_log = model.predict(X)
    df["predicted_sales"] = np.expm1(y_pred_log)

    # Get last date in file + 1 day
    next_day = pd.to_datetime(df["date"].max()) + pd.Timedelta(days=1)
    
    # Average per item for that next day prediction
    predictions = df.groupby("item")["predicted_sales"].mean().round(1)

    # Create a simple DataFrame with text
    result_df = pd.DataFrame({
        "date": [next_day] * len(predictions),
        "item": predictions.index,
        "predicted_sales": predictions.values
    })

    return render_template ('index.html', prediction_text = 'Next day predicted sales:\n {}'.format(result_df))
    


if __name__ == "__main__":
    app.run(debug=True)
    
 