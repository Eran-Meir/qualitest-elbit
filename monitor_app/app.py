from flask import Flask, render_template, jsonify
import psutil

app = Flask(__name__)

# Initialize psutil CPU polling
psutil.cpu_percent(interval=None)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/metrics')
def get_metrics():
    """API endpoint to fetch live OS metrics."""
    # interval=0.5 calculates the average over half a second
    cpu_usage = psutil.cpu_percent(interval=0.5)
    memory_info = psutil.virtual_memory()

    return jsonify({
        'cpu_percent': cpu_usage,
        'memory_percent': memory_info.percent
    })


if __name__ == '__main__':
    # Run on port 5003
    app.run(host='0.0.0.0', port=5003)