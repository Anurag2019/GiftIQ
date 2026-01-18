#!/usr/bin/env python
"""
GiftIQ Global Runner
Starts both Flask API and Streamlit UI simultaneously
"""

import subprocess
import sys
import time
import os
import warnings
from pathlib import Path
# Suppress warnings
warnings.filterwarnings('ignore')

processes = []

def run_flask_app():
    """Start Flask API server"""
    print("🚀 Starting Flask API server...")
    api_path = Path(__file__).parent / "api"
    try:
        # Start Flask and display output in real-time
        process = subprocess.Popen(
            ["python3", "-W","ignore","app.py"],
            cwd=str(api_path)
        )
        processes.append(process)
        print("✓ Flask API server started on http://localhost:5000")
        return process
    except Exception as e:
        print(f"❌ Error starting Flask app: {e}")
        sys.exit(1)


def run_streamlit_app():
    """Start Streamlit UI"""
    print("🎨 Starting Streamlit UI...")
    ui_path = Path(__file__).parent
    try:
        # Start Streamlit and display output in real-time
        process = subprocess.Popen(
            ["python3", "-m", "streamlit", "run", "app.py", "--logger.level=warning"],
            cwd=str(ui_path)
        )
        processes.append(process)
        print("✓ Streamlit UI started on http://localhost:8501")
        return process
    except Exception as e:
        print(f"❌ Error starting Streamlit app: {e}")
        sys.exit(1)


def cleanup():
    """Clean up all processes"""
    print("\n🛑 Shutting down all services...")
    for process in processes:
        try:
            process.terminate()
            process.wait(timeout=2000)
        except:
            try:
                process.kill()
            except:
                pass


def main():
    """Main entry point"""
    print("=" * 60)
    print("🎁 GiftIQ - Starting All Services")
    print("=" * 60)
    print()
    
    # Start Flask API first
    flask_process = run_flask_app()
    
    # Wait for Flask to start
    time.sleep(3)
    
    # Check if Flask started successfully
    if flask_process.poll() is not None:
        print("❌ Flask failed to start. Check error message above.")
        print("   Make sure you have flask and dependencies installed.")
        print("   Run: pip install -r requirements.txt")
        cleanup()
        sys.exit(1)
    
    # Start Streamlit UI
    streamlit_process = run_streamlit_app()
    
    print()
    print("=" * 60)
    print("✓ All services are running!")
    print("=" * 60)
    print()
    print("📍 API Server:   http://localhost:5000")
    print("📍 Streamlit UI: http://localhost:8501")
    print()
    print("Press Ctrl+C to stop all services")
    print()
    
    try:
        # Keep the script running and monitor processes
        while True:
            # Check if processes are still alive
            flask_status = flask_process.poll()
            streamlit_status = streamlit_process.poll()
            
            if flask_status is not None:
                print("⚠️  Flask process exited. Check the error output above.")
                cleanup()
                sys.exit(1)
            
            if streamlit_status is not None:
                print("⚠️  Streamlit process exited. Check the error output above.")
                cleanup()
                sys.exit(1)
            
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup()
        print("✓ All services stopped successfully")
        sys.exit(0)


if __name__ == "__main__":
    main()



if __name__ == "__main__":
    main()
