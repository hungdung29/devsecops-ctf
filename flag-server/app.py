#!/usr/bin/env python3
"""
Internal Flag Server
This application serves flags for the CTF challenges. It's meant to be accessed internally.
"""

import os
import json
import time
from flask import Flask, jsonify, request, render_template_string
import logging

app = Flask(__name__)
app.secret_key = 'internal_flag_server_secret_2024'

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
        pre { background: #f8f9fa; padding: 10px; border-radius: 3px; overflow-x: auto; }
        .warning { background: #fff3cd; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #ffc107; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏴 Internal Flag Server</h1>
        <div class="warning">
            <strong>⚠️ Internal Use Only</strong><br>
            This server contains sensitive flags and should only be accessible internally.
        </div>
        
        {{ content | safe }}
        
        <div class="info-box">
            <h3>Available Endpoints:</h3>
            <ul>
                <li><a href="/flags">All Flags</a></li>
                <li><a href="/secrets">Secret Files</a></li>
                <li><a href="/admin">Admin Secrets</a></li>
                <li><a href="/health">Health Check</a></li>
                <li><a href="/info">Server Info</a></li>
            </ul>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    content = '''
    <h2>Welcome to the Internal Flag Server</h2>
    <p>This server contains flags for the CTF challenges. It should only be accessible from internal networks.</p>
    
    <div class="info-box">
        <h3>Server Status:</h3>
        <p><strong>Status:</strong> Online</p>
        <p><strong>Purpose:</strong> Internal flag distribution</p>
        <p><strong>Access:</strong> Restricted to internal network</p>
    </div>
    '''
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/flags')
def get_all_flags():
    """Return all flags - this is what SSRF should target"""
    flags = {
        'design_flaw': os.getenv('FLAG_A04', 'CTF{1ns3cur3_d3s1gn_fl4w_2024}'),
        'vulnerable_components': os.getenv('FLAG_A06', 'CTF{vuln3r4bl3_c0mp0n3nts_2024}'),
        'integrity_failure': os.getenv('FLAG_A08', 'CTF{1nt3gr1ty_f41lur3_2024}'),
        'logging_monitoring': os.getenv('FLAG_A09', 'CTF{l0gg1ng_m0n1t0r1ng_2024}'),
        'server_info': {
            'hostname': os.uname().nodename if hasattr(os, 'uname') else 'flag-server',
            'timestamp': int(time.time()),
            'internal_access': True
        }
    }
    
    return jsonify(flags)

@app.route('/flags/web')
def flags_web():
    """Web interface for flags"""
    flags = {
        'design_flaw': os.getenv('FLAG_A04', 'CTF{1ns3cur3_d3s1gn_fl4w_2024}'),
        'vulnerable_components': os.getenv('FLAG_A06', 'CTF{vuln3r4bl3_c0mp0n3nts_2024}'),
        'integrity_failure': os.getenv('FLAG_A08', 'CTF{1nt3gr1ty_f41lur3_2024}'),
        'logging_monitoring': os.getenv('FLAG_A09', 'CTF{l0gg1ng_m0n1t0r1ng_2024}')
    }
    
    content = '''
    <h2>🏆 CTF Flags</h2>
    <p>Internal flags for CTF challenges:</p>
    '''
    
    for flag_name, flag_value in flags.items():
        content += f'''
        <div class="flag-box">
            <strong>{flag_name.replace('_', ' ').title()}:</strong><br>
            <code>{flag_value}</code>
        </div>
        '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

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
            'admin_bypass': 'CTF{4dm1n_byp4ss_m4st3r_2024}',
            'privilege_escalation': 'CTF{pr1v1l3g3_3sc4l4t10n_2024}',
            'internal_access': 'CTF{1nt3rn4l_4cc3ss_gr4nt3d_2024}'
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
        <strong>Admin Bypass Flag:</strong><br>
        <code>CTF{4dm1n_byp4ss_m4st3r_2024}</code>
    </div>
    
    <div class="flag-box">
        <strong>Privilege Escalation Flag:</strong><br>
        <code>CTF{pr1v1l3g3_3sc4l4t10n_2024}</code>
    </div>
    
    <div class="flag-box">
        <strong>Internal Access Flag:</strong><br>
        <code>CTF{1nt3rn4l_4cc3ss_gr4nt3d_2024}</code>
    </div>
    '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    health_data = {
        'status': 'healthy',
        'timestamp': int(time.time()),
        'version': '1.0.0',
        'flags_available': True,
        'secrets_loaded': os.path.exists('/app/secrets'),
        'environment': 'internal'
    }
    
    return jsonify(health_data)

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
    """Configuration information"""
    config = {
        'flag_server_config': {
            'internal_api_enabled': True,
            'authentication_required': False,  # Misconfiguration!
            'cors_enabled': True,
            'debug_mode': True,
            'log_level': 'DEBUG'
        },
        'flags': {
            'total_flags': 4,
            'flag_types': ['design_flaw', 'vulnerable_components', 'integrity_failure', 'logging_monitoring']
        },
        'secrets': {
            'secrets_dir': '/app/secrets',
            'admin_secrets_enabled': True
        }
    }
    
    return jsonify(config)

# Allow CORS for all domains (misconfiguration)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Server', 'Internal-Flag-Server/1.0')
    return response

# Error handler that reveals too much information
@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': str(error),
        'server': 'Internal Flag Server',
        'debug_info': {
            'python_version': os.sys.version,
            'working_directory': os.getcwd(),
            'process_id': os.getpid()
        }
    }), 500

if __name__ == '__main__':
    # Log startup information
    print("🏴 Starting Internal Flag Server...")
    print(f"📍 Working Directory: {os.getcwd()}")
    print(f"🔐 Secrets Directory: {'/app/secrets' if os.path.exists('/app/secrets') else 'Not found'}")
    print("⚠️  WARNING: This server should only be accessible internally!")
    
    app.run(host='0.0.0.0', port=8080, debug=True) 