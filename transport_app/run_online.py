from pyngrok import ngrok
import subprocess
import time
import os

# Set your ngrok auth token if you have one (optional but recommended for persistent tunnels)
# ngrok.set_auth_token("YOUR_AUTH_TOKEN")

# Start the Flask app in the background
print("Starting Flask app...")
flask_process = subprocess.Popen(['python', 'app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait a bit for the app to start
time.sleep(5)

# Create a tunnel to the Flask app
print("Creating ngrok tunnel...")
tunnel = ngrok.connect(5000, "http")
print(f"App is now accessible at: {tunnel.public_url}")

# Keep the script running
try:
    flask_process.wait()
except KeyboardInterrupt:
    print("Shutting down...")
    ngrok.kill()
    flask_process.terminate()
