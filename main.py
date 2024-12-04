import webview
import os
from flask import Flask, render_template
from tkinter import filedialog

class GCSBackend:
    def connect_robot(self):
        print("Python: Connecting to robot...")
        return "Connected to robot!"

    def load_csv(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")],
            title="Select CSV File"
        )
        if file_path:
            return f"Loaded CSV from {file_path}"
        else:
            return "Nothing Loaded!"


    def send_waypoints(self):
        print("Python: Sending waypoints to the robot...")
        return "Waypoints sent successfully!"

    def exit_app(self):
        print("Python: Exiting application...")
        os._exit(0)  # Hard exit to ensure the app closes

# Flask App to serve the HTML
app = Flask(__name__, template_folder="resources")

@app.route("/")
def map_view():
    return render_template("map.html")

# Main Script
if __name__ == "__main__":
    backend = GCSBackend()
    # Create pywebview window
    window = webview.create_window(
        "Ground Control Station",
        app,
        js_api=backend,
        width=1200,
        height=800,
        resizable=True
    )
    # Start Flask and pywebview
    webview.start(debug=False)
