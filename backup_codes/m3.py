import webview
import folium
import os
from pathlib import Path
from tkinter import filedialog, messagebox


class SimpleGCS:
    def __init__(self):
        # Expose the Python methods to JavaScript
        self.window = None

        # Generate the interactive map with buttons
        self.map_path = self.generate_map_with_buttons()

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
                        window.pywebview.api.connectRobot();
                    }

                    function loadCSV() {
                        window.pywebview.api.loadCSV();
                    }

                    function sendWaypoints() {
                        window.pywebview.api.sendWaypoints();
                    }

                    function exitApp() {
                        window.pywebview.api.exitApp();
                    }
                </script>
                           
            """)

        return str(map_path)

    def connect_robot(self):
        # This function will be called from JavaScript
        print("Connecting to the robot...")
        messagebox.showinfo("Connect", "Connecting to robot...")

    def load_csv(self):
        # This function will be called from JavaScript
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")],
            title="Select CSV File"
        )
        if file_path:
            print(f"Loaded CSV from {file_path}")
            messagebox.showinfo("Load CSV", f"Loaded CSV from {file_path}")

    def send_waypoints(self):
        # This function will be called from JavaScript
        print("Sending waypoints to the robot...")
        messagebox.showinfo("Send Waypoints", "Waypoints sent to the robot!")

    def exit_app(self):
        # This function will be called from JavaScript to exit the app
        print("Exiting the application...")
        webview.destroy_window()

    def run(self):
        # Expose Python methods to JavaScript (use the 'api' name)
        webview.create_window("Simple GCS", self.map_path, js_api=self)
        webview.start()


if __name__ == "__main__":
    app = SimpleGCS()
    app.run()
