from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import and_

app = Flask(__name__)

# Set your DB URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model
class FurnaceLogs(db.Model):
    __tablename__ = 'furnace_logs'  # New table name

    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def as_dict(self):
        return {
            'temperature': self.temperature,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }


# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_temp():
    try:
        temp = float(request.form['temperature'])
        print(f"Received Temperature: {temp}")
        data = FurnaceLogs(temperature=temp)
        db.session.add(data)
        db.session.commit()
        print("Temperature saved to database.")
        return jsonify({'status': 'success'})
    except Exception as e:
        print("Error occurred:", e)
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/fetch', methods=['GET'])
def fetch_data():
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    min_temp = request.args.get('min_temp')
    max_temp = request.args.get('max_temp')

    print(f"Received filters -> start: {start_date}, end: {end_date}, min: {min_temp}, max: {max_temp}")

    query = FurnaceLogs.query

    if start_date:
        query = query.filter(FurnaceLogs.timestamp >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
        query = query.filter(FurnaceLogs.timestamp < end_dt)

    if min_temp:
        query = query.filter(FurnaceLogs.temperature >= float(min_temp))
    if max_temp:
        query = query.filter(FurnaceLogs.temperature <= float(max_temp))

    result = [record.as_dict() for record in query.order_by(FurnaceLogs.timestamp.desc()).all()]
    print(f"Fetched {len(result)} records after filtering.")
    return jsonify(result)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
