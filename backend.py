from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Simple in-memory database
logs = []

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()}), 200

# Get all logs
@app.route('/api/logs', methods=['GET'])
def get_logs():
    return jsonify({'logs': logs, 'count': len(logs)}), 200

# Create new log entry
@app.route('/api/logs', methods=['POST'])
def create_log():
    data = request.get_json()
    
    if not data or 'stimulus' not in data:
        return jsonify({'error': 'stimulus field is required'}), 400
    
    log_entry = {
        'id': len(logs) + 1,
        'stimulus': data.get('stimulus'),
        'response': data.get('response', ''),
        'timestamp': datetime.now().isoformat(),
        'notes': data.get('notes', '')
    }
    
    logs.append(log_entry)
    return jsonify(log_entry), 201

# Get single log by ID
@app.route('/api/logs/<int:log_id>', methods=['GET'])
def get_log(log_id):
    for log in logs:
        if log['id'] == log_id:
            return jsonify(log), 200
    return jsonify({'error': 'Log not found'}), 404

# Update log entry
@app.route('/api/logs/<int:log_id>', methods=['PUT'])
def update_log(log_id):
    data = request.get_json()
    
    for log in logs:
        if log['id'] == log_id:
            log.update(data)
            return jsonify(log), 200
    
    return jsonify({'error': 'Log not found'}), 404

# Delete log entry
@app.route('/api/logs/<int:log_id>', methods=['DELETE'])
def delete_log(log_id):
    for i, log in enumerate(logs):
        if log['id'] == log_id:
            deleted_log = logs.pop(i)
            return jsonify({'message': 'Log deleted', 'log': deleted_log}), 200
    
    return jsonify({'error': 'Log not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
