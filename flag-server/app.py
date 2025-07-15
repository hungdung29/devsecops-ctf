#!/usr/bin/env python3
"""
Internal Flag Server
This application serves flags for the CTF challenges. It's meant to be accessed internally.
HINT: This server is only accessible from the internal network. External access is blocked by firewall.
"""

import os
import json
import time
import socket
import subprocess
from flask import Flask, jsonify, request, render_template_string
import logging

app = Flask(__name__)
app.secret_key = 'internal_flag_server_secret_2025'

# HTML Template for web interface
BASE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Internal Flag Server</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        .flag-box { background: #d4edda; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #28a745; }
        .secret-box { background: #f8d7da; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #dc3545; }
        .info-box { background: #d1ecf1; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #17a2b8; }
        .hint-box { background: #fff3cd; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #ffc107; }
        pre { background: #f8f9fa; padding: 10px; border-radius: 3px; overflow-x: auto; }
        .warning { background: #fff3cd; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #ffc107; }
        .exploit-hint { background: #e2e3e5; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #6c757d; font-family: monospace; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏴 Internal Flag Server</h1>
        <div class="warning">
            <strong>⚠️ Internal Use Only</strong><br>
            This server contains sensitive flags and should only be accessible internally.
            <br><small>Server IP: 192.168.1.100 | Internal Network: 172.20.0.0/16</small>
        </div>
        
        {{ content | safe }}
        
        <div class="info-box">
            <h3>Available Endpoints:</h3>
            <ul>
                <li><a href="/flags">All Flags</a> - Main flag endpoint</li>
                <li><a href="/secrets">Secret Files</a> - Docker secrets</li>
                <li><a href="/admin">Admin Secrets</a> - Administrative data</li>
                <li><a href="/health">Health Check</a> - Service status</li>
                <li><a href="/info">Server Info</a> - System information</li>
                <li><a href="/config">Configuration</a> - Server config</li>
                <li><a href="/network">Network Info</a> - Network topology</li>
                <li><a href="/internal">Internal Services</a> - Service discovery</li>
                <li><a href="/debug">Debug Info</a> - Debugging endpoint</li>
                <li><a href="/metrics">Metrics</a> - Performance metrics</li>
            </ul>
        </div>
        
        <div class="hint-box">
            <strong>💡 SSRF Testing Hint:</strong><br>
            This server is designed to be accessed internally. Try accessing it from other services in the network!
            <br><small>Example: http://flag-server:8080/flags</small>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
    
    content = f'''
    <h2>Welcome to the Internal Flag Server</h2>
    <p>This server contains flags for the CTF challenges. It should only be accessible from internal networks.</p>
    
    <div class="info-box">
        <h3>Server Status:</h3>
        <p><strong>Status:</strong> Online and Ready</p>
        <p><strong>Purpose:</strong> Internal flag distribution</p>
        <p><strong>Access:</strong> Restricted to internal network (172.20.0.0/16)</p>
        <p><strong>Client IP:</strong> {client_ip}</p>
        <p><strong>Hostname:</strong> flag-server</p>
    </div>
    
    <div class="exploit-hint">
        <strong>🎯 Exploitation Hint:</strong><br>
        This service is behind a firewall and only accessible internally.<br>
        You might need to find a way to make requests from inside the network...<br>
        <code>curl http://flag-server:8080/flags</code>
    </div>
    '''
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/flags')
def get_all_flags():
    """Return all flags - this is what SSRF should target"""
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
    
    flags = {
        'success': True,
        'message': 'Flags retrieved successfully from internal server',
        'client_ip': client_ip,
        'server_hostname': socket.gethostname(),
        'flags': {
            'ssrf_flag': os.getenv('FLAG_SSRF', 'CTF{ssrf_1nt3rn4l_4cc3ss_2025}'),
        },
        'server_info': {
            'hostname': socket.gethostname(),
            'timestamp': int(time.time()),
            'internal_access': True,
            'network': '172.20.0.0/16'
        },
        'hint': 'Congratulations! You successfully performed SSRF to access internal services!'
    }
    
    return jsonify(flags)

@app.route('/flags/web')
def flags_web():
    """Web interface for flags"""
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
    
    flags = {
        'ssrf_flag': os.getenv('FLAG_SSRF', 'CTF{ssrf_1nt3rn4l_4cc3ss_2025}'),
    }
    
    content = f'''
    <h2>🏆 CTF Flags</h2>
    <p>Internal flags for CTF challenges (accessed from {client_ip}):</p>
    
    <div class="flag-box">
        <strong>🎯 SSRF Success!</strong><br>
        You successfully accessed the internal flag server!
    </div>
    '''
    
    for flag_name, flag_value in flags.items():
        content += f'''
        <div class="flag-box">
            <strong>{flag_name.replace('_', ' ').title()}:</strong><br>
            <code>{flag_value}</code>
        </div>
        '''
    
    content += '''
    <div class="hint-box">
        <strong>💡 Exploitation Note:</strong><br>
        This endpoint proves you can access internal services via SSRF!
    </div>
    '''
    
    return render_template_string(BASE_TEMPLATE, content=content)


@app.route('/debug')
def debug_info():
    """Debug endpoint with verbose information"""
    debug_data = {
        'request_info': {
            'method': request.method,
            'path': request.path,
            'headers': dict(request.headers),
            'remote_addr': request.remote_addr,
            'forwarded_for': request.environ.get('HTTP_X_FORWARDED_FOR'),
            'user_agent': request.headers.get('User-Agent')
        },
        'server_debug': {
            'hostname': socket.gethostname(),
            'cwd': os.getcwd(),
            'pid': os.getpid(),
            'environment': dict(os.environ),
            'python_path': os.sys.path
        },
        'exploitation_notes': {
            'ssrf_target': 'http://flag-server:8080/flags',
            'internal_hostname': 'flag-server',
            'internal_port': 8080,
            'hint': 'This debug info helps you understand the internal network structure'
        }
    }
    
    return jsonify(debug_data)


@app.route('/health')
def health_check():
    """Enhanced health check endpoint"""
    health_data = {
        'status': 'healthy',
        'timestamp': int(time.time()),
        'version': '1.0.0',
        'flags_available': True,
        'secrets_loaded': os.path.exists('/app/secrets'),
        'environment': 'internal',
        'network': {
            'hostname': socket.gethostname(),
            'internal_ip': '172.20.0.100',
            'accessible_from': 'internal network only'
        },
        'services': {
            'flag_server': 'running',
            'admin_panel': 'running',
            'secret_manager': 'running'
        },
        'ssrf_hint': 'Health check confirms internal services are accessible at http://flag-server:8080'
    }
    
    return jsonify(health_data)

@app.route('/secrets')
def get_secrets():
    """Read secret files created by Docker"""
    secrets = {}
    secrets_dir = '/app/secrets'
    
    try:
        if os.path.exists(secrets_dir):
            for filename in os.listdir(secrets_dir):
                file_path = os.path.join(secrets_dir, filename)
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r') as f:
                            secrets[filename] = f.read().strip()
                    except Exception as e:
                        secrets[filename] = f"Error reading file: {str(e)}"
        else:
            secrets['error'] = 'Secrets directory not found'
            
    except Exception as e:
        secrets['error'] = str(e)
    
    return jsonify(secrets)

@app.route('/secrets/web')
def secrets_web():
    """Web interface for secrets"""
    secrets = {}
    secrets_dir = '/app/secrets'
    
    try:
        if os.path.exists(secrets_dir):
            for filename in os.listdir(secrets_dir):
                file_path = os.path.join(secrets_dir, filename)
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r') as f:
                            secrets[filename] = f.read().strip()
                    except Exception as e:
                        secrets[filename] = f"Error reading file: {str(e)}"
    except Exception as e:
        secrets['error'] = str(e)
    
    content = '<h2>🔐 Secret Files</h2>'
    
    if secrets:
        for filename, content_data in secrets.items():
            if filename.endswith('.txt'):
                if 'flag' in filename.lower():
                    content += f'''
                    <div class="flag-box">
                        <strong>{filename}:</strong><br>
                        <code>{content_data}</code>
                    </div>
                    '''
                else:
                    content += f'''
                    <div class="secret-box">
                        <strong>{filename}:</strong><br>
                        <code>{content_data}</code>
                    </div>
                    '''
    else:
        content += '<p>No secret files found.</p>'
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/admin')
def admin_secrets():
    """Admin-only secrets - requires authentication in a real scenario"""
    admin_data = {
        'master_password': 'SuperSecretPassword123!',
        'database_root': 'root:VerySecureRootPassword456!',
        'api_master_key': 'mk-1234567890abcdef-master-key',
        'encryption_master_key': 'emk-9876543210fedcba-encryption',
        'backup_encryption_key': 'bek-abcdef1234567890-backup',
        'internal_service_token': 'ist-deadbeef-internal-service-token',
        'admin_flags': {
            'privilege_escalation': 'CTF{pr1v1l3g3_3sc4l4t10n_2025}'
        }
    }
    
    return jsonify(admin_data)

@app.route('/admin/web')
def admin_web():
    """Web interface for admin secrets"""
    content = '''
    <h2>⚙️ Admin Secrets</h2>
    <div class="secret-box">
        <strong>Master Password:</strong><br>
        <code>SuperSecretPassword123!</code>
    </div>
    
    <div class="secret-box">
        <strong>Database Root:</strong><br>
        <code>root:VerySecureRootPassword456!</code>
    </div>
    
    <div class="secret-box">
        <strong>API Master Key:</strong><br>
        <code>mk-1234567890abcdef-master-key</code>
    </div>
    
    <div class="flag-box">
        <strong>Privilege Escalation Flag:</strong><br>
        <code>CTF{pr1v1l3g3_3sc4l4t10n_2025}</code>
    </div>
    '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/info')
def server_info():
    """Server information"""
    import sys
    import platform
    
    server_info = {
        'server': 'Internal Flag Server',
        'version': '1.0.0',
        'python_version': sys.version,
        'platform': platform.platform(),
        'hostname': os.uname().nodename if hasattr(os, 'uname') else 'flag-server',
        'process_id': os.getpid(),
        'working_directory': os.getcwd(),
        'environment_variables': dict(os.environ),
        'timestamp': int(time.time())
    }
    
    return jsonify(server_info)

@app.route('/info/web')
def info_web():
    """Web interface for server info"""
    import sys
    import platform
    
    content = f'''
    <h2>📊 Server Information</h2>
    <div class="info-box">
        <strong>Server:</strong> Internal Flag Server v1.0.0<br>
        <strong>Python:</strong> {sys.version}<br>
        <strong>Platform:</strong> {platform.platform()}<br>
        <strong>Hostname:</strong> {os.uname().nodename if hasattr(os, 'uname') else 'flag-server'}<br>
        <strong>Process ID:</strong> {os.getpid()}<br>
        <strong>Working Directory:</strong> {os.getcwd()}
    </div>
    
    <div class="info-box">
        <h4>Environment Variables:</h4>
        <pre>{json.dumps(dict(os.environ), indent=2)}</pre>
    </div>
    '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/config')
def get_config():
    """Enhanced configuration information"""
    config = {
        'flag_server_config': {
            'internal_api_enabled': True,
            'authentication_required': False, 
            'cors_enabled': True,
            'debug_mode': True,
            'log_level': 'DEBUG',
            'firewall_bypass': 'Use SSRF from internal services',
            'internal_hostname': 'flag-server',
            'internal_port': 8080
        },
        'secrets': {
            'secrets_dir': '/app/secrets',
            'admin_secrets_enabled': True
        },
        'network_config': {
            'internal_network': '172.20.0.0/16',
            'external_access': 'blocked_by_firewall',
            'ssrf_vulnerable_services': ['app4-ssrf']
        },
        'exploitation_guide': {
            'step1': 'Find SSRF vulnerability in external service',
            'step2': 'Target http://flag-server:8080/flags',
            'step3': 'Retrieve internal flags',
            'example_payload': 'http://flag-server:8080/flags'
        }
    }
    
    return jsonify(config)

# Allow CORS for all domains
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Server', 'Internal-Flag-Server/1.0')
    return response

# Enhanced error handler that reveals even more information
@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': str(error),
        'server': 'Internal Flag Server',
        'debug_info': {
            'python_version': os.sys.version,
            'working_directory': os.getcwd(),
            'process_id': os.getpid(),
            'hostname': socket.gethostname(),
            'internal_ip': '172.20.0.100'
        },
        'exploitation_hint': 'Server errors reveal internal information - useful for SSRF attacks!',
        'ssrf_target': 'http://flag-server:8080/flags'
    }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested endpoint was not found',
        'available_endpoints': [
            '/flags - Main flag endpoint (SSRF target)',
            '/admin - Admin secrets',
            '/secrets - Secret files',
            '/network - Network information',
            '/internal - Service discovery',
            '/debug - Debug information'
        ],
        'ssrf_hint': 'Try accessing http://flag-server:8080/flags from an internal service',
        'server': 'flag-server (internal)'
    }), 404

if __name__ == '__main__':
    # Enhanced startup information
    print("🏴 Starting Internal Flag Server...")
    print(f"📍 Working Directory: {os.getcwd()}")
    print(f"🔐 Secrets Directory: {'/app/secrets' if os.path.exists('/app/secrets') else 'Not found'}")
    print(f"🌐 Hostname: {socket.gethostname()}")
    print(f"🔗 Internal URL: http://flag-server:8080")
    print("⚠️  WARNING: This server should only be accessible internally!")
    print("💡 SSRF Hint: Target this server from other internal services")
    print("🎯 Primary flag endpoint: /flags")
    
    app.run(host='0.0.0.0', port=8080, debug=True) 