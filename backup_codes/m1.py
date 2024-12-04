import tkinter as tk
from tkinter import filedialog, messagebox
import folium
from pathlib import Path
import webview

# Main window
class GroundControlStation(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple GCS")
        self.geometry("800x600")

        # Add buttons
        self.connect_btn = tk.Button(self, text="Connect", command=self.connect_robot)
        self.connect_btn.pack(side=tk.TOP, pady=5)

        self.load_csv_btn = tk.Button(self, text="Load CSV", command=self.load_csv)
        self.load_csv_btn.pack(side=tk.TOP, pady=5)

        self.send_wp_btn = tk.Button(self, text="Send Waypoints", command=self.send_waypoints)
        self.send_wp_btn.pack(side=tk.TOP, pady=5)

        # Map Display
        self.map_window = None
        self.load_map()

    def load_map(self):
        # Create a simple folium map
        map_path = Path("templates/map2.html")
        map_path.parent.mkdir(exist_ok=True)  # Ensure resources directory exists
        m = folium.Map(location=[45.4642, 9.1900], zoom_start=12)  # Centered at Milan, Italy
        m.save(str(map_path))

        # Launch map in a webview
        self.map_window = webview.create_window("Map", str(map_path))
        webview.start()

    def connect_robot(self):
        messagebox.showinfo("Connect", "Connecting to robot...")

    def load_csv(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")],
            title="Select CSV File"
        )
        if file_path:
            messagebox.showinfo("Load CSV", f"Loaded CSV from {file_path}")

    def send_waypoints(self):
        messagebox.showinfo("Send Waypoints", "Waypoints sent to the robot!")


if __name__ == "__main__":
    app = GroundControlStation()
    app.mainloop()
