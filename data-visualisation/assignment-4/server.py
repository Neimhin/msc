from flask import Flask, request, jsonify, send_from_directory
import flask
import os
import pandas as pd

app = Flask(__name__)

# Example DataFrame
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}
df = pd.DataFrame(data)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'flags.jpg', mimetype='image/jpeg')

@app.route('/' ,methods=['GET'])
def index():
    return flask.render_template('index.html')

@app.route('/col', methods=['GET'])
def get_data():
    # Retrieve query parameters
    columns = request.args.get('columns')
    
    if not columns:
        return jsonify({"error": "No columns specified"}), 400

    try:
        # Split the columns and filter the DataFrame
        columns = columns.split(',')
        filtered_df = df[columns]

        # Convert DataFrame to JSON
        result = filtered_df.to_json(orient='records')
        return result
    except KeyError as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/new_adjacency_matrix', methods=['GET'])
def new_adjacency_matrix():
    import random
    length = random.randint(3,10)
    matrix = [[0 for i in range(length)] for i in range(length)]
    for i in range(length):
        for j in range(i,length):
            v = random.randint(0,1)
            matrix[i][j] = v
            matrix[j][i] = v

    return jsonify(matrix)

if __name__ == '__main__':
    app.run(debug=True)

