import webview
import folium
from pathlib import Path
from tkinter import filedialog, messagebox

class SimpleGCS:
    def __init__(self):
        # Generate the interactive map with buttons
        self.map_path = self.generate_map_with_buttons()

        # Open the map with the buttons in a webview window
        self.window = webview.create_window("Simple GCS", self.map_path)

    def generate_map_with_buttons(self):
        # Create a map using folium
        map_path = Path("resources/map_with_buttons.html")
        map_path.parent.mkdir(exist_ok=True)
        m = folium.Map(location=[45.4642, 9.1900], zoom_start=12)  # Centered at Milan, Italy
        m.save(str(map_path))

        # Add the buttons to the map HTML file
        with open(map_path, "a") as map_file:
            map_file.write("""
                <br>
                <div style="position: fixed; top: 10px; right: 10px; display: flex; flex-direction: row; gap: 10px; z-index: 9999;">
                    <button onclick="connectRobot()" style="
                        padding: 10px 20px;
                        font-size: 16px;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
                    ">Connect</button>

                    <button onclick="sendWaypoints()" style="
                        padding: 10px 20px;
                        font-size: 16px;
                        background-color: #2196F3;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
                    ">Send Waypoints</button>

                    <button onclick="loadCSV()" style="
                        padding: 10px 20px;
                        font-size: 16px;
                        background-color: #FF9800;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
                    ">Load CSV</button>

                    <button onclick="exitApp()" style="
                        padding: 10px 20px;
                        font-size: 16px;
                        background-color: #f44336;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
                    ">Exit</button>
                </div>

                <script>
                    function connectRobot() {
                        window.pywebview.api.connect_robot();
                    }

                    function loadCSV() {
                        window.pywebview.api.load_csv();
                    }

                    function sendWaypoints() {
                        window.pywebview.api.send_waypoints();
                    }

                    function exitApp() {
                        window.close();
                    }
                </script>

                           
            """)

        return str(map_path)

    def run(self):
        # Start the webview window
        webview.start()

    def connect_robot(self):
        # Actual connect robot functionality
        print("Connecting to robot...")  # Placeholder for actual logic
        # Optionally show a message in Python using messagebox if needed:
        # messagebox.showinfo("Connect", "Connecting to robot...")

    def load_csv(self):
        # Load CSV functionality
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")],
            title="Select CSV File"
        )
        if file_path:
            print(f"Loaded CSV from {file_path}")  # Placeholder for actual logic
            # Optionally show a message in Python using messagebox if needed:
            # messagebox.showinfo("Load CSV", f"Loaded CSV from {file_path}")

    def send_waypoints(self):
        # Send waypoints functionality
        print("Waypoints sent to the robot!")  # Placeholder for actual logic
        # Optionally show a message in Python using messagebox if needed:
        messagebox.showinfo("Send Waypoints", "Waypoints sent to the robot!")
    
    def run(self):
        # Start the webview window
        webview.start()

if __name__ == "__main__":
    app = SimpleGCS()
    app.run()
