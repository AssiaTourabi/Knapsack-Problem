import os
from flask import Flask, render_template, request
from knapsac import Knapsack 
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/solveFile', methods=['POST'])
def solve():
    capacity = request.form['capacity']
    weights = request.form['weights']
    values = request.form['values']

    file = request.files['file']
    if file and file.filename != '':
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        with open(filename, 'r') as f:
            data = f.readlines()
            capacity = int(data[0].strip())
            weights = list(map(int, data[1].strip().split(',')))
            values = list(map(int, data[2].strip().split(',')))
    else:
        capacity = int(capacity)
        weights = list(map(int, weights.split(',')))
        values = list(map(int, values.split(',')))

    results = solve_knapsack(capacity, weights, values)
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
