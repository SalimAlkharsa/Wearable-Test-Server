from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize an empty data store
data_store = []

# Define a route that only accepts POST requests
@app.route('/post_endpoint', methods=['POST'])
def post_request_handler():
    # Check if the request contains JSON data
    if request.is_json:
        data = request.get_json()
        data_store.append(data)  # Store the posted data
        return jsonify({"message": "Received POST request", "data": data}), 200
    else:
        return jsonify({"error": "Request data must be in JSON format"}), 400

# Define a route that only accepts GET requests
@app.route('/get_endpoint', methods=['GET'])
def get_request_handler():
    return jsonify(data_store)

# Define a route that resets the data_store
@app.route('/reset_endpoint', methods=['POST'])
def reset_request_handler():
    global data_store
    data_store = []  # Clear the data store
    return jsonify({"message": "Data store reset successfully"}), 200

# Define a route that shows hello world
@app.route('/')
def index():
    return jsonify({"message": "Hello World!"})

if __name__ == '__main__':
    app.run(debug=True)
