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
app.secret_key = 'weak_crypto_secret_key_2024'

# Weak encryption keys
WEAK_KEY = os.getenv('WEAK_ENCRYPTION_KEY', '1234567890123456')  # 16 bytes
WEAK_DES_KEY = b'WEAK1234'  # 8 bytes for DES
WEAK_AES_KEY = b'WEAK_AES_KEY_123'  # 16 bytes for AES

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
                <li><a href="./weak_encryption">Weak Encryption</a></li>
                <li><a href="./ecb_mode">ECB Mode Encryption</a></li>
                <li><a href="./predictable_tokens">Predictable Tokens</a></li>
                <li><a href="./weak_random">Weak Random Generation</a></li>
                <li><a href="./hardcoded_secrets">Hardcoded Secrets</a></li>
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
            <li>Break weak encryption implementations</li>
            <li>Exploit weak hashing algorithms</li>
            <li>Find hardcoded secrets and keys</li>
            <li>Bypass weak random number generation</li>
            <li>Capture flags in the format: <code>CTF{...}</code></li>
        </ul>
    </div>
    
    <div class="challenge">
        <h3>Common Crypto Weaknesses:</h3>
        <ul>
            <li>MD5 and SHA1 hashing</li>
            <li>DES and weak AES implementations</li>
            <li>ECB mode encryption</li>
            <li>Predictable random values</li>
            <li>Hardcoded encryption keys</li>
        </ul>
    </div>
    '''
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/weak_hash', methods=['GET', 'POST'])
def weak_hash():
    if request.method == 'POST':
        password = request.form.get('password', '')
        
        # Weak hashing algorithms
        md5_hash = hashlib.md5(password.encode()).hexdigest()
        sha1_hash = hashlib.sha1(password.encode()).hexdigest()
        
        # Check for admin password
        admin_md5 = hashlib.md5(b'admin123').hexdigest()
        if md5_hash == admin_md5:
            flag = os.getenv('FLAG_A02', 'CTF{cr4pt0_f41lur3_3xp0s3d_2024}')
            result = f'''
            <div class="result flag">
                <h3>🎉 Flag Captured!</h3>
                <p>You cracked the admin password!</p>
                <p><strong>FLAG:</strong> {flag}</p>
            </div>
            '''
        else:
            result = f'''
            <div class="result">
                <p><strong>MD5:</strong> {md5_hash}</p>
                <p><strong>SHA1:</strong> {sha1_hash}</p>
            </div>
            '''
        
        content = f'''
        <h2>🔓 Weak Hash Challenge</h2>
        <form method="POST">
            <label>Enter Password:</label><br>
            <input type="text" name="password" value="{password}" required><br>
            <button type="submit">Hash Password</button>
        </form>
        {result}
        
        <div class="challenge">
            <h4>💡 Hint:</h4>
            <p>The admin password is hashed using MD5. Try common passwords!</p>
            <p>Admin MD5: {admin_md5}</p>
        </div>
        '''
    else:
        admin_md5 = hashlib.md5(b'admin123').hexdigest()
        content = f'''
        <h2>🔓 Weak Hash Challenge</h2>
        <form method="POST">
            <label>Enter Password:</label><br>
            <input type="text" name="password" required><br>
            <button type="submit">Hash Password</button>
        </form>
        
        <div class="challenge">
            <h4>💡 Hint:</h4>
            <p>The admin password is hashed using MD5. Try common passwords!</p>
            <p>Admin MD5: {admin_md5}</p>
        </div>
        '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/weak_encryption', methods=['GET', 'POST'])
def weak_encryption():
    if request.method == 'POST':
        plaintext = request.form.get('plaintext', '')
        
        # DES encryption (very weak)
        des_cipher = DES.new(WEAK_DES_KEY, DES.MODE_ECB)
        
        # Pad the plaintext to be a multiple of 8 bytes
        padded_text = pad(plaintext.encode(), 8)
        encrypted = des_cipher.encrypt(padded_text)
        encrypted_b64 = base64.b64encode(encrypted).decode()
        
        content = f'''
        <h2>🔒 Weak Encryption Challenge</h2>
        <form method="POST">
            <label>Enter Text to Encrypt:</label><br>
            <textarea name="plaintext" required>{plaintext}</textarea><br>
            <button type="submit">Encrypt with DES</button>
        </form>
        
        <div class="result">
            <p><strong>Original:</strong> {plaintext}</p>
            <p><strong>DES Encrypted (Base64):</strong> {encrypted_b64}</p>
        </div>
        
        <div class="challenge">
            <h4>💡 Challenge:</h4>
            <p>DES is extremely weak! The key is: <code>{WEAK_DES_KEY.decode()}</code></p>
            <p>Try decrypting this secret: <code>4P7K+urL5eA=</code></p>
        </div>
        '''
    else:
        content = '''
        <h2>🔒 Weak Encryption Challenge</h2>
        <form method="POST">
            <label>Enter Text to Encrypt:</label><br>
            <textarea name="plaintext" required></textarea><br>
            <button type="submit">Encrypt with DES</button>
        </form>
        
        <div class="challenge">
            <h4>💡 Challenge:</h4>
            <p>DES is extremely weak! Try decrypting this secret: <code>4P7K+urL5eA=</code></p>
        </div>
        '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/decrypt_des', methods=['GET', 'POST'])
def decrypt_des():
    if request.method == 'POST':
        encrypted_b64 = request.form.get('encrypted', '')
        
        try:
            encrypted = base64.b64decode(encrypted_b64)
            des_cipher = DES.new(WEAK_DES_KEY, DES.MODE_ECB)
            decrypted_padded = des_cipher.decrypt(encrypted)
            decrypted = unpad(decrypted_padded, 8).decode()
            
            if 'flag' in decrypted.lower():
                flag = os.getenv('FLAG_A02', 'CTF{cr4pt0_f41lur3_3xp0s3d_2024}')
                result = f'''
                <div class="result flag">
                    <h3>🎉 Flag Captured!</h3>
                    <p><strong>Decrypted:</strong> {decrypted}</p>
                    <p><strong>FLAG:</strong> {flag}</p>
                </div>
                '''
            else:
                result = f'''
                <div class="result">
                    <p><strong>Decrypted:</strong> {decrypted}</p>
                </div>
                '''
        except Exception as e:
            result = f'<div class="result error"><p>Decryption failed: {str(e)}</p></div>'
        
        content = f'''
        <h2>🔓 DES Decryption Tool</h2>
        <form method="POST">
            <label>Enter Encrypted Text (Base64):</label><br>
            <input type="text" name="encrypted" value="{encrypted_b64}" required><br>
            <button type="submit">Decrypt</button>
        </form>
        {result}
        '''
    else:
        content = '''
        <h2>🔓 DES Decryption Tool</h2>
        <form method="POST">
            <label>Enter Encrypted Text (Base64):</label><br>
            <input type="text" name="encrypted" required><br>
            <button type="submit">Decrypt</button>
        </form>
        
        <div class="challenge">
            <h4>💡 Hint:</h4>
            <p>The DES key is: <code>WEAK1234</code></p>
        </div>
        '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/ecb_mode', methods=['GET', 'POST'])
def ecb_mode():
    if request.method == 'POST':
        plaintext = request.form.get('plaintext', '')
        
        # AES ECB mode (vulnerable to pattern attacks)
        aes_cipher = AES.new(WEAK_AES_KEY, AES.MODE_ECB)
        
        # Pad the plaintext to be a multiple of 16 bytes
        padded_text = pad(plaintext.encode(), 16)
        encrypted = aes_cipher.encrypt(padded_text)
        encrypted_hex = encrypted.hex()
        
        content = f'''
        <h2>🔄 ECB Mode Challenge</h2>
        <form method="POST">
            <label>Enter Text to Encrypt:</label><br>
            <textarea name="plaintext" required>{plaintext}</textarea><br>
            <button type="submit">Encrypt with AES-ECB</button>
        </form>
        
        <div class="result">
            <p><strong>Original:</strong> {plaintext}</p>
            <p><strong>AES-ECB Encrypted (Hex):</strong> {encrypted_hex}</p>
        </div>
        
        <div class="challenge">
            <h4>💡 ECB Mode Weakness:</h4>
            <p>Try encrypting repeated patterns like: <code>AAAAAAAAAAAAAAAA</code></p>
            <p>Notice how identical blocks produce identical ciphertext!</p>
        </div>
        '''
    else:
        content = '''
        <h2>🔄 ECB Mode Challenge</h2>
        <form method="POST">
            <label>Enter Text to Encrypt:</label><br>
            <textarea name="plaintext" required></textarea><br>
            <button type="submit">Encrypt with AES-ECB</button>
        </form>
        
        <div class="challenge">
            <h4>💡 ECB Mode Weakness:</h4>
            <p>Try encrypting repeated patterns like: <code>AAAAAAAAAAAAAAAA</code></p>
            <p>Notice how identical blocks produce identical ciphertext!</p>
        </div>
        '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/predictable_tokens')
def predictable_tokens():
    # Generate predictable tokens based on time
    timestamp = int(time.time())
    predictable_token = hashlib.md5(f"token_{timestamp}".encode()).hexdigest()
    
    # Simple token that increments
    session_counter = session.get('counter', 0) + 1
    session['counter'] = session_counter
    simple_token = f"token_{session_counter:06d}"
    
    content = f'''
    <h2>🎲 Predictable Token Challenge</h2>
    
    <div class="crypto-box">
        <h4>Time-based Token:</h4>
        <p><strong>Token:</strong> {predictable_token}</p>
        <p><strong>Generation Time:</strong> {timestamp}</p>
        <p><strong>Algorithm:</strong> MD5(token_{timestamp})</p>
    </div>
    
    <div class="crypto-box">
        <h4>Sequential Token:</h4>
        <p><strong>Token:</strong> {simple_token}</p>
        <p><strong>Pattern:</strong> token_XXXXXX (6-digit counter)</p>
    </div>
    
    <div class="challenge">
        <h4>💡 Challenge:</h4>
        <p>Can you predict the next token? Refresh the page to see new tokens!</p>
        <p>Time-based tokens are vulnerable to timing attacks.</p>
        <p>Sequential tokens can be easily enumerated.</p>
    </div>
    
    <div class="result flag">
        <p><strong>FLAG:</strong> CTF{pr3d1ct4bl3_t0k3ns_4r3_w34k_2024}</p>
    </div>
    '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/weak_random')
def weak_random():
    # Weak random number generation
    import random
    
    # Seed with current time (predictable)
    random.seed(int(time.time()))
    weak_random = random.randint(1000, 9999)
    
    # Better random (but still showing the weakness)
    secure_random = secrets.randbelow(10000)
    
    content = f'''
    <h2>🎯 Weak Random Generation</h2>
    
    <div class="crypto-box">
        <h4>Weak Random (time-seeded):</h4>
        <p><strong>Value:</strong> {weak_random}</p>
        <p><strong>Seed:</strong> {int(time.time())}</p>
        <p>Generated using: <code>random.seed(time.time())</code></p>
    </div>
    
    <div class="crypto-box">
        <h4>Secure Random:</h4>
        <p><strong>Value:</strong> {secure_random}</p>
        <p>Generated using: <code>secrets.randbelow()</code></p>
    </div>
    
    <div class="challenge">
        <h4>💡 Weakness:</h4>
        <p>The weak random number can be predicted if you know the time!</p>
        <p>Never use time-based seeds for security-critical randomness.</p>
    </div>
    
    <div class="result flag">
        <p><strong>FLAG:</strong> CTF{w34k_r4nd0m_1s_pr3d1ct4bl3_2024}</p>
    </div>
    '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/hardcoded_secrets')
def hardcoded_secrets():
    # Read hardcoded secrets from files
    try:
        with open('/app/data/encryption_key.txt', 'r') as f:
            encryption_key = f.read().strip()
    except:
        encryption_key = 'secret_key_12345'
    
    try:
        with open('/app/data/secret_flag.txt', 'r') as f:
            secret_flag = f.read().strip()
    except:
        secret_flag = os.getenv('FLAG_A02', 'CTF{cr4pt0_f41lur3_3xp0s3d_2024}')
    
    content = f'''
    <h2>🔑 Hardcoded Secrets Challenge</h2>
    
    <div class="crypto-box">
        <h4>Application Source Code:</h4>
        <pre># Hardcoded encryption key (NEVER DO THIS!)
ENCRYPTION_KEY = "secret_key_12345"

# Hardcoded database password
DB_PASSWORD = "super_secret_db_pass_123"

# Hardcoded API key
API_KEY = "sk-1234567890abcdef"</pre>
    </div>
    
    <div class="crypto-box">
        <h4>Configuration Files:</h4>
        <p><strong>Encryption Key:</strong> {encryption_key}</p>
        <p><strong>File:</strong> /app/data/encryption_key.txt</p>
    </div>
    
    <div class="challenge">
        <h4>💡 Challenge:</h4>
        <p>Hardcoded secrets are easily discoverable in:</p>
        <ul>
            <li>Source code repositories</li>
            <li>Configuration files</li>
            <li>Environment variables</li>
            <li>Database dumps</li>
        </ul>
    </div>
    
    <div class="result flag">
        <h3>🎉 Secret Found!</h3>
        <p><strong>FLAG:</strong> {secret_flag}</p>
    </div>
    '''
    
    return render_template_string(BASE_TEMPLATE, content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True) 