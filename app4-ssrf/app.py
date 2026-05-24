#!/usr/bin/env python3
"""
OWASP Top 10 - A10: Server-Side Request Forgery (SSRF)
This application demonstrates SSRF vulnerabilities for educational purposes.
"""

import os
import requests
import subprocess
import urllib.parse
from flask import Flask, render_template_string, request, jsonify
import logging
import json

app = Flask(__name__)
app.secret_key = 'ssrf_vulnerable_secret_2025'

# Configure logging
logging.basicConfig(level=logging.INFO)


def is_safe_url(target_url):
    """
    Validate URL before server-side request.
    Return True only if URL is allowed to be fetched.
    """

    try:
        parsed = urllib.parse.urlparse(target_url)

        # Only allow http/https
        if parsed.scheme not in ["http", "https"]:
            return False, "Only HTTP and HTTPS schemes are allowed"

        hostname = parsed.hostname
        if not hostname:
            return False, "Missing hostname"

        # Block internal hostname via service Docker name
        blocked_hostnames = {
            "flag-server",
            "localhost",
            "127.0.0.1",
            "0.0.0.0"
        }

        if hostname in blocked_hostnames:
            return False, "Internal hostname is not allowed"

        # Resolve hostname to IP for blocking private/internal IP
        ip = socket.gethostbyname(hostname)
        ip_obj = ipaddress.ip_address(ip)

        if (
            ip_obj.is_private
            or ip_obj.is_loopback
            or ip_obj.is_link_local
            or ip_obj.is_multicast
            or ip_obj.is_reserved
        ):
            return False, "Internal or private IP address is not allowed"

        return True, "URL is allowed"

    except Exception as e:
        return False, f"Invalid URL: {str(e)}"

# HTML Template
BASE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>SSRF Proxy Challenge - OWASP A10</title>
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
        pre { background: #f8f9fa; padding: 10px; border-radius: 3px; overflow-x: auto; max-height: 300px; overflow-y: auto; }
        .url-box { background: #e9ecef; padding: 15px; border-radius: 5px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 Server-Side Request Forgery (SSRF) Proxy Challenge</h1>
        <div class="challenge warning">
            <h3>⚠️ Educational Purpose Only</h3>
            <p>This application contains intentional SSRF vulnerabilities. Exploit the proxy to capture flags!</p>
        </div>
        
        {{ content | safe }}
        
        <div style="margin-top: 30px; padding: 15px; background: #e9ecef; border-radius: 5px;">
            <h3>🎯 Navigation:</h3>
            <ul>
                <li><a href="./">Home</a></li>
                <li><a href="./proxy">Web Proxy</a></li>
            </ul>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    content = '''
    <h2>Welcome to the SSRF Proxy Security Lab</h2>
    <p>This application demonstrates Server-Side Request Forgery vulnerabilities through a web proxy service.</p>
    
    <div class="challenge">
        <h3>Your Mission:</h3>
        <ul>
            <li>Exploit the web proxy to perform SSRF attacks</li>
            <li>Bypass URL filters and access internal services</li>
            <li>Use custom headers to access protected endpoints</li>
            <li>Capture flags in the format: <code>CTF{...}</code></li>
        </ul>
    </div>
    
    <div class="challenge">
        <h3>Common SSRF Targets:</h3>
        <ul>
            <li><strong>Localhost services:</strong> <code>http://localhost:PORT/</code></li>
            <li><strong>Internal networks:</strong> <code>http://192.168.1.1/</code></li>
            <li><strong>Cloud metadata:</strong> <code>http://169.254.169.254/</code></li>
            <li><strong>Docker services:</strong> <code>http://flag-server:8080/</code></li>
        </ul>
    </div>
    
    
    <div class="challenge">
        <h3>🚀 Get Started:</h3>
        <p><a href="./proxy" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Launch Web Proxy Challenge</a></p>
    </div>
    '''
    return render_template_string(BASE_TEMPLATE, content=content)


@app.route('/proxy', methods=['GET', 'POST'])
def web_proxy():
    if request.method == 'POST':
        target_url = request.form.get('target_url', '').strip()
        custom_headers = request.form.get('custom_headers', '').strip()
        
        if not target_url:
            result = '<div class="result error"><p>Please provide a target URL!</p></div>'
        else:
            try:
                # Parse custom headers
                headers = {'User-Agent': 'SSRF-Proxy/1.0'}
                if custom_headers:
                    for line in custom_headers.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            headers[key.strip()] = value.strip()
                
                is_allowed, reason = is_safe_url(target_url)

                if not is_allowed:
                    content = f'''
                    <h2>🌐 URL Proxy</h2>
                    <div class="result error">
                        <h3>Request Blocked</h3>
                        <p><strong>Reason:</strong> {reason}</p>
                        <p><strong>Blocked URL:</strong> {target_url}</p>
                    </div>
                    '''
                    return render_template_string(BASE_TEMPLATE, content=content)

                response = requests.get(target_url, headers=headers, timeout=15)
                
                result = f'''
                <div class="result">
                    <h4>Proxied Response from: {target_url}</h4>
                    <p><strong>Status:</strong> {response.status_code}</p>
                    <p><strong>Content-Type:</strong> {response.headers.get('Content-Type', 'Unknown')}</p>
                    <p><strong>Response Headers:</strong></p>
                    <pre>{json.dumps(dict(response.headers), indent=2)}</pre>
                    <p><strong>Content:</strong></p>
                    <pre>{response.text[:1500]}{'...' if len(response.text) > 1500 else ''}</pre>
                </div>
                '''
                
                if 'CTF{' in response.text:
                    result += '''
                    <div class="result flag">
                        <h3>🎉 Flag Captured!</h3>
                        <p>Your proxy request found a flag!</p>
                    </div>
                    '''
                
            except Exception as e:
                result = f'<div class="result error"><p>Proxy error: {str(e)}</p></div>'
        
        content = f'''
        <h2>🔄 Web Proxy (SSRF Challenge)</h2>
        <p>This proxy service can fetch URLs with custom headers.</p>
        
        <form method="POST">
            <label>Target URL:</label><br>
            <input type="text" name="target_url" value="{target_url}" placeholder="http://internal-service/" required><br>
            <label>Custom Headers (one per line, format: Header: Value):</label><br>
            <textarea name="custom_headers" rows="4" placeholder="Authorization: Bearer token123">{custom_headers}</textarea><br>
            <button type="submit">Proxy Request</button>
        </form>
        {result}
        '''
    else:
        content = '''
        <h2>🔄 Web Proxy (SSRF Challenge)</h2>
        <p>This proxy service can fetch URLs with custom headers.</p>
        
        <form method="POST">
            <label>Target URL:</label><br>
            <input type="text" name="target_url" placeholder="http://internal-service/" required><br>
            <label>Custom Headers (one per line, format: Header: Value):</label><br>
            <textarea name="custom_headers" rows="4" placeholder="Authorization: Bearer token123"></textarea><br>
            <button type="submit">Proxy Request</button>
        </form>
        '''
    
    content += '''
    <div class="challenge">
        <h4>💡 SSRF Attack Techniques:</h4>
        <ul>
            <li>Add authentication headers to access protected endpoints</li>
            <li>Try localhost variations: <code>127.0.0.1</code>, <code>[::1]</code></li>
            <li>Target internal Docker services by hostname</li>
        </ul>
    </div>
    '''
    
    return render_template_string(BASE_TEMPLATE, content=content)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True) 
