import webview
import os
from flask import Flask, render_template
from tkinter import filedialog
import json
import csv
import subprocess

class GCSBackend:
    def __init__(self):
        # Initialize waypoints as an empty list
        self.waypoints = []
        
    def connect_robot(self):
        script_path = "tb3_nav2/a"
        try:
            result = subprocess.run(
                [script_path],  # Do not prefix with 'bash' if it’s an executable
                text=True,
                capture_output=True,
                check=True
            )
            return f"Script output: {result.stdout.strip()}"
        except subprocess.CalledProcessError as e:
            print("Error:", e)
            return f"Error: {e.stderr.strip()}"
        except Exception as e:
            print("Error:", e)
            return f"Unexpected error: {e}"
        

    
    def disconnect_robot(self):
                try:
                    # Example: Replace 'echo "Connected!"' with your desired bash command
                    result = subprocess.run(
                        ['echo', 'Connected!'],
                        text=True,
                        capture_output=True,
                        check=True
                    )
                    print("Bash output:", result.stdout.strip())  # Log the output for debugging
                    return f"Bash output: {result.stdout.strip()}"
                except subprocess.CalledProcessError as e:
                    print("Error:", e)
                    return f"Error: {e}"
                
    def load_csv(self):
        import csv
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")],
            title="Select CSV File"
        )
        if file_path:
            waypoints = []
            try:
                with open(file_path, "r") as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        latitude = float(row["latitude"])
                        longitude = float(row["longitude"])
                        waypoints.append([latitude, longitude])  # Ensure this is a list, not a tuple
                print("Parsed Waypoints:", waypoints)
                return json.dumps(waypoints)  # Serialize as JSON
            except Exception as e:
                print(f"Error loading CSV: {e}")
                return json.dumps([])  # Return an empty list if parsing fails
        else:
            return json.dumps([])  # Return an empty list if no file selected

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
