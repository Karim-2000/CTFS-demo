from flask import Flask, request, render_template_string, session, make_response
from flask_wtf.csrf import CSRFProtect
import secrets

app = Flask(__name__)
app.secret_key = 'your-secret-key'
csrf = CSRFProtect(app)  # Enable CSRF protection

# [Previous user database code remains the same]
users = {
    'alice': {'balance': 1000},
    'bob': {'balance': 500}
}

# Updated template with CSRF token
BANK_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>My Bank (Protected)</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        .balance { font-size: 24px; color: green; margin: 20px 0; }
        .protected { background: #e8f5e9; padding: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="protected">✅ This page is protected against CSRF attacks</div>
    
    <h1>Welcome {{ username }}</h1>
    <div class="balance">Your Balance: ${{ balance }}</div>
    
    <h3>Transfer Money</h3>
    <form method="POST" action="/transfer">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
        To: <input type="text" name="to" required><br><br>
        Amount: $<input type="number" name="amount" required><br><br>
        <button type="submit">Transfer</button>
    </form>

    {% if message %}
        <p style="color: {% if success %}green{% else %}red{% endif %}">
            {{ message }}
        </p>
    {% endif %}
</body>
</html>
'''

# [Previous route code remains largely the same]
# The CSRF protection is automatically applied to all POST requests

if __name__ == '__main__':
    app.run(debug=True, port=5000)