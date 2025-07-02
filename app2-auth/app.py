#!/usr/bin/env python3
"""
OWASP Top 10 - A07: Identification and Authentication Failures
This application demonstrates various authentication vulnerabilities for educational purposes.
"""

import os
import jwt
import bcrypt
import redis
import hashlib
import time
import uuid
from datetime import datetime, timedelta
from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for, make_response
import logging

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'weak_secret_key_123')  # Intentionally weak

# Redis configuration for session storage
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=6379,
    decode_responses=True
)

# Weak JWT secret
JWT_SECRET = 'super_weak_jwt_secret_2024'

# In-memory user storage (vulnerable to enumeration)
USERS = {
    'admin': {
        'password': 'admin',  # Weak password
        'role': 'admin',
        'email': 'admin@vulnerable.com',
        'failed_attempts': 0,
        'locked_until': None
    },
    'user1': {
        'password': 'password',  # Common password
        'role': 'user',
        'email': 'user1@test.com',
        'failed_attempts': 0,
        'locked_until': None
    },
    'john': {
        'password': '123456',  # Very weak password
        'role': 'user',
        'email': 'john@example.com',
        'failed_attempts': 0,
        'locked_until': None
    },
    'alice': {
        'password': 'alice123',  # Predictable password
        'role': 'manager',
        'email': 'alice@company.com',
        'failed_attempts': 0,
        'locked_until': None
    }
}

# HTML Template
BASE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Authentication Challenges - OWASP A07</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        .challenge { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        .warning { background: #fff3cd; border-color: #ffc107; color: #856404; }
        .success { background: #d4edda; border-color: #28a745; color: #155724; }
        .error { background: #f8d7da; border-color: #dc3545; color: #721c24; }
        input { width: 300px; padding: 8px; margin: 5px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin: 10px 0; padding: 10px; background: #f8f9fa; border-left: 3px solid #007bff; }
        .flag { background: #d4edda; border-left-color: #28a745; color: #155724; font-weight: bold; }
        pre { background: #f8f9fa; padding: 10px; border-radius: 3px; overflow-x: auto; }
        .session-info { background: #e9ecef; padding: 10px; border-radius: 3px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 Authentication Failures Challenge</h1>
        <div class="challenge warning">
            <h3>⚠️ Educational Purpose Only</h3>
            <p>This application contains intentional authentication vulnerabilities. Exploit them to capture flags!</p>
        </div>
        
        {{ content | safe }}
        
        <div style="margin-top: 30px; padding: 15px; background: #e9ecef; border-radius: 5px;">
            <h3>🎯 Available Challenges:</h3>
            <ul>
                <li><a href="./">Home</a></li>
                <li><a href="./login">Weak Authentication</a></li>
                <li><a href="./bruteforce">Brute Force Protection Bypass</a></li>
                <li><a href="./session">Session Management Issues</a></li>
                <li><a href="./jwt">JWT Vulnerabilities</a></li>
                <li><a href="./reset">Password Reset Flaws</a></li>
                <li><a href="./admin">Admin Panel</a></li>
            </ul>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    content = '''
    <h2>Welcome to the Authentication Security Lab</h2>
    <p>This application demonstrates common authentication vulnerabilities from OWASP A07.</p>
    
    <div class="challenge">
        <h3>Your Mission:</h3>
        <ul>
            <li>Bypass weak authentication mechanisms</li>
            <li>Exploit session management flaws</li>
            <li>Break JWT implementations</li>
            <li>Find password reset vulnerabilities</li>
            <li>Capture flags in the format: <code>CTF{...}</code></li>
        </ul>
    </div>
    
    <div class="challenge">
        <h3>Common Weak Passwords to Try:</h3>
        <ul>
            <li><code>admin / admin</code></li>
            <li><code>user1 / password</code></li>
            <li><code>john / 123456</code></li>
            <li><code>alice / alice123</code></li>
        </ul>
    </div>
    '''
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # Check if user exists (vulnerable to user enumeration)
        if username not in USERS:
            content = '''
            <div class="result error">
                <p>User does not exist!</p>
            </div>
            '''
        else:
            user = USERS[username]
            
            # Check if account is locked (weak lockout mechanism)
            if user['locked_until'] and datetime.now() < user['locked_until']:
                content = '''
                <div class="result error">
                    <p>Account temporarily locked. Try again later.</p>
                </div>
                '''
            elif user['password'] == password:  # Plain text password comparison
                user['failed_attempts'] = 0
                user['locked_until'] = None
                
                # Create vulnerable session
                session['username'] = username
                session['role'] = user['role']
                session['authenticated'] = True
                
                # Store session in Redis with predictable key
                session_id = hashlib.md5(f"{username}_{time.time()}".encode()).hexdigest()
                redis_client.setex(f"session_{username}", 3600, session_id)
                
                if user['role'] == 'admin':
                    flag = os.getenv('FLAG_A07', 'CTF{4uth_byp4ss_h4ck3r_2024}')
                    content = f'''
                    <div class="result flag">
                        <h2>🎉 Admin Login Successful!</h2>
                        <p>Welcome, {username}!</p>
                        <p><strong>FLAG CAPTURED:</strong> {flag}</p>
                        <p>Session ID: {session_id}</p>
                    </div>
                    '''
                else:
                    content = f'''
                    <div class="result success">
                        <h2>Login Successful</h2>
                        <p>Welcome, {username} ({user['role']})!</p>
                        <p>Session ID: {session_id}</p>
                    </div>
                    '''
            else:
                # Increment failed attempts (weak protection)
                user['failed_attempts'] += 1
                if user['failed_attempts'] >= 3:  # Very permissive limit
                    user['locked_until'] = datetime.now() + timedelta(minutes=1)  # Short lockout
                
                content = f'''
                <div class="result error">
                    <p>Invalid password! Attempts: {user['failed_attempts']}/3</p>
                </div>
                '''
        
        content += '''
        <h2>🔐 Login System</h2>
        <form method="POST">
            <label>Username:</label><br>
            <input type="text" name="username" required><br>
            <label>Password:</label><br>
            <input type="password" name="password" required><br><br>
            <button type="submit">Login</button>
        </form>
        
        <div class="challenge">
            <h4>💡 Vulnerabilities:</h4>
            <ul>
                <li>User enumeration through different error messages</li>
                <li>Weak password policy</li>
                <li>Plain text password storage</li>
                <li>Weak account lockout mechanism</li>
                <li>Predictable session IDs</li>
            </ul>
        </div>
        '''
    else:
        content = '''
        <h2>🔐 Login System</h2>
        <form method="POST">
            <label>Username:</label><br>
            <input type="text" name="username" required><br>
            <label>Password:</label><br>
            <input type="password" name="password" required><br><br>
            <button type="submit">Login</button>
        </form>
        
        <div class="challenge">
            <h4>💡 Vulnerabilities:</h4>
            <ul>
                <li>User enumeration through different error messages</li>
                <li>Weak password policy</li>
                <li>Plain text password storage</li>
                <li>Weak account lockout mechanism</li>
                <li>Predictable session IDs</li>
            </ul>
        </div>
        '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/bruteforce', methods=['GET', 'POST'])
def bruteforce():
    if request.method == 'POST':
        username = request.form.get('username', '')
        
        # Vulnerable: No rate limiting, easily bypassable
        if username in USERS:
            user = USERS[username]
            attempts_info = f"Failed attempts: {user['failed_attempts']}"
            lockout_info = ""
            
            if user['locked_until']:
                lockout_info = f"Locked until: {user['locked_until']}"
            
            content = f'''
            <div class="result">
                <h3>User Information:</h3>
                <p>Username: {username}</p>
                <p>Email: {user['email']}</p>
                <p>Role: {user['role']}</p>
                <p>{attempts_info}</p>
                <p>{lockout_info}</p>
            </div>
            '''
        else:
            content = '''
            <div class="result error">
                <p>User not found</p>
            </div>
            '''
        
        content += '''
        <h2>🔓 Brute Force Testing</h2>
        <form method="POST">
            <label>Username to check:</label><br>
            <input type="text" name="username" required><br><br>
            <button type="submit">Check Status</button>
        </form>
        
        <div class="challenge">
            <h4>💡 Hints:</h4>
            <ul>
                <li>No CAPTCHA protection</li>
                <li>No rate limiting</li>
                <li>Account lockout can be reset by checking user status</li>
                <li>Try common usernames: admin, user1, john, alice</li>
            </ul>
        </div>
        '''
    else:
        content = '''
        <h2>🔓 Brute Force Testing</h2>
        <form method="POST">
            <label>Username to check:</label><br>
            <input type="text" name="username" required><br><br>
            <button type="submit">Check Status</button>
        </form>
        
        <div class="challenge">
            <h4>💡 Hints:</h4>
            <ul>
                <li>No CAPTCHA protection</li>
                <li>No rate limiting</li>
                <li>Account lockout can be reset by checking user status</li>
                <li>Try common usernames: admin, user1, john, alice</li>
            </ul>
        </div>
        '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/session')
def session_info():
    content = '''
    <h2>🗂️ Session Management</h2>
    
    <div class="session-info">
        <h3>Current Session:</h3>
        <pre>'''
    
    # Display session information (vulnerable)
    for key, value in session.items():
        content += f"{key}: {value}\\n"
    
    content += '''</pre>
    </div>
    
    <div class="session-info">
        <h3>Session Vulnerabilities:</h3>
        <ul>
            <li>Session data exposed to client</li>
            <li>Predictable session IDs</li>
            <li>No session rotation after login</li>
            <li>Sessions stored with weak encryption</li>
        </ul>
    </div>
    
    <div class="challenge">
        <h4>💡 Try These:</h4>
        <ul>
            <li>Modify session data in browser dev tools</li>
            <li>Predict other users' session IDs</li>
            <li>Session fixation attacks</li>
        </ul>
    </div>
    '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/jwt', methods=['GET', 'POST'])
def jwt_demo():
    if request.method == 'POST':
        username = request.form.get('username', 'guest')
        
        # Create vulnerable JWT
        payload = {
            'username': username,
            'role': 'user',
            'exp': datetime.utcnow() + timedelta(hours=1),
            'iat': datetime.utcnow()
        }
        
        # Vulnerable: Using weak secret and no signature verification
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        
        # Also create a "none" algorithm token (very vulnerable)
        none_payload = payload.copy()
        none_token = jwt.encode(none_payload, '', algorithm='none')
        
        content = f'''
        <div class="result">
            <h3>Generated JWT Tokens:</h3>
            <p><strong>Standard Token:</strong></p>
            <pre>{token}</pre>
            <p><strong>"None" Algorithm Token:</strong></p>
            <pre>{none_token}</pre>
        </div>
        
        <h2>🎫 JWT Token Generator</h2>
        <form method="POST">
            <label>Username:</label><br>
            <input type="text" name="username" value="{username}"><br><br>
            <button type="submit">Generate JWT</button>
        </form>
        
        <div class="challenge">
            <h4>💡 JWT Vulnerabilities:</h4>
            <ul>
                <li>Weak secret key: <code>{JWT_SECRET}</code></li>
                <li>"None" algorithm accepted</li>
                <li>No proper signature verification</li>
                <li>Client-side role management</li>
            </ul>
        </div>
        '''
    else:
        content = '''
        <h2>🎫 JWT Token Generator</h2>
        <form method="POST">
            <label>Username:</label><br>
            <input type="text" name="username" placeholder="guest"><br><br>
            <button type="submit">Generate JWT</button>
        </form>
        
        <div class="challenge">
            <h4>💡 JWT Vulnerabilities:</h4>
            <ul>
                <li>Weak secret key</li>
                <li>"None" algorithm accepted</li>
                <li>No proper signature verification</li>
                <li>Client-side role management</li>
            </ul>
        </div>
        '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/reset', methods=['GET', 'POST'])
def password_reset():
    if request.method == 'POST':
        email = request.form.get('email', '')
        
        # Vulnerable password reset
        user_found = None
        for username, user_data in USERS.items():
            if user_data['email'] == email:
                user_found = username
                break
        
        if user_found:
            # Generate predictable reset token
            reset_token = hashlib.md5(f"{email}_reset_2024".encode()).hexdigest()
            
            content = f'''
            <div class="result success">
                <h3>Reset Link Generated!</h3>
                <p>Password reset link (normally sent via email):</p>
                <p><a href="./reset?token={reset_token}&user={user_found}">Reset Password</a></p>
                <p><strong>Reset Token:</strong> {reset_token}</p>
            </div>
            '''
        else:
            content = '''
            <div class="result error">
                <p>Email not found in system</p>
            </div>
            '''
        
        content += '''
        <h2>🔄 Password Reset</h2>
        <form method="POST">
            <label>Email Address:</label><br>
            <input type="email" name="email" required><br><br>
            <button type="submit">Send Reset Link</button>
        </form>
        
        <div class="challenge">
            <h4>💡 Reset Vulnerabilities:</h4>
            <ul>
                <li>Predictable reset tokens</li>
                <li>User enumeration via different responses</li>
                <li>No token expiration</li>
                <li>Username exposed in URL</li>
            </ul>
        </div>
        '''
    else:
        # Check for reset token
        token = request.args.get('token')
        user = request.args.get('user')
        
        if token and user:
            content = f'''
            <div class="result flag">
                <h3>🎉 Password Reset Access Granted!</h3>
                <p>You can now reset password for user: {user}</p>
                <p><strong>FLAG:</strong> CTF{{p4ssw0rd_r3s3t_vuln_2024}}</p>
            </div>
            
            <h2>🔄 Reset Password for {user}</h2>
            <form>
                <label>New Password:</label><br>
                <input type="password" name="new_password"><br>
                <label>Confirm Password:</label><br>
                <input type="password" name="confirm_password"><br><br>
                <button type="button" onclick="alert('Password would be reset in real scenario')">Reset Password</button>
            </form>
            '''
        else:
            content = '''
            <h2>🔄 Password Reset</h2>
            <form method="POST">
                <label>Email Address:</label><br>
                <input type="email" name="email" required><br><br>
                <button type="submit">Send Reset Link</button>
            </form>
            
            <div class="challenge">
                <h4>💡 Reset Vulnerabilities:</h4>
                <ul>
                    <li>Predictable reset tokens</li>
                    <li>User enumeration via different responses</li>
                    <li>No token expiration</li>
                    <li>Username exposed in URL</li>
                </ul>
            </div>
            '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/admin')
def admin_panel():
    if session.get('role') == 'admin' or session.get('authenticated'):
        content = '''
        <h2>🔒 Admin Panel</h2>
        <div class="result flag">
            <h3>🎉 Access Granted!</h3>
            <p>You've successfully accessed the admin panel through authentication bypass!</p>
            <p><strong>Additional FLAG:</strong> CTF{4dm1n_4cc3ss_gr4nt3d_2024}</p>
        </div>
        
        <div class="session-info">
            <h3>Admin Functions:</h3>
            <ul>
                <li>User Management</li>
                <li>System Configuration</li>
                <li>Audit Logs</li>
                <li>Flag Collection</li>
            </ul>
        </div>
        '''
    else:
        content = '''
        <h2>🔒 Admin Panel</h2>
        <div class="result error">
            <p>Access Denied! Admin authentication required.</p>
            <p>Please login as admin first.</p>
        </div>
        '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/debug')
def debug_info():
    """Debug endpoint exposing sensitive information"""
    debug_data = {
        'users': USERS,
        'jwt_secret': JWT_SECRET,
        'session_data': dict(session),
        'redis_keys': redis_client.keys('*') if redis_client.ping() else []
    }
    return jsonify(debug_data)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=5002, debug=True) 