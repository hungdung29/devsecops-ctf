#!/usr/bin/env python3
"""
OWASP Top 10 - A02: Cryptographic Failures
This application demonstrates various cryptographic vulnerabilities for educational purposes.
"""

import os
import base64
import hashlib
import hmac
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad, unpad
from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import logging
import secrets
import time

app = Flask(__name__)
app.secret_key = 'weak_crypto_secret_key_2025'


# HTML Template
BASE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Cryptographic Failures - OWASP A02</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        .challenge { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        .warning { background: #fff3cd; border-color: #ffc107; color: #856404; }
        .success { background: #d4edda; border-color: #28a745; color: #155724; }
        .error { background: #f8d7da; border-color: #dc3545; color: #721c24; }
        input, textarea { width: 300px; padding: 8px; margin: 5px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin: 10px 0; padding: 10px; background: #f8f9fa; border-left: 3px solid #007bff; }
        .flag { background: #d4edda; border-left-color: #28a745; color: #155724; font-weight: bold; }
        pre { background: #f8f9fa; padding: 10px; border-radius: 3px; overflow-x: auto; }
        .crypto-box { background: #e9ecef; padding: 15px; border-radius: 5px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 Cryptographic Failures Challenge</h1>
        <div class="challenge warning">
            <h3>⚠️ Educational Purpose Only</h3>
            <p>This application contains intentional cryptographic vulnerabilities. Exploit them to capture flags!</p>
        </div>
        
        {{ content | safe }}
        
        <div style="margin-top: 30px; padding: 15px; background: #e9ecef; border-radius: 5px;">
            <h3>🎯 Available Challenges:</h3>
            <ul>
                <li><a href="./">Home</a></li>
                <li><a href="./weak_hash">Weak Hashing</a></li>
                <li><a href="./weak_random">Weak Random Generation</a></li>
            </ul>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    content = '''
    <h2>Welcome to the Cryptographic Security Lab</h2>
    <p>This application demonstrates common cryptographic vulnerabilities from OWASP A02.</p>
    
    <div class="challenge">
        <h3>Your Mission:</h3>
        <ul>
            <li>Exploit weak hashing algorithms</li>
            <li>Bypass weak random number generation</li>
            <li>Capture flags in the format: <code>CTF{...}</code></li>
        </ul>
    </div>
    
    <div class="challenge">
        <h3>Common Crypto Weaknesses:</h3>
        <ul>
            <li>MD5 and SHA1 hashing</li>
            <li>DES and weak AES implementations</li>
            <li>Predictable random values</li>
            <li>Hardcoded encryption keys</li>
        </ul>
    </div>
    '''
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/weak_hash', methods=['GET', 'POST'])
def weak_hash():
    common_words = [
        'password', 'welcome', 'sunshine', 'dragon', 'monkey', 'football', 
        'master', 'secret', 'hello', 'summer', 'winter', 'spring', 'flower',
        'rainbow', 'butterfly', 'mountain', 'ocean', 'freedom', 'happiness',
        'chocolate', 'pizza', 'coffee', 'music', 'guitar', 'dancing'
    ]
    
    import random
    random.seed(hash(app.secret_key) % (2**32))
    
    word = random.choice(common_words)
    digits = random.randint(0, 9)  # 1-3 digits
    admin_password = f"{word}{digits}"
    admin_md5 = hashlib.md5(admin_password.encode()).hexdigest()
    
    # Rate limiting implementation
    if 'hash_attempts' not in session:
        session['hash_attempts'] = 0
        session['last_attempt_time'] = 0
    
    current_time = time.time()
    time_since_last = current_time - session.get('last_attempt_time', 0)
    
    # Reset attempts if more than 60 seconds have passed
    if time_since_last > 60:
        session['hash_attempts'] = 0
    
    if request.method == 'POST':
        # Check rate limit
        if session['hash_attempts'] >= 5:
            remaining_time = 60 - time_since_last
            if remaining_time > 0:
                result = f'''
                <div class="result error">
                    <h3>⚠️ Rate Limited!</h3>
                    <p>Too many attempts. Please wait {remaining_time:.0f} seconds before trying again.</p>
                    <p>This prevents brute force attacks. Use external tools to crack the hash!</p>
                </div>
                '''
                content = f'''
                <h2>🔓 Weak Hash Challenge</h2>
                
                <div class="crypto-box">
                    <h4>🔍 Password Hasher</h4>
                    <form method="POST">
                        <label>Enter Password:</label><br>
                        <input type="text" name="password" required disabled><br>
                        <button type="submit" disabled>Hash Password (Rate Limited)</button>
                    </form>
                </div>
                
                {result}
                
                <div class="challenge">
                    <h4>💡 Challenge Goal:</h4>
                    <p>The admin's password has been hashed using MD5. Can you crack it?</p>
                    <p><strong>Admin's MD5 Hash:</strong> <code>{admin_md5}</code></p>
                    <p>💡 Hint: The password is a common word followed by 1-3 digits!</p>
                    <p>💡 Use external MD5 crackers or tools - this form is rate limited!</p>
                    
                    <h5>🛠️ Exploitation Tips:</h5>
                    <ul>
                        <li>MD5 is cryptographically broken and vulnerable to rainbow table attacks</li>
                        <li>Try common passwords with simple variations</li>
                        <li>Use tools like <code>hashcat</code> or online hash crackers</li>
                        <li>Consider dictionary attacks with common words + numbers</li>
                        <li><strong>Rate limiting prevents web-based brute force!</strong></li>
                    </ul>
                </div>
                '''
                return render_template_string(BASE_TEMPLATE, content=content)
        
        # Increment attempt counter
        session['hash_attempts'] += 1
        session['last_attempt_time'] = current_time
        
        # Add delay based on number of attempts
        if session['hash_attempts'] > 1:
            delay = min(session['hash_attempts'] * 2, 10)  # Max 10 second delay
            time.sleep(delay)
        password = request.form.get('password', '')
        
        # Weak hashing algorithms
        md5_hash = hashlib.md5(password.encode()).hexdigest()
        sha1_hash = hashlib.sha1(password.encode()).hexdigest()
        
        # Check for admin password
        if md5_hash == admin_md5:
            flag = os.getenv('FLAG_A02_HASH', 'CTF{md5_1s_br0k3n_us3_bcrypt_2025}')
            result = f'''
            <div class="result flag">
                <h3>🎉 Flag Captured!</h3>
                <p>You cracked the admin password: <strong>{password}</strong></p>
                <p><strong>FLAG:</strong> {flag}</p>
            </div>
            '''
        else:
            result = f'''
            <div class="result">
                <p><strong>Input:</strong> {password}</p>
                <p><strong>MD5:</strong> {md5_hash}</p>
                <p><strong>SHA1:</strong> {sha1_hash}</p>
            </div>
            '''
        
        attempts_left = max(0, 5 - session['hash_attempts'])
        content = f'''
        <h2>🔓 Weak Hash Challenge</h2>
        
        <div class="crypto-box">
            <h4>🔍 Password Hasher</h4>
            <form method="POST">
                <label>Enter Password:</label><br>
                <input type="text" name="password" value="{password}" required><br>
                <button type="submit">Hash Password</button>
            </form>
            <p><strong>Attempts remaining:</strong> {attempts_left}/5 (Rate limited to prevent brute force)</p>
        </div>
        
        {result}
        
        <div class="challenge">
            <h4>💡 Challenge Goal:</h4>
            <p>The admin's password has been hashed using MD5. Can you crack it?</p>
            <p><strong>Admin's MD5 Hash:</strong> <code>{admin_md5}</code></p>
            <p>💡 Hint: The password is a common word followed by 1-3 digits!</p>
            <p>💡 Use external MD5 crackers or tools - this form is rate limited!</p>
            
            <h5>🛠️ Exploitation Tips:</h5>
            <ul>
                <li>MD5 is cryptographically broken and vulnerable to rainbow table attacks</li>
                <li>Try common passwords with simple variations</li>
                <li>Use tools like <code>hashcat</code> or online hash crackers</li>
                <li>Consider dictionary attacks with common words + numbers</li>
                <li><strong>Rate limiting prevents web-based brute force!</strong></li>
            </ul>
        </div>
        '''
    else:
        attempts_left = max(0, 5 - session.get('hash_attempts', 0))
        content = f'''
        <h2>🔓 Weak Hash Challenge</h2>
        
        <div class="crypto-box">
            <h4>🔍 Password Hasher</h4>
            <form method="POST">
                <label>Enter Password:</label><br>
                <input type="text" name="password" required><br>
                <button type="submit">Hash Password</button>
            </form>
            <p><strong>Attempts remaining:</strong> {attempts_left}/5 (Rate limited to prevent brute force)</p>
        </div>
        
        <div class="challenge">
            <h4>💡 Challenge Goal:</h4>
            <p>The admin's password has been hashed using MD5. Can you crack it?</p>
            <p><strong>Admin's MD5 Hash:</strong> <code>{admin_md5}</code></p>
            <p>💡 Hint: The password is a common word followed by 1-3 digits!</p>
            <p>💡 Use external MD5 crackers or tools - this form is rate limited!</p>
            
            <h5>🛠️ Exploitation Tips:</h5>
            <ul>
                <li>MD5 is cryptographically broken and vulnerable to rainbow table attacks</li>
                <li>Try common passwords with simple variations</li>
                <li>Use tools like <code>hashcat</code> or online hash crackers</li>
                <li>Consider dictionary attacks with common words + numbers</li>
                <li><strong>Rate limiting prevents web-based brute force!</strong></li>
            </ul>
        </div>
        '''
    
    return render_template_string(BASE_TEMPLATE, content=content)


@app.route('/weak_random', methods=['GET', 'POST'])
def weak_random():
    # Weak random number generation using predictable seeding
    import random
    
    # Use current time rounded to 30 seconds for predictability
    current_time = int(time.time())
    rounded_time = (current_time // 30) * 30  # Round to nearest 30 seconds
    
    # Seed with rounded time (predictable)
    random.seed(rounded_time)
    weak_random = random.randint(1000, 9999)
    
    if request.method == 'POST':
        guess = request.form.get('guess', '')
        
        try:
            guess_int = int(guess)
            if guess_int == weak_random:
                flag = os.getenv('FLAG_A02_RANDOM', 'CTF{w34k_r4nd0m_pr3d1ct4bl3_2025}')
                result = f'''
                <div class="result flag">
                    <h3>🎉 Flag Captured!</h3>
                    <p>You correctly predicted the random number: <strong>{weak_random}</strong></p>
                    <p><strong>FLAG:</strong> {flag}</p>
                </div>
                '''
            else:
                result = f'''
                <div class="result error">
                    <p>Wrong guess! You guessed <strong>{guess_int}</strong>, but the number was <strong>{weak_random}</strong></p>
                    <p>💡 Hint: The seed changes every 30 seconds. Try to predict the next one!</p>
                </div>
                '''
        except ValueError:
            result = f'''
            <div class="result error">
                <p>Invalid input. Please enter a number between 1000 and 9999.</p>
            </div>
            '''
        
        content = f'''
        <h2>🎯 Weak Random Generation Challenge</h2>
        
        <div class="crypto-box">
            <h4>🎲 Random Number Guesser</h4>
            <p>A "random" number has been generated. Can you predict it?</p>
            <form method="POST">
                <label>Enter your guess (1000-9999):</label><br>
                <input type="number" name="guess" min="1000" max="9999" value="{guess}" required><br>
                <button type="submit">Submit Guess</button>
            </form>
        </div>
        
        {result}
        
        <div class="challenge">
            <h4>💡 Challenge Information:</h4>
            <p><strong>Current Time:</strong> {current_time}</p>
            <p><strong>Seed Time:</strong> {rounded_time} (rounded to 30s intervals)</p>
            <p><strong>Algorithm:</strong> <code>random.seed(rounded_time); random.randint(1000, 9999)</code></p>
            
            <h5>🛠️ Exploitation Strategy:</h5>
            <ul>
                <li>The random number is seeded with the current time rounded to 30-second intervals</li>
                <li>You can predict the next number by calculating the seed yourself</li>
            </ul>
            
            <h5>⚠️ Security Lesson:</h5>
            <p>Never use predictable seeds for cryptographic purposes. Use <code>secrets</code> module instead!</p>
        </div>
        '''
    else:
        content = f'''
        <h2>🎯 Weak Random Generation Challenge</h2>
        
        <div class="crypto-box">
            <h4>🎲 Random Number Guesser</h4>
            <p>A "random" number has been generated. Can you predict it?</p>
            <form method="POST">
                <label>Enter your guess (1000-9999):</label><br>
                <input type="number" name="guess" min="1000" max="9999" required><br>
                <button type="submit">Submit Guess</button>
            </form>
        </div>
        
        <div class="challenge">
            <h4>💡 Challenge Information:</h4>
            <p><strong>Current Time:</strong> {current_time}</p>
            <p><strong>Seed Time:</strong> {rounded_time} (rounded to 30s intervals)</p>
            <p><strong>Algorithm:</strong> <code>random.seed(rounded_time); random.randint(1000, 9999)</code></p>
            
            <h5>🛠️ Exploitation Strategy:</h5>
            <ul>
                <li>The random number is seeded with the current time rounded to 30-second intervals</li>
                <li>You can predict the next number by calculating the seed yourself</li>
            </ul>
            
            <h5>⚠️ Security Lesson:</h5>
            <p>Never use predictable seeds for cryptographic purposes. Use <code>secrets</code> module instead!</p>
        </div>
        '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True) 