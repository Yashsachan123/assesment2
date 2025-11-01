"""
Target Server - Simulated Victim Website
This is a simple Flask server that acts as the target for DoS attacks
"""

from flask import Flask, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

# Request counter
request_count = 0


@app.route('/')
def home():
    """Main page of target website"""
    global request_count
    request_count += 1
    
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Target Website - DoS Testing</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            
            .container {
                background: white;
                padding: 50px;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                text-align: center;
                max-width: 600px;
                width: 100%;
            }
            
            h1 {
                color: #667eea;
                font-size: 2.5em;
                margin-bottom: 20px;
            }
            
            .status {
                background: #10b981;
                color: white;
                padding: 15px 30px;
                border-radius: 50px;
                display: inline-block;
                margin: 20px 0;
                font-weight: bold;
                font-size: 1.1em;
            }
            
            .info {
                background: #f3f4f6;
                padding: 30px;
                border-radius: 15px;
                margin-top: 30px;
            }
            
            .info p {
                margin: 10px 0;
                color: #4b5563;
                font-size: 1.1em;
            }
            
            .counter {
                font-size: 3em;
                color: #667eea;
                font-weight: bold;
                margin: 20px 0;
            }
            
            .description {
                color: #6b7280;
                line-height: 1.6;
                margin-top: 20px;
            }
            
            .endpoint {
                background: #1f2937;
                color: #10b981;
                padding: 10px 20px;
                border-radius: 8px;
                font-family: 'Courier New', monospace;
                margin: 10px 0;
                display: inline-block;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 Target Website</h1>
            <div class="status">✅ Server Running</div>
            
            <div class="info">
                <p><strong>Server Status:</strong> Active</p>
                <p><strong>Port:</strong> 5000</p>
                <p><strong>Total Requests Received:</strong></p>
                <div class="counter">""" + str(request_count) + """</div>
            </div>
            
            <div class="description">
                <p>This is a simulated target website for DoS attack testing.</p>
                <p>Use the detection system at <span class="endpoint">http://127.0.0.1:8000</span> to monitor traffic.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html


@app.route('/api/data')
def api_data():
    """API endpoint that can be targeted"""
    global request_count
    request_count += 1
    
    return jsonify({
        'status': 'success',
        'message': 'This is a test API endpoint',
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'request_number': request_count
    })


@app.route('/about')
def about():
    """About page"""
    global request_count
    request_count += 1
    
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>About - Target Website</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f0f0f0;
                padding: 50px;
                text-align: center;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 10px;
                max-width: 600px;
                margin: 0 auto;
            }
            h1 { color: #333; }
            p { color: #666; line-height: 1.6; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>About This Server</h1>
            <p>This is a simple Flask server used for testing DoS detection systems.</p>
            <p>Total requests: <strong>""" + str(request_count) + """</strong></p>
            <p><a href="/">← Back to Home</a></p>
        </div>
    </body>
    </html>
    """
    
    return html


@app.route('/reset')
def reset_counter():
    """Reset request counter"""
    global request_count
    old_count = request_count
    request_count = 0
    
    return jsonify({
        'status': 'success',
        'message': f'Counter reset from {old_count} to 0'
    })


if __name__ == '__main__':
    print("=" * 60)
    print("Target Server - Simulated Victim Website")
    print("=" * 60)
    print("This server simulates a website that can be targeted")
    print("for DoS attack testing and detection.")
    print("=" * 60)
    print("Available endpoints:")
    print("  - http://127.0.0.1:5000/         (Home page)")
    print("  - http://127.0.0.1:5000/about    (About page)")
    print("  - http://127.0.0.1:5000/api/data (API endpoint)")
    print("  - http://127.0.0.1:5000/reset    (Reset counter)")
    print("=" * 60)
    print("⚠️  Start the detection server (app.py) to monitor this server")
    print("=" * 60)
    
    app.run(host='127.0.0.1', port=5000, debug=False)
