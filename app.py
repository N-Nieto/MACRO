import csv
from flask import Flask, render_template, request, Response, session
from flask_session import Session
from io import BytesIO, StringIO
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
app.secret_key = '1234'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = '1234asd'
Session(app)
model_folder = 'models/'
models = {
    'model_admission': 'model_admission.pkl',
    'model_cascade': 'model_cascade.pkl',
    'model_24hs': 'model_24hs.pkl'
}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        if 'file' not in request.files:
            return render_template('index.html', error='No file uploaded.')

        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error='Invalid file name.')

        selected_model = request.form.get('model')
        model_path = model_folder + models.get(selected_model)

        try:
            model = joblib.load(model_path)
        except Exception as e:
            return render_template('index.html', error=str(e))

        # Read the CSV file
        csv_data = file.read().decode('utf-8')
        csv_file = BytesIO(csv_data.encode('utf-8'))
        df = pd.read_csv(csv_file, index_col=0)
        session['df'] = df  # Store the DataFrame in the session
        patient_id = df.loc[:, "patient_ID"]
        # Remove the patient ID column if exists
        if 'patient_ID' in df.columns:
            data = df.drop('patient_ID', axis=1)

        # Prepare input data for prediction
        data = data.to_numpy(dtype=float)

        # Perform prediction using the selected model
        try:
            # Get class probabilities
            probabilities = np.round(model.predict_proba(data)[:, 1],
                                     decimals=4)
            # Assign risk categories based on thresholds
            risk_categories = np.select(
                [probabilities < 0.4, probabilities < 0.6],
                ['No Risk', 'Uncertain'],
                'Risk'
            )
            # Convert probabilities to list format
            probabilities = probabilities.tolist()
            # Convert risk categories to list format
            risk_categories = risk_categories.tolist()
        except Exception as e:
            return render_template('index.html', error=str(e))

        return render_template('prediction.html', patient_id=patient_id,
                               probabilities=probabilities,
                               risk_categories=risk_categories)

    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    patient_ids = request.form.getlist('patient_id')
    probabilities = request.form.getlist('probability')
    risk_categories = request.form.getlist('risk_category')

    # Create the CSV response for download
    csv_output = StringIO()
    csv_writer = csv.writer(csv_output, delimiter=',', quotechar='"')
    csv_writer.writerow(['Patient ID', 'Probability', 'Risk Category'])

    for patient_id, probability, risk_category in zip(patient_ids, probabilities, risk_categories): # noqa
        csv_writer.writerow([patient_id, probability, risk_category])

    csv_output.seek(0)  # Move the cursor to the beginning of the stream

    return Response(
        csv_output.getvalue(),
        headers={
            'Content-Disposition': 'attachment; filename=predictions.csv',
            'Content-Type': 'text/csv'
        }
    )


@app.route('/data_show', methods=['GET', 'POST'])
def data_show():
    if 'df' in session:
        df = session['df']
    else:
        df = None

    if request.method == 'POST':
        inspect_data = request.form.get('inspect_data')
        if inspect_data == 'true':
            return render_template('data_show.html', df=df)

    return render_template('data_show.html', df=df)


@app.route('/return', methods=['POST'])
def return_to_index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
