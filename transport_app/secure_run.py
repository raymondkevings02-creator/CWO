#!/usr/bin/env python3
"""
Secure Flask App Runner with HTTPS and Authentication
"""
import os
import ssl
import subprocess
from flask import Flask
from werkzeug.serving import make_ssl_devcert
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_ssl_cert():
    """Create self-signed SSL certificate for development"""
    cert_file = 'cert.pem.crt'
    key_file = 'cert.pem.key'

    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        print("Creating SSL certificate...")
        make_ssl_devcert('cert.pem.crt', host='localhost')
        print("SSL certificate created.")

    return cert_file, key_file

def run_secure_app():
    """Run the Flask app with SSL and security headers"""
    print("Starting secure Flask app...")

    # Create SSL context
    cert_file, key_file = create_ssl_cert()
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(cert_file, key_file)

    # Run with SSL
    print("App running with HTTPS on https://localhost:5000")
    print("Press Ctrl+C to stop")

    # Use socketio.run to run the app with SSL
    from app import app, socketio

    print("Starting secure Flask app with SocketIO...")

    try:
        socketio.run(
            app,
            host='0.0.0.0',
            port=5000,
            ssl_context=ssl_context,
            debug=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\nShutting down securely...")

if __name__ == "__main__":
    run_secure_app()
