#!/usr/bin/env python3
"""
OWASP Top 10 - A03: Injection Vulnerabilities
This application intentionally contains multiple injection vulnerabilities for educational purposes.
"""

import os
import subprocess
import mysql.connector
from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import logging

app = Flask(__name__)
app.secret_key = 'vulnerable_secret_key_123'

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'mysql'),
    'user': os.getenv('DB_USER', 'ctf_user'),
    'password': os.getenv('DB_PASSWORD', 'vulnerable123'),
    'database': os.getenv('DB_NAME', 'injection_db'),
    'autocommit': True
}

def get_db_connection():
    """Get database connection"""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        logging.error(f"Database connection failed: {err}")
        return None

# HTML Templates (inline for simplicity)
BASE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Injection Challenges - OWASP A03</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        .challenge { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        .warning { background: #fff3cd; border-color: #ffc107; color: #856404; }
        input, textarea { width: 300px; padding: 8px; margin: 5px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin: 10px 0; padding: 10px; background: #f8f9fa; border-left: 3px solid #007bff; }
        .flag { background: #d4edda; border-left-color: #28a745; color: #155724; font-weight: bold; }
        pre { background: #f8f9fa; padding: 10px; border-radius: 3px; overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background: #f2f2f2; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Injection Vulnerabilities Challenge</h1>
        <div class="challenge warning">
            <h3>⚠️ Educational Purpose Only</h3>
            <p>This application contains intentional vulnerabilities. Find and exploit them to capture flags!</p>
        </div>
        
        {{ content | safe }}
        
        <div style="margin-top: 30px; padding: 15px; background: #e9ecef; border-radius: 5px;">
            <h3>🎯 Available Challenges:</h3>
            <ul>
                <li><a href="./">Home</a></li>
                <li><a href="./search">SQL Injection - Product Search</a></li>
                <li><a href="./login">SQL Injection - Login Bypass</a></li>
                <li><a href="./ping">Command Injection - Network Tools</a></li>
            </ul>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    content = '''
    <h2>Welcome to the Injection Challenge Lab</h2>
    <p>This application contains three injection vulnerabilities following the OWASP Top 10.</p>
    
    <div class="challenge">
        <h3>Your Mission:</h3>
        <ul>
            <li>Find SQL Injection vulnerabilities to access hidden data</li>
            <li>Bypass authentication using SQL injection</li>
            <li>Use Command Injection to execute system commands</li>
            <li>Capture flags in the format: <code>CTF{...}</code></li>
        </ul>
    </div>
    
    <div class="challenge">
        <h3>Hints:</h3>
        <ul>
            <li>Try different SQL payloads: <code>' OR '1'='1</code></li>
            <li>Look for authentication bypass opportunities</li>
            <li>Command injection: Try chaining commands with <code>;</code> or <code>&&</code></li>
            <li>Environment variables may contain sensitive information</li>
        </ul>
    </div>
    '''
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/search')
def search_form():
    query = request.args.get('q', '')
    results = []
    
    if query:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                vulnerable_query = f"SELECT id, name, price, description FROM products WHERE name LIKE '%{query}%'"
                logging.info(f"Executing query: {vulnerable_query}")
                cursor.execute(vulnerable_query)
                results = cursor.fetchall()
            except mysql.connector.Error as err:
                results = [("Error", str(err), "", "")]
            finally:
                cursor.close()
                conn.close()
    
    content = f'''
    <h2>🔍 Product Search (SQL Injection Challenge)</h2>
    <form method="GET" action="./search">
        <label>Search Products:</label><br>
        <input type="text" name="q" placeholder="Enter product name..." value="{query}">
        <button type="submit">Search</button>
    </form>
    
    {'<div class="result"><h3>Search Results:</h3><table><tr><th>ID</th><th>Name</th><th>Price</th><th>Description</th></tr>' if results else ''}
    {''.join([f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>${row[2]}</td><td>{row[3]}</td></tr>' for row in results]) if results else ''}
    {'</table></div>' if results else ''}
    
    <div class="challenge">
        <h4>💡 Hint:</h4>
        <p>The search functionality might be vulnerable to SQL injection. Try searching for: <code>' OR 1=1; --</code></p>
    </div>
    '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                query = f"SELECT id, username, role FROM users WHERE username = '{username}' AND password = '{password}'"
                logging.info(f"Login query: {query}")
                cursor.execute(query)
                user = cursor.fetchone()
                
                if user:
                    session['user_id'] = user[0]
                    session['username'] = user[1] 
                    session['role'] = user[2]
                    
                    if user[2] == 'admin':
                        flag = os.getenv('FLAG_A03', 'CTF{1nj3ct10n_m4st3r_2025}')
                        content = f'''
                        <div class="result flag">
                            <h2>🎉 Login Successful!</h2>
                            <p>Welcome, Admin {user[1]}!</p>
                            <p><strong>FLAG CAPTURED:</strong> {flag}</p>
                        </div>
                        '''
                    else:
                        content = f'''
                        <div class="result">
                            <h2>Login Successful</h2>
                            <p>Welcome, {user[1]} ({user[2]})!</p>
                        </div>
                        '''
                else:
                    content = '''
                    <div class="result">
                        <p style="color: red;">Invalid credentials!</p>
                    </div>
                    '''
            except mysql.connector.Error as err:
                content = f'''
                <div class="result">
                    <p style="color: red;">Database error: {str(err)}</p>
                </div>
                '''
            finally:
                cursor.close()
                conn.close()
        else:
            content = '<div class="result"><p style="color: red;">Database connection failed!</p></div>'
            
        content += '''
        <h2>🔐 Admin Login (SQL Injection Challenge)</h2>
        <form method="POST">
            <label>Username:</label><br>
            <input type="text" name="username" required><br>
            <label>Password:</label><br>
            <input type="password" name="password" required><br><br>
            <button type="submit">Login</button>
        </form>
        
        <div class="challenge">
            <h4>💡 Hint:</h4>
            <p>Try bypassing authentication for user: <code>admin</code></p>
        </div>
        '''
        
    else:
        content = '''
        <h2>🔐 Admin Login (SQL Injection Challenge)</h2>
        <form method="POST">
            <label>Username:</label><br>
            <input type="text" name="username" required><br>
            <label>Password:</label><br>
            <input type="password" name="password" required><br><br>
            <button type="submit">Login</button>
        </form>
        
        <div class="challenge">
            <h4>💡 Hint:</h4>
            <p>Try bypassing authentication for user: <code>admin</code></p>
        </div>
        '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/ping', methods=['GET', 'POST'])
def ping_tool():
    if request.method == 'POST':
        host = request.form.get('host', '127.0.0.1')
        
        try:
            command = f"ping -c 4 {host}"
            logging.info(f"Executing command: {command}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
            output = result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            output = "Command timed out"
        except Exception as e:
            output = f"Error: {str(e)}"
        
        content = f'''
        <h2>🌐 Network Ping Tool (Command Injection Challenge)</h2>
        <form method="POST">
            <label>Host to ping:</label><br>
            <input type="text" name="host" value="{host}" placeholder="127.0.0.1">
            <button type="submit">Ping</button>
        </form>
        
        <div class="result">
            <h3>Command Output:</h3>
            <pre>{output}</pre>
        </div>
        
        <div class="challenge">
            <h4>💡 Hint:</h4>
            <p>The system has sensitive information stored in environment variables. Try command injection to read them.</p>
        </div>
        '''
    else:
        content = '''
        <h2>🌐 Network Ping Tool (Command Injection Challenge)</h2>
        <form method="POST">
            <label>Host to ping:</label><br>
            <input type="text" name="host" placeholder="127.0.0.1">
            <button type="submit">Ping</button>
        </form>
        
        <div class="challenge">
            <h4>💡 Hint:</h4>
            <p>The system has sensitive information stored in environment variables. Try command injection to read them.</p>
        </div>
        '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=5001, debug=True) 