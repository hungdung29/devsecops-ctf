#!/usr/bin/env python3
"""
OWASP Top 10 - A01: Broken Access Control
This application demonstrates various access control vulnerabilities for educational purposes.
"""

import os
import psycopg2
from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import logging

app = Flask(__name__)
app.secret_key = 'insecure_access_control_key_456'

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'postgres'),
    'user': os.getenv('DB_USER', 'ctf_user'),
    'password': os.getenv('DB_PASSWORD', 'insecure456'),
    'database': os.getenv('DB_NAME', 'access_db'),
    'port': 5432
}

def get_db_connection():
    """Get database connection"""
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.Error as err:
        logging.error(f"Database connection failed: {err}")
        return None

def get_user_info():
    """Generate user info HTML based on session"""
    if session.get('username'):
        username = session.get('username')
        role = session.get('role', 'user')
        return f'''
        <div class="user-info">
            <strong>Logged in as:</strong> {username} ({role})
            <a href="./logout" style="margin-left: 20px;">Logout</a>
        </div>
        '''
    return ''

# HTML Template
BASE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Access Control Challenges - OWASP A01</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        .challenge { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        .warning { background: #fff3cd; border-color: #ffc107; color: #856404; }
        .success { background: #d4edda; border-color: #28a745; color: #155724; }
        .error { background: #f8d7da; border-color: #dc3545; color: #721c24; }
        input { width: 300px; padding: 8px; margin: 5px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin: 10px 0; padding: 10px; background: #f8f9fa; border-left: 3px solid #007bff; }
        .flag { background: #d4edda; border-left-color: #28a745; color: #155724; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background: #f2f2f2; }
        .user-info { background: #e9ecef; padding: 10px; border-radius: 5px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚫 Broken Access Control Challenge</h1>
        <div class="challenge warning">
            <h3>⚠️ Educational Purpose Only</h3>
            <p>This application contains intentional access control vulnerabilities. Exploit them to capture flags!</p>
        </div>
        
        {{ user_info | safe }}
        
        {{ content | safe }}
        
        <div style="margin-top: 30px; padding: 15px; background: #e9ecef; border-radius: 5px;">
            <h3>🎯 Available Challenges:</h3>
            <ul>
                <li><a href="./">Home</a></li>
                <li><a href="./login">Login</a></li>
                <li><a href="./profile">User Profile</a></li>
                <li><a href="./admin">Admin Panel</a></li>
                <li><a href="./files">File Access</a></li>
            </ul>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    content = '''
    <h2>Welcome to the Access Control Security Lab</h2>
    <p>This application demonstrates common access control vulnerabilities from OWASP A01.</p>
    
    <div class="challenge">
        <h3>Your Mission:</h3>
        <ul>
            <li>Bypass access controls to access unauthorized data</li>
            <li>Exploit Insecure Direct Object References (IDOR)</li>
            <li>Access admin functionality as a regular user</li>
            <li>Find horizontal and vertical privilege escalation flaws</li>
            <li>Capture flags in the format: <code>CTF{...}</code></li>
        </ul>
    </div>
    
    <div class="challenge">
        <h3>Test Accounts:</h3>
        <ul>
            <li><code>employee1 / password123</code> (Regular User)</li>
            <li><code>employee2 / qwerty456</code> (Regular User)</li>
            <li><code>admin</code> (Administrator)</li>
        </ul>
    </div>
    '''
    return render_template_string(BASE_TEMPLATE, content=content, user_info=get_user_info())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT id, username, password_hash, role FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()
                
                if user and user[2] == password:  # Plain text password comparison
                    session['user_id'] = user[0]
                    session['username'] = user[1]
                    session['role'] = user[3]
                    
                    if user[3] == 'admin':
                        content = f'''
                        <div class="result flag">
                            <h2>🎉 Admin Login Successful!</h2>
                            <p>Welcome, {user[1]}!</p>
                        </div>
                        '''
                    else:
                        content = f'''
                        <div class="result success">
                            <h2>Login Successful</h2>
                            <p>Welcome, {user[1]} ({user[3]})!</p>
                        </div>
                        '''
                else:
                    content = '''
                    <div class="result error">
                        <p>Invalid username or password!</p>
                    </div>
                    '''
            except Exception as e:
                content = f'<div class="result error"><p>Database error: {str(e)}</p></div>'
            finally:
                cursor.close()
                conn.close()
        else:
            content = '<div class="result error"><p>Database connection failed!</p></div>'
    else:
        content = ''
    
    login_form = '''
    <h2>🔐 Login</h2>
    <form method="POST">
        <label>Username:</label><br>
        <input type="text" name="username" required><br>
        <label>Password:</label><br>
        <input type="password" name="password" required><br>
        <button type="submit">Login</button>
    </form>
    ''' + content
    
    return render_template_string(BASE_TEMPLATE, content=login_form, user_info=get_user_info())

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    if not session.get('username'):
        return redirect('/access/login')
    
    user_id = session.get('user_id')
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, username, email, role, created_at FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            
            if user:
                content = f'''
                <h2>👤 User Profile</h2>
                <div class="result">
                    <p><strong>ID:</strong> {user[0]}</p>
                    <p><strong>Username:</strong> {user[1]}</p>
                    <p><strong>Email:</strong> {user[2]}</p>
                    <p><strong>Role:</strong> {user[3]}</p>
                    <p><strong>Created:</strong> {user[4]}</p>
                </div>
                '''
            else:
                content = '<div class="result error"><p>User not found!</p></div>'
        except Exception as e:
            content = f'<div class="result error"><p>Database error: {str(e)}</p></div>'
        finally:
            cursor.close()
            conn.close()
    else:
        content = '<div class="result error"><p>Database connection failed!</p></div>'
    
    return render_template_string(BASE_TEMPLATE, content=content, user_info=get_user_info())

@app.route('/admin')
def admin():
    if not session.get('username'):
        return redirect('/access/login')
    
    content = '''
    <h2>⚙️ Admin Panel</h2>
    <div class="result flag">
        <h3>🎉 Access Control Bypassed!</h3>
        <p>You've accessed the admin panel without proper authorization!</p>
        <p><strong>FLAG:</strong> CTF{4cc3ss_c0ntr0l_pwn3d_2025}</p>
    </div>
    
    <div class="challenge">
        <h3>Admin Functions:</h3>
        <ul>
            <li><a href="./admin/users">Manage Users</a></li>
        </ul>
    </div>
    '''
    
    return render_template_string(BASE_TEMPLATE, content=content, user_info=get_user_info())

@app.route('/admin/users')
def admin_users():
    if not session.get('username'):
        return redirect('/access/login')
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, username, email, role FROM users ORDER BY id")
            users = cursor.fetchall()
            
            user_rows = ''
            for user in users:
                user_rows += f'<tr><td>{user[0]}</td><td>{user[1]}</td><td>{user[2]}</td><td>{user[3]}</td></tr>'
            
            content = f'''
            <h2>👥 User Management</h2>
            <table>
                <tr><th>ID</th><th>Username</th><th>Email</th><th>Role</th></tr>
                {user_rows}
            </table>
            '''
        except Exception as e:
            content = f'<div class="result error"><p>Database error: {str(e)}</p></div>'
        finally:
            cursor.close()
            conn.close()
    else:
        content = '<div class="result error"><p>Database connection failed!</p></div>'
    
    return render_template_string(BASE_TEMPLATE, content=content, user_info=get_user_info())

@app.route('/api/users')
def api_users():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, username, email, role FROM users")
            users = cursor.fetchall()
            
            user_list = []
            for user in users:
                user_list.append({
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'role': user[3]
                })
            
            return jsonify({'users': user_list, 'flag': os.getenv('FLAG_API', 'CTF{4p1_4cc3ss_n0_4uth_2025}')})
        except Exception as e:
            return jsonify({'error': str(e)})
        finally:
            cursor.close()
            conn.close()
    
    return jsonify({'error': 'Database connection failed'})

@app.route('/files')
def files():
    filename = request.args.get('file', 'readme.txt')
    
    try:
        with open(f'/app/data/{filename}', 'r') as f:
            content = f.read()
        
        file_content = f'''
        <h2>📁 File Viewer</h2>
        <p><strong>File:</strong> {filename}</p>
        <div class="result">
            <pre>{content}</pre>
        </div>
        
        <div class="challenge">
            <h4>💡 Path Traversal Challenge:</h4>
            <p>Try accessing other files.</p>
        </div>
        '''
    except Exception as e:
        file_content = f'<div class="result error"><p>Error reading file: {str(e)}</p></div>'
    
    return render_template_string(BASE_TEMPLATE, content=file_content, user_info=get_user_info())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True) 