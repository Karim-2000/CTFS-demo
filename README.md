# CTFS-demo
# CSRF Attack and Protection Demonstration

This project demonstrates Cross-Site Request Forgery (CSRF) attacks and protection mechanisms through a simple banking application. It includes both vulnerable and protected versions of the same functionality, allowing users to understand how CSRF attacks work and how to prevent them.

## Project Overview

The demonstration consists of three main components:

1. A Flask-based banking application (`bankapp.py`)
   - Implements basic money transfer functionality
   - Maintains separate protected and vulnerable versions
   - Includes comprehensive transaction logging

2. A simulated malicious website (`evilsite.html`)
   - Demonstrates how CSRF attacks can be executed
   - Shows social engineering techniques
   - Includes hidden form submission

3. A demonstration interface that allows users to:
   - Switch between protected and vulnerable versions
   - View transaction logs in real-time
   - Understand the differences in implementation

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Basic understanding of web security concepts
- Modern web browser with developer tools

### Installation

1. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

2. Install required packages:
```bash
pip install flask flask-wtf
```

3. Set environment variables:
```bash
# On Windows:
set FLASK_APP=bankapp.py
set FLASK_ENV=development

# On Unix or MacOS:
export FLASK_APP=bankapp.py
export FLASK_ENV=development
```

### Running the Demonstration

1. Start the Flask application:
```bash
flask run
```

2. Access the application:
   - Main interface: http://localhost:5000
   - Vulnerable version: http://localhost:5000/vulnerable
   - Protected version: http://localhost:5000/protected

3. Login credentials:
   - Username: alice (balance: $1000)
   - Username: bob (balance: $500)

## Using the Demonstration

1. Start by logging in as Alice in one browser window
2. Access the vulnerable version and note the balance
3. Open the evil site in another browser window
4. Observe how the CSRF attack can transfer money without user consent
5. Repeat the process with the protected version to see how CSRF tokens prevent the attack

## Security Notes

This demonstration intentionally includes vulnerable code for educational purposes. Do not use the vulnerable version in any production environment. The protected version demonstrates security best practices for preventing CSRF attacks.

## Project Structure

```
csrf-demo/
├── bankapp.py          # Main Flask application
├── evilsite.html       # Simulated malicious website
└── README.md          # This file
```

## Educational Resources

For more information about CSRF attacks and protection:
- OWASP CSRF Prevention Cheat Sheet
- Flask-WTF Documentation
- Python Web Security Best Practices

## Contributing

This is an educational project. If you find bugs or have suggestions for improving the demonstration, please feel free to open an issue or submit a pull request.

## License

This project is provided for educational purposes under the MIT License. See the LICENSE file for details.
