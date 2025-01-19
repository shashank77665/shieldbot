import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from logging_config import setup_logging
from tasks import run_attacks
from celery.result import AsyncResult

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Set up logger
logger = setup_logging("ShieldBotAPI")


@app.route('/test-website', methods=['POST'])
def test_website():
    try:
        data = request.json
        base_url = data.get("base_url")
        options = data.get("options", {})

        if not base_url:
            return jsonify({"error": "base_url is required"}), 400

        # Submit attack tasks to Celery
        task = run_attacks.delay(base_url, options)
        return jsonify({"task_id": task.id, "message": "Attack tasks started"}), 202

    except Exception as e:
        logger.error(f"Error initiating tests: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/task-status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = AsyncResult(task_id)
    if task.state == 'PENDING':
        return jsonify({"status": "Pending"}), 202
    elif task.state == 'SUCCESS':
        return jsonify({"status": "Completed", "result": task.result}), 200
    elif task.state == 'FAILURE':
        return jsonify({"status": "Failed", "error": str(task.info)}), 500
    else:
        return jsonify({"status": task.state}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
