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
        self.Shared_Path = os.getcwd()

    def connect_robot(self):
        print('Robot Connected')
        script_path = self.Shared_Path + "/GCS/resources/bashfiles/simulation"
        try:
            result = subprocess.run(
                [script_path],  # Do not prefix with 'bash' if it’s an executable
                text=True,
                capture_output=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print("Error:", e)
            return False
        except Exception as e:
            print("Error:", e)
            return False
    
    def disconnect_robot(self):
        print("Python: disconnecting robot...")
        script_path = self.Shared_Path + "/GCS/resources/bashfiles/disconect"
        try:
            result = subprocess.run(
            [script_path],
            text=True,
            capture_output=True,
            check=True
        )
            return "Robot disconnected successfully!"
        except subprocess.CalledProcessError as e:
            print("Error:", e)
            return False
        except Exception as e:
            print("Error:", e)
            return False
                
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

    def export_temporary_waypoints(self):
        if not self.waypoints:
            print("No waypoints to export!")
            return "No waypoints to export!"
        else:
            # Open save dialog to select path and filename
            file_path = self.Shared_Path + "/GCS/resources/temporary.csv"
            
            with open(file_path, mode="w+", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["latitude", "longitude"])  # CSV header
                writer.writerows(self.waypoints)  # Write the waypoints
            print(f"Waypoints exported to {file_path}")
            file.close()
            return f"Waypoints exported successfully to {file_path}!"
        
    def send_waypoints(self):
        print("Python: Sending waypoints to the robot...")
        self.export_temporary_waypoints()
        script_path = self.Shared_Path + "/GCS/resources/bashfiles/follower"
        try:
            print("Python: 1...")
            result = subprocess.run(
                [script_path],
                text=True,
                capture_output=True,
                check=True
            )
            return "Waypoints sent successfully!"
        except subprocess.CalledProcessError as e:
            print("Python: 2...")
            print("Error:", e)
            return False
        except Exception as e:
            print("Python: 3...")
            print("Error:", e)
            return False
        

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
