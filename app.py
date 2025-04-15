from flask import Flask, render_template, request, redirect, url_for
import csv
from datetime import datetime

app = Flask(__name__)
print("Flask app is loading...")


# Load events from CSV
def load_events():
    events = []
    with open('data/sample_events.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            events.append(row)
    return events

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/events')
def events():
    search = request.args.get('search', '').lower()
    events = load_events()
    if search:
        events = [e for e in events if search in e['name'].lower()]
    return render_template('events.html', events=events, search=search)

@app.route('/order/<event_id>', methods=['GET', 'POST'])
def order(event_id):
    events = load_events()
    event = next((e for e in events if e['event_id'] == event_id), None)
    if request.method == 'POST':
        name = request.form['name']
        qty = int(request.form['quantity'])
        ticket_price = float(event['price'])
        total = ticket_price * qty

        with open('data/orders.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now(), name, event_id, qty, total])

        return redirect(url_for('confirmation', name=name, total=total))

    return render_template('order.html', event=event)

@app.route('/confirmation')
def confirmation():
    name = request.args.get('name')
    total = request.args.get('total')
    return render_template('confirmation.html', name=name, total=total)

if __name__ == '__main__':
    app.run(debug=True)
