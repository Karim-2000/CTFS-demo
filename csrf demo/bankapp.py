from flask import Flask, request, render_template_string, session, make_response
from flask_wtf.csrf import CSRFProtect
import secrets
import time

app = Flask(__name__)
app.secret_key = 'your-secret-key'
csrf = CSRFProtect(app)

# Separate databases for vulnerable and protected versions
vulnerable_users = {
    'alice': {'balance': 1000},
    'bob': {'balance': 500}
}

protected_users = {
    'alice': {'balance': 1000},
    'bob': {'balance': 500}
}

transaction_log = []

VULNERABLE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Bank (Vulnerable)</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        .balance { font-size: 24px; color: green; margin: 20px 0; }
        .warning { 
            background: #ffebee; 
            padding: 10px; 
            border-radius: 5px; 
            margin-bottom: 20px;
            border: 1px solid #ef9a9a;
        }
        .log { 
            background: #f5f5f5; 
            padding: 10px; 
            margin-top: 20px;
            border-radius: 5px;
        }
        .log-entry {
            margin: 5px 0;
            padding: 5px;
            border-bottom: 1px solid #ddd;
        }
        .success { color: green; }
        .error { color: red; }
    </style>
</head>
<body>
    <div class="warning">
        <strong>⚠️ VULNERABLE VERSION</strong>
        <p>This version has no CSRF protection and uses a separate balance from the protected version.</p>
        <p>Current version balance is tracked independently.</p>
    </div>
    
    <h1>Welcome {{ username }}</h1>
    <div class="balance">Your Balance: ${{ balance }}</div>
    
    <h3>Transfer Money</h3>
    <form method="POST" action="/vulnerable/transfer">
        To: <input type="text" name="to" required><br><br>
        Amount: $<input type="number" name="amount" required><br><br>
        <button type="submit">Transfer</button>
    </form>

    {% if message %}
        <p style="color: {% if success %}green{% else %}red{% endif %}">
            {{ message }}
        </p>
    {% endif %}
    
    <div class="log">
        <h3>Transaction Log:</h3>
        {% for entry in log %}
            <div class="log-entry {% if entry.success %}success{% else %}error{% endif %}">
                {{ entry.time }} - {{ entry.message }}
            </div>
        {% endfor %}
    </div>
    
    <p>
        <a href="/logout">Logout</a> | 
        <a href="/protected">Switch to Protected Version</a>
    </p>
</body>
</html>
'''

PROTECTED_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Bank (Protected)</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        .balance { font-size: 24px; color: green; margin: 20px 0; }
        .protected { 
            background: #e8f5e9; 
            padding: 10px; 
            border-radius: 5px; 
            margin-bottom: 20px;
            border: 1px solid #a5d6a7;
        }
        .log { 
            background: #f5f5f5; 
            padding: 10px; 
            margin-top: 20px;
            border-radius: 5px;
        }
        .log-entry {
            margin: 5px 0;
            padding: 5px;
            border-bottom: 1px solid #ddd;
        }
        .success { color: green; }
        .error { color: red; }
    </style>
</head>
<body>
    <div class="protected">
        <strong>✅ PROTECTED VERSION</strong>
        <p>This version has CSRF protection and uses a separate balance from the vulnerable version.</p>
        <p>Current version balance is tracked independently.</p>
    </div>
    
    <h1>Welcome {{ username }}</h1>
    <div class="balance">Your Balance: ${{ balance }}</div>
    
    <h3>Transfer Money</h3>
    <form method="POST" action="/protected/transfer">
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
    
    <div class="log">
        <h3>Transaction Log:</h3>
        {% for entry in log %}
            <div class="log-entry {% if entry.success %}success{% else %}error{% endif %}">
                {{ entry.time }} - {{ entry.message }}
            </div>
        {% endfor %}
    </div>
    
    <p>
        <a href="/logout">Logout</a> | 
        <a href="/vulnerable">Switch to Vulnerable Version</a>
    </p>
</body>
</html>
'''

@app.route('/vulnerable')
def vulnerable():
    if 'username' not in session:
        return 'Please <a href="/login/alice">login as Alice</a> or <a href="/login/bob">login as Bob</a>'
    
    username = session['username']
    return render_template_string(
        VULNERABLE_TEMPLATE,
        username=username,
        balance=vulnerable_users[username]['balance'],
        message=session.pop('message', None),
        success=session.pop('success', False),
        log=transaction_log
    )

@app.route('/protected')
def protected():
    if 'username' not in session:
        return 'Please <a href="/login/alice">login as Alice</a> or <a href="/login/bob">login as Bob</a>'
    
    username = session['username']
    return render_template_string(
        PROTECTED_TEMPLATE,
        username=username,
        balance=protected_users[username]['balance'],
        message=session.pop('message', None),
        success=session.pop('success', False),
        log=transaction_log
    )

@app.route('/vulnerable/transfer', methods=['POST'])
@csrf.exempt
def vulnerable_transfer():
    if 'username' not in session:
        transaction_log.append({
            'time': time.strftime('%H:%M:%S'),
            'message': '[Vulnerable] Transfer failed: Not logged in',
            'success': False
        })
        return 'Not logged in', 401
    
    from_user = session['username']
    to_user = request.form.get('to')
    amount = int(request.form.get('amount', 0))
    
    if to_user in vulnerable_users and amount > 0:
        if vulnerable_users[from_user]['balance'] >= amount:
            vulnerable_users[from_user]['balance'] -= amount
            vulnerable_users[to_user]['balance'] += amount
            message = f'[Vulnerable] Transferred ${amount} to {to_user}'
            success = True
        else:
            message = '[Vulnerable] Insufficient funds'
            success = False
    else:
        message = '[Vulnerable] Invalid transfer'
        success = False
    
    transaction_log.append({
        'time': time.strftime('%H:%M:%S'),
        'message': message,
        'success': success
    })
    
    session['message'] = message
    session['success'] = success
    return make_response('', 302, {'Location': '/vulnerable'})

@app.route('/protected/transfer', methods=['POST'])
def protected_transfer():
    if 'username' not in session:
        transaction_log.append({
            'time': time.strftime('%H:%M:%S'),
            'message': '[Protected] Transfer failed: Not logged in',
            'success': False
        })
        return 'Not logged in', 401
    
    from_user = session['username']
    to_user = request.form.get('to')
    amount = int(request.form.get('amount', 0))
    
    if to_user in protected_users and amount > 0:
        if protected_users[from_user]['balance'] >= amount:
            protected_users[from_user]['balance'] -= amount
            protected_users[to_user]['balance'] += amount
            message = f'[Protected] Transferred ${amount} to {to_user}'
            success = True
        else:
            message = '[Protected] Insufficient funds'
            success = False
    else:
        message = '[Protected] Invalid transfer'
        success = False
    
    transaction_log.append({
        'time': time.strftime('%H:%M:%S'),
        'message': message,
        'success': success
    })
    
    session['message'] = message
    session['success'] = success
    return make_response('', 302, {'Location': '/protected'})

@app.route('/')
def home():
    return '''
        <h1>Bank Security Demo</h1>
        <p>This demo shows CSRF vulnerability by maintaining separate balances for protected and vulnerable versions.</p>
        <p>Choose a version to test:</p>
        <ul>
            <li><a href="/vulnerable">Vulnerable Version</a> (No CSRF Protection)</li>
            <li><a href="/protected">Protected Version</a> (With CSRF Protection)</li>
        </ul>
    '''

@app.route('/login/<username>')
def login(username):
    if username in vulnerable_users:  # or protected_users, they have same usernames
        session['username'] = username
        transaction_log.append({
            'time': time.strftime('%H:%M:%S'),
            'message': f'{username} logged in',
            'success': True
        })
        return f'''
            Logged in as {username}.<br>
            Choose version:<br>
            <a href="/vulnerable">Go to Vulnerable Version</a><br>
            <a href="/protected">Go to Protected Version</a>
        '''
    return 'User not found'

@app.route('/logout')
def logout():
    if 'username' in session:
        transaction_log.append({
            'time': time.strftime('%H:%M:%S'),
            'message': f'{session["username"]} logged out',
            'success': True
        })
    session.clear()
    return 'Logged out. <a href="/">Home</a>'

if __name__ == '__main__':
    app.run(debug=True, port=5000)