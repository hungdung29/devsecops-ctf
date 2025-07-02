#!/usr/bin/env python3
"""
OWASP Top 10 - A10: Server-Side Request Forgery (SSRF) & A05: Security Misconfiguration
This application demonstrates SSRF and security misconfiguration vulnerabilities for educational purposes.
"""

import os
import requests
import subprocess
import urllib.parse
from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import logging
import socket
import json
import time

app = Flask(__name__)
app.secret_key = 'ssrf_vulnerable_secret_2024'

# Configure Flask to show debug information (intentionally insecure)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'

# Weak configuration
INTERNAL_API_KEY = os.getenv('INTERNAL_API_KEY', 'internal_secret_api_key_789')

# HTML Template
BASE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>SSRF & Security Misconfiguration - OWASP A10/A05</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        .challenge { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        .warning { background: #fff3cd; border-color: #ffc107; color: #856404; }
        .success { background: #d4edda; border-color: #28a745; color: #155724; }
        .error { background: #f8d7da; border-color: #dc3545; color: #721c24; }
        input, textarea { width: 400px; padding: 8px; margin: 5px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin: 10px 0; padding: 10px; background: #f8f9fa; border-left: 3px solid #007bff; }
        .flag { background: #d4edda; border-left-color: #28a745; color: #155724; font-weight: bold; }
        pre { background: #f8f9fa; padding: 10px; border-radius: 3px; overflow-x: auto; }
        .config-box { background: #e9ecef; padding: 15px; border-radius: 5px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 SSRF & Security Misconfiguration Challenge</h1>
        <div class="challenge warning">
            <h3>⚠️ Educational Purpose Only</h3>
            <p>This application contains intentional SSRF and misconfiguration vulnerabilities. Exploit them to capture flags!</p>
        </div>
        
        {{ content | safe }}
        
        <div style="margin-top: 30px; padding: 15px; background: #e9ecef; border-radius: 5px;">
            <h3>🎯 Available Challenges:</h3>
            <ul>
                <li><a href="./">Home</a></li>
                <li><a href="./fetch">URL Fetcher (SSRF)</a></li>
                <li><a href="./proxy">Web Proxy (SSRF)</a></li>
                <li><a href="./webhook">Webhook Tester</a></li>
                <li><a href="./admin">Admin Panel</a></li>
                <li><a href="./config">Configuration Info</a></li>
                <li><a href="./debug">Debug Information</a></li>
                <li><a href="./internal">Internal API</a></li>
            </ul>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    content = '''
    <h2>Welcome to the SSRF & Security Misconfiguration Lab</h2>
    <p>This application demonstrates SSRF and security misconfiguration vulnerabilities from OWASP A10 and A05.</p>
    
    <div class="challenge">
        <h3>Your Mission:</h3>
        <ul>
            <li>Exploit Server-Side Request Forgery (SSRF) vulnerabilities</li>
            <li>Access internal services and resources</li>
            <li>Find security misconfigurations</li>
            <li>Discover exposed sensitive information</li>
            <li>Capture flags in the format: <code>CTF{...}</code></li>
        </ul>
    </div>
    
    <div class="challenge">
        <h3>Common SSRF Targets:</h3>
        <ul>
            <li><code>http://localhost/</code> - Local services</li>
            <li><code>http://127.0.0.1/</code> - Loopback interface</li>
            <li><code>http://flag-server:8080/</code> - Internal flag server</li>
            <li><code>http://[::1]/</code> - IPv6 localhost</li>
            <li><code>file:///etc/passwd</code> - Local files</li>
        </ul>
    </div>
    '''
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/fetch', methods=['GET', 'POST'])
def fetch_url():
    if request.method == 'POST':
        url = request.form.get('url', '')
        
        if not url:
            result = '<div class="result error"><p>Please provide a URL!</p></div>'
        else:
            try:
                # VULNERABLE: No URL validation - allows SSRF
                response = requests.get(url, timeout=10, allow_redirects=True)
                
                result = f'''
                <div class="result">
                    <h4>Response from: {url}</h4>
                    <p><strong>Status Code:</strong> {response.status_code}</p>
                    <p><strong>Headers:</strong></p>
                    <pre>{json.dumps(dict(response.headers), indent=2)}</pre>
                    <p><strong>Content:</strong></p>
                    <pre>{response.text[:2000]}{'...' if len(response.text) > 2000 else ''}</pre>
                </div>
                '''
                
                # Check if flag server was accessed
                if 'flag-server' in url or '8080' in url:
                    flag = os.getenv('FLAG_A10', 'CTF{ssrf_4nd_m1sc0nf1g_2024}')
                    result += f'''
                    <div class="result flag">
                        <h3>🎉 Flag Captured!</h3>
                        <p>You successfully performed SSRF to access internal services!</p>
                        <p><strong>FLAG:</strong> {flag}</p>
                    </div>
                    '''
                    
            except Exception as e:
                result = f'<div class="result error"><p>Error fetching URL: {str(e)}</p></div>'
        
        content = f'''
        <h2>🌐 URL Fetcher (SSRF Challenge)</h2>
        <form method="POST">
            <label>Enter URL to fetch:</label><br>
            <input type="text" name="url" value="{url}" placeholder="https://example.com" required><br>
            <button type="submit">Fetch URL</button>
        </form>
        {result}
        
        <div class="challenge">
            <h4>💡 SSRF Challenge:</h4>
            <p>Try accessing internal services:</p>
            <ul>
                <li><code>http://flag-server:8080/flags</code></li>
                <li><code>http://localhost:5005/internal</code></li>
                <li><code>http://127.0.0.1:5005/config</code></li>
            </ul>
        </div>
        '''
    else:
        content = '''
        <h2>🌐 URL Fetcher (SSRF Challenge)</h2>
        <form method="POST">
            <label>Enter URL to fetch:</label><br>
            <input type="text" name="url" placeholder="https://example.com" required><br>
            <button type="submit">Fetch URL</button>
        </form>
        
        <div class="challenge">
            <h4>💡 SSRF Challenge:</h4>
            <p>Try accessing internal services:</p>
            <ul>
                <li><code>http://flag-server:8080/flags</code></li>
                <li><code>http://localhost:5005/internal</code></li>
                <li><code>http://127.0.0.1:5005/config</code></li>
            </ul>
        </div>
        '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/proxy', methods=['GET', 'POST'])
def web_proxy():
    if request.method == 'POST':
        target_url = request.form.get('target_url', '')
        user_agent = request.form.get('user_agent', 'SSRF-Proxy/1.0')
        
        if not target_url:
            result = '<div class="result error"><p>Please provide a target URL!</p></div>'
        else:
            try:
                # VULNERABLE: Acts as an open proxy - SSRF vulnerability
                headers = {
                    'User-Agent': user_agent,
                    'X-Forwarded-For': request.environ.get('REMOTE_ADDR', '127.0.0.1'),
                    'X-Real-IP': request.environ.get('REMOTE_ADDR', '127.0.0.1')
                }
                
                response = requests.get(target_url, headers=headers, timeout=15)
                
                result = f'''
                <div class="result">
                    <h4>Proxied Response from: {target_url}</h4>
                    <p><strong>Status:</strong> {response.status_code}</p>
                    <p><strong>Content-Type:</strong> {response.headers.get('Content-Type', 'Unknown')}</p>
                    <div style="max-height: 400px; overflow-y: auto; border: 1px solid #ccc; padding: 10px;">
                        <pre>{response.text}</pre>
                    </div>
                </div>
                '''
                
            except Exception as e:
                result = f'<div class="result error"><p>Proxy error: {str(e)}</p></div>'
        
        content = f'''
        <h2>🔄 Web Proxy (SSRF Challenge)</h2>
        <form method="POST">
            <label>Target URL:</label><br>
            <input type="text" name="target_url" value="{target_url}" placeholder="http://internal-service/" required><br>
            <label>User-Agent:</label><br>
            <input type="text" name="user_agent" value="{user_agent}"><br>
            <button type="submit">Proxy Request</button>
        </form>
        {result}
        
        <div class="challenge">
            <h4>💡 Proxy SSRF:</h4>
            <p>This proxy can access internal networks!</p>
        </div>
        '''
    else:
        content = '''
        <h2>🔄 Web Proxy (SSRF Challenge)</h2>
        <form method="POST">
            <label>Target URL:</label><br>
            <input type="text" name="target_url" placeholder="http://internal-service/" required><br>
            <label>User-Agent:</label><br>
            <input type="text" name="user_agent" value="SSRF-Proxy/1.0"><br>
            <button type="submit">Proxy Request</button>
        </form>
        
        <div class="challenge">
            <h4>💡 Proxy SSRF:</h4>
            <p>This proxy can access internal networks!</p>
        </div>
        '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook_tester():
    if request.method == 'POST':
        webhook_url = request.form.get('webhook_url', '')
        payload = request.form.get('payload', '{"test": "data"}')
        
        if not webhook_url:
            result = '<div class="result error"><p>Please provide a webhook URL!</p></div>'
        else:
            try:
                # VULNERABLE: No URL validation for webhooks
                response = requests.post(webhook_url, 
                                       json=json.loads(payload), 
                                       timeout=10,
                                       headers={'Content-Type': 'application/json'})
                
                result = f'''
                <div class="result">
                    <h4>Webhook Response from: {webhook_url}</h4>
                    <p><strong>Status:</strong> {response.status_code}</p>
                    <p><strong>Response:</strong></p>
                    <pre>{response.text[:1000]}{'...' if len(response.text) > 1000 else ''}</pre>
                </div>
                '''
                
            except json.JSONDecodeError:
                result = '<div class="result error"><p>Invalid JSON payload!</p></div>'
            except Exception as e:
                result = f'<div class="result error"><p>Webhook error: {str(e)}</p></div>'
        
        content = f'''
        <h2>🪝 Webhook Tester (SSRF Challenge)</h2>
        <form method="POST">
            <label>Webhook URL:</label><br>
            <input type="text" name="webhook_url" value="{webhook_url}" placeholder="http://example.com/webhook" required><br>
            <label>JSON Payload:</label><br>
            <textarea name="payload" rows="4">{payload}</textarea><br>
            <button type="submit">Send Webhook</button>
        </form>
        {result}
        '''
    else:
        content = '''
        <h2>🪝 Webhook Tester (SSRF Challenge)</h2>
        <form method="POST">
            <label>Webhook URL:</label><br>
            <input type="text" name="webhook_url" placeholder="http://example.com/webhook" required><br>
            <label>JSON Payload:</label><br>
            <textarea name="payload" rows="4">{"test": "data"}</textarea><br>
            <button type="submit">Send Webhook</button>
        </form>
        '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/config')
def config_info():
    # VULNERABLE: Exposes sensitive configuration information
    config_data = {
        'DEBUG': app.config.get('DEBUG'),
        'ENV': app.config.get('ENV'),
        'SECRET_KEY': app.secret_key,
        'INTERNAL_API_KEY': INTERNAL_API_KEY,
        'DATABASE_URL': 'postgresql://admin:supersecret@postgres:5432/internal_db',
        'REDIS_URL': 'redis://redis:6379/0',
        'FLAG_A05': os.getenv('FLAG_A05', 'CTF{s3cur1ty_m1sc0nf1g_2024}')
    }
    
    content = f'''
    <h2>⚙️ Configuration Information</h2>
    <div class="config-box">
        <h4>Application Configuration:</h4>
        <pre>{json.dumps(config_data, indent=2)}</pre>
    </div>
    
    <div class="result flag">
        <h3>🎉 Security Misconfiguration Found!</h3>
        <p>Sensitive configuration exposed!</p>
        <p><strong>FLAG:</strong> {config_data['FLAG_A05']}</p>
    </div>
    
    <div class="challenge">
        <h4>💡 Security Misconfiguration:</h4>
        <p>This endpoint exposes sensitive information that should never be public:</p>
        <ul>
            <li>Secret keys and API keys</li>
            <li>Database credentials</li>
            <li>Internal service URLs</li>
            <li>Debug information</li>
        </ul>
    </div>
    '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/debug')
def debug_info():
    # VULNERABLE: Debug information exposure
    import sys
    import platform
    
    debug_data = {
        'python_version': sys.version,
        'platform': platform.platform(),
        'environment_variables': dict(os.environ),
        'current_working_directory': os.getcwd(),
        'process_id': os.getpid(),
        'user_id': os.getuid() if hasattr(os, 'getuid') else 'N/A'
    }
    
    content = f'''
    <h2>🐛 Debug Information</h2>
    <div class="config-box">
        <h4>System Information:</h4>
        <p><strong>Python:</strong> {debug_data['python_version']}</p>
        <p><strong>Platform:</strong> {debug_data['platform']}</p>
        <p><strong>Working Directory:</strong> {debug_data['current_working_directory']}</p>
        <p><strong>Process ID:</strong> {debug_data['process_id']}</p>
        <p><strong>User ID:</strong> {debug_data['user_id']}</p>
    </div>
    
    <div class="config-box">
        <h4>Environment Variables:</h4>
        <pre style="max-height: 300px; overflow-y: auto;">{json.dumps(debug_data['environment_variables'], indent=2)}</pre>
    </div>
    
    <div class="challenge">
        <h4>💡 Information Disclosure:</h4>
        <p>Debug endpoints can reveal sensitive system information!</p>
    </div>
    '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/internal')
def internal_api():
    # VULNERABLE: Internal API accessible externally
    api_key = request.headers.get('X-API-Key')
    
    if api_key != INTERNAL_API_KEY:
        return jsonify({
            'error': 'Invalid API key',
            'hint': 'Try checking the /config endpoint for the API key'
        }), 401
    
    # Read configuration files
    config_files = {}
    config_dir = '/app/config'
    
    try:
        for filename in os.listdir(config_dir):
            file_path = os.path.join(config_dir, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as f:
                    config_files[filename] = f.read().strip()
    except Exception as e:
        config_files['error'] = str(e)
    
    return jsonify({
        'message': 'Internal API access granted',
        'config_files': config_files,
        'flag': 'CTF{1nt3rn4l_4p1_4cc3ss_2024}'
    })

@app.route('/admin')
def admin_panel():
    # VULNERABLE: No authentication
    content = '''
    <h2>⚙️ Admin Panel</h2>
    <div class="result flag">
        <h3>🎉 Admin Access Granted!</h3>
        <p>No authentication required - Security Misconfiguration!</p>
        <p><strong>FLAG:</strong> CTF{4dm1n_n0_4uth_2024}</p>
    </div>
    
    <div class="challenge">
        <h3>Admin Functions:</h3>
        <ul>
                            <li><a href="./admin/users">User Management</a></li>
                <li><a href="./admin/logs">System Logs</a></li>
                <li><a href="./admin/config">Configuration</a></li>
                <li><a href="./admin/backup">Database Backup</a></li>
        </ul>
    </div>
    '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/admin/logs')
def admin_logs():
    # VULNERABLE: Exposes system logs
    try:
        # Simulate reading log files
        logs = [
            "2024-01-15 10:30:15 - INFO - User admin logged in from 192.168.1.100",
            "2024-01-15 10:35:22 - ERROR - Failed login attempt for user 'admin' from 10.0.0.5",
            "2024-01-15 10:40:11 - INFO - Database backup completed",
            "2024-01-15 10:45:33 - WARNING - Suspicious request to /admin from 172.16.0.10",
            "2024-01-15 10:50:44 - INFO - Flag server accessed internally",
            f"2024-01-15 10:55:15 - DEBUG - Internal API key: {INTERNAL_API_KEY}"
        ]
        
        content = f'''
        <h2>📊 System Logs</h2>
        <div class="config-box">
            <pre>{'<br>'.join(logs)}</pre>
        </div>
        
        <div class="challenge">
            <h4>💡 Information Disclosure:</h4>
            <p>Logs contain sensitive information including API keys!</p>
        </div>
        '''
        
    except Exception as e:
        content = f'<div class="result error"><p>Error reading logs: {str(e)}</p></div>'
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.errorhandler(404)
def not_found(error):
    # VULNERABLE: Verbose error messages
    content = f'''
    <h2>🚫 404 - Page Not Found</h2>
    <div class="result error">
        <p><strong>Error:</strong> The requested URL was not found on this server.</p>
        <p><strong>Requested URL:</strong> {request.url}</p>
        <p><strong>Method:</strong> {request.method}</p>
        <p><strong>User Agent:</strong> {request.headers.get('User-Agent', 'Unknown')}</p>
        <p><strong>Remote Address:</strong> {request.environ.get('REMOTE_ADDR', 'Unknown')}</p>
    </div>
    
    <div class="challenge">
        <h4>💡 Information Disclosure:</h4>
        <p>Verbose error messages can reveal system information!</p>
    </div>
    '''
    
    return render_template_string(BASE_TEMPLATE, content=content), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True) 