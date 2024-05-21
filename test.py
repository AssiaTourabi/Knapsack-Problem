from flask import Flask, render_template, request
from knapsac import Knapsack  # Assurez-vous que ce fichier est nommé knapsack.py et est dans le même répertoire
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve_knapsack():
    capacity = int(request.form['capacity'])
    weights = [int(w) for w in request.form['weights'].split(',')]
    values = [int(v) for v in request.form['values'].split(',')]

    # Création de l'objet Knapsack
    knapsack = Knapsack(capacity, len(weights), weights, values)

    results = []

    def test_method(method_name):
        method = getattr(knapsack, method_name)
        start_time = time.time()
        solution, value = method()
        end_time = time.time()
        results.append({
            'method': method_name,
            'solution': solution,
            'value': value,
            'time': end_time - start_time
        })

    methods_to_test = [
        'best_improvement_ls',
        'first_improvement_ls',
        'full_random',
        'homogene_sa',
        'no_homogene_sa'
    ]

    for method in methods_to_test:
        test_method(method)

    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
