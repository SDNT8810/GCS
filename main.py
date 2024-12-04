import webview
import os
from flask import Flask, render_template
from tkinter import filedialog
import json
import csv

class GCSBackend:
    def __init__(self):
        # Initialize waypoints as an empty list
        self.waypoints = []

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

    def add_waypoint(self, latitude, longitude):
        self.waypoints.append((latitude, longitude))
        print(f"Waypoint added: ({latitude}, {longitude})")
        return f"Waypoint added successfully: ({latitude}, {longitude})"

    def export_waypoints(self):
        if not self.waypoints:
            print("No waypoints to export!")
            return "No waypoints to export!"

        # Open save dialog to select path and filename
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save Waypoints As"
        )
        if not file_path:
            return "Export canceled by user."

        # Write waypoints to the CSV file
        try:
            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["latitude", "longitude"])  # CSV header
                writer.writerows(self.waypoints)  # Write the waypoints
            print(f"Waypoints exported to {file_path}")
            return f"Waypoints exported successfully to {file_path}!"
        except Exception as e:
            print(f"Error exporting waypoints: {e}")
            return f"Error exporting waypoints: {e}"
    
    def clear_waypoints(self):
        # Clear all waypoints
        self.waypoints = []
        print("All waypoints cleared.")
        return "All waypoints cleared."

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
        height=600,
        resizable=True
    )
    # Start Flask and pywebview
    webview.start(debug=False)
