import sys
import csv
from collections import defaultdict
from datetime import datetime
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QAbstractItemView, QSplitter
import pyqtgraph as pg

class SensorPlotter(QtWidgets.QMainWindow):
    
    sensor_dict = {
        '0x101': ['Pot_1', 'ax', 'ay', 'az'],
        '0x201': ['Pot_2', 'gx', 'gy', 'gz'],
        '0x520': ['RPM', 'Throttle', 'MAP', 'Lambda'],
        '0x521': ['Lambda A', 'Ignition Angle', 'Ignition Cut', 'NO_SENSOR'],
        '0x522': ['Fuel Cut', 'Vehicle Speed', 'NO_SENSOR', 'NO_SENSOR'],
        '0x524': ['Lambda Corr A', 'NO_SENSOR', 'NO_SENSOR', 'NO_SENSOR'],
        '0x530': ['Battery Voltage', 'Intake Air Temp', 'Coolant Temp', 'NO_SENSOR'],
        '0x536': ['Gear', 'Oil Pressure', 'Oil Temp', 'NO_SENSOR'],
        '0x537': ['Coolant Pressure', 'NO_SENSOR', 'NO_SENSOR', 'NO_SENSOR'],
        '0x538': ['Brake Pressure'],
        '0x527': ['Lambda Target', 'NO_SENSOR', 'NO_SENSOR', 'NO_SENSOR'],
        '0x542': ['ECU Errors', 'NO_SENSOR', 'NO_SENSOR', 'NO_SENSOR']
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sensor Data Visualizer | TelemetryFSTUC")
        self.setGeometry(100, 100, 1200, 700)
        
        # Apply modern theme
        self.apply_dark_theme()

        # Main Layout with Splitter
        self.splitter = QSplitter(QtCore.Qt.Horizontal)
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QtWidgets.QHBoxLayout(self.central_widget)
        main_layout.addWidget(self.splitter)

        # Sidebar Layout
        self.sidebar = QtWidgets.QWidget()
        self.sidebar.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.sidebar.setMinimumWidth(220)  # Set a reasonable minimum width
        self.sidebar.setMaximumWidth(220)  # Prevent auto-expansion
        sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar)

        # File selection
        self.file_label = QtWidgets.QLabel("No file selected")
        self.file_button = QtWidgets.QPushButton("📂 Select CSV File")
        self.file_button.setObjectName("modernButton")
        self.file_button.clicked.connect(self.load_file)

        # Sensor selection
        self.sensor_list = QtWidgets.QListWidget()
        self.sensor_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.sensor_list.setStyleSheet("""
            QListWidget {
                background-color: #282828;
                color: white;
            }
            QListWidget::item:selected {
                background-color: #bc2b1b;  /* Change selected item background to red */
                color: white;           /* Ensure text is visible */
            }
            QListWidget::item:hover {
                background-color: #9c2b1f;  /* Optional: Change hover color */
            }
        """)

        # Plot Mode
        self.plot_mode = QtWidgets.QComboBox()
        self.plot_mode.addItems(["Single Plot", "Multiple Subplots"])
        self.plot_mode.setStyleSheet("background-color: #282828; color: white; padding: 5px; border-radius: 5px;")

        # Add/Remove Sensor Buttons
        self.add_button = QtWidgets.QPushButton("➕Add Sensors")
        self.add_button.setObjectName("modernButton")
        # Set custom icon (provide the correct path to your icon file)
        #addIcon = QtGui.QIcon("icons/add.svg")  # Use a .png, .svg, or .ico file
        #self.add_button.setIcon(addIcon)
        #self.add_button.setIconSize(QtCore.QSize(32, 32))  # Adjust size as needed
        self.add_button.clicked.connect(self.add_sensors_to_plot)

        self.remove_button = QtWidgets.QPushButton("➖Remove Sensors")
        self.remove_button.setObjectName("modernButton")
        #removeIcon = QtGui.QIcon("icons/remove.svg")  # Use a .png, .svg, or .ico file
        #self.add_button.setIcon(removeIcon)
        #self.add_button.setIconSize(QtCore.QSize(32, 32))  # Adjust size as needed
        self.remove_button.clicked.connect(self.remove_sensors_from_plot)

        # Reset Button
        self.reset_button = QtWidgets.QPushButton("Reset")
        self.reset_button.setObjectName("modernButton")
        #resetIcon = QtGui.QIcon("icons/reset.svg")  # Use a .png, .svg, or .ico file
        #self.add_button.setIcon(resetIcon)
        #self.add_button.setIconSize(QtCore.QSize(32, 32))  # Adjust size as needed
        self.reset_button.clicked.connect(self.reset_plot)

        # Add Widgets to Sidebar
        sidebar_layout.addWidget(self.file_label)
        sidebar_layout.addWidget(self.file_button)
        sidebar_layout.addWidget(QtWidgets.QLabel("Select Sensors:"))
        sidebar_layout.addWidget(self.sensor_list)
        sidebar_layout.addWidget(QtWidgets.QLabel("Plot Mode:"))
        sidebar_layout.addWidget(self.plot_mode)
        sidebar_layout.addWidget(self.add_button)
        sidebar_layout.addWidget(self.remove_button)
        sidebar_layout.addWidget(self.reset_button)

        self.sidebar.setLayout(sidebar_layout)

        # Graph Container
        self.graphWidget = pg.GraphicsLayoutWidget()
        pg.setConfigOption('background', 'black')
        pg.setConfigOption('foreground', 'white')

        # Add Sidebar and Graph to Splitter
        # Add Sidebar and Graph to Splitter
        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.graphWidget)
        self.splitter.setStretchFactor(0, 0)  # Sidebar should not stretch
        self.splitter.setStretchFactor(1, 1)  # Graph should take remaining space
        self.splitter.setSizes([220, 900])  # Initial sizes

        # Initialize variables
        self.sensor_data = {}
        self.plotted_sensors = {}
        self.plots = []  # List for subplots

    def apply_dark_theme(self):
        """Apply a modern dark theme with rounded buttons"""
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                color: white;
                font-family: Roboto;
            }
            QPushButton#modernButton {
                background-color: #bc2b1b;
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton#modernButton:hover {
                background-color: #9c2b1f;
            }
        """)

    def load_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select a CSV file", "", "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            self.file_label.setText(f"Selected: {file_path}")
            self.sensor_data = self.read_csv_and_extract_data(file_path)
            self.update_sensor_list()

    def read_csv_and_extract_data(self, file_path):
        """Read CSV and extract sensor data"""
        sensor_data = defaultdict(lambda: {'timestamps': [], 'values': []})

        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  

            base_time = None
            for row in reader:
                timestamp, sensor_id, *values = row
                try:
                    current_time = datetime.strptime(timestamp, "%H:%M:%S.%f")
                    if base_time is None:
                        base_time = current_time
                    elapsed_seconds = (current_time - base_time).total_seconds()
                except ValueError:
                    continue  

                if sensor_id in self.sensor_dict:
                    for name, value in zip(self.sensor_dict[sensor_id], values):
                        if name != 'NO_SENSOR':
                            sensor_data[name]['timestamps'].append(elapsed_seconds)
                            sensor_data[name]['values'].append(float(value))
        
        return sensor_data

    def update_sensor_list(self):
        """Update the sensor list with available data"""
        self.sensor_list.clear()
        sorted_sensors = sorted(self.sensor_data.keys())

        for sensor in sorted_sensors:
            item = QtWidgets.QListWidgetItem(sensor)
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Center text
            self.sensor_list.addItem(item)

    def add_sensors_to_plot(self):
        """Add selected sensors to the plot without removing already plotted ones."""
        selected_sensors = [item.text() for item in self.sensor_list.selectedItems()]
        colors = ['#FF3CAC', '#5EC3FF', '#3AFF5B', '#FFC75F', '#FF6F91', '#845EC2', '#D65DB1']

        # Αν δεν έχουμε επιλεγμένους αισθητήρες, δεν κάνουμε τίποτα
        if not selected_sensors:
            return  

        if self.plot_mode.currentText() == "Single Plot":
            # Αν δεν υπάρχει ήδη plot, δημιουργούμε ένα
            if not self.plots:
                p = self.graphWidget.addPlot(title="Sensor Data")
                p.showGrid(x=True, y=True)
                p.addLegend()
                self.plots.append(p)
            else:
                p = self.plots[0]  # Παίρνουμε το ήδη υπάρχον γράφημα

            # Προσθέτουμε μόνο τους νέους αισθητήρες
            for sensor in selected_sensors:
                if sensor not in self.plotted_sensors:  # Μην προσθέτεις διπλότυπα
                    color = colors[len(self.plotted_sensors) % len(colors)]
                    curve = p.plot(
                        self.sensor_data[sensor]['timestamps'],
                        self.sensor_data[sensor]['values'],
                        pen=pg.mkPen(color, width=2),
                        name=sensor
                    )
                    self.plotted_sensors[sensor] = color  # Καταγράφουμε τον αισθητήρα

        else:  # Multiple Subplots Mode
            for sensor in selected_sensors:
                if sensor not in self.plotted_sensors:  # Μην προσθέτεις αν υπάρχει ήδη
                    p = self.graphWidget.addPlot(title=sensor)
                    p.showGrid(x=True, y=True)
                    p.addLegend()
                    color = colors[len(self.plotted_sensors) % len(colors)]
                    p.plot(
                        self.sensor_data[sensor]['timestamps'],
                        self.sensor_data[sensor]['values'],
                        pen=pg.mkPen(color, width=2),
                        name=sensor
                    )
                    self.graphWidget.nextRow()
                    self.plots.append(p)
                    self.plotted_sensors[sensor] = color  # Καταγράφουμε τον αισθητήρα


    def remove_sensors_from_plot(self):
        """Remove only the selected sensors from the existing plots, without clearing everything."""
        selected_sensors = [item.text() for item in self.sensor_list.selectedItems()]

        if not selected_sensors:
            return  # Αν δεν υπάρχει επιλογή, δεν κάνουμε τίποτα

        if self.plot_mode.currentText() == "Single Plot":
            if self.plots:
                plot = self.plots[0]  # Στην περίπτωση του Single Plot, έχουμε ένα μόνο γράφημα
                for sensor in selected_sensors:
                    for curve in plot.listDataItems():  # Παίρνουμε όλα τα curves που έχουν σχεδιαστεί
                        if curve.name() == sensor:
                            plot.removeItem(curve)  # Αφαιρούμε μόνο το επιλεγμένο curve

        else:  # Multiple Subplots
            for plot in self.plots[:]:  # Χρησιμοποιούμε copy της λίστας για ασφαλή διαγραφή
                for curve in plot.listDataItems():
                    if curve.name() in selected_sensors:
                        plot.removeItem(curve)

                # Αν το γράφημα δεν έχει πια δεδομένα, το αφαιρούμε από το layout
                if not plot.listDataItems():
                    self.graphWidget.removeItem(plot)
                    self.plots.remove(plot)

        # Αφαιρούμε τους επιλεγμένους αισθητήρες από το tracking
        for sensor in selected_sensors:
            if sensor in self.plotted_sensors:
                del self.plotted_sensors[sensor]



    def reset_plot(self):
        """Clear everything and reset selections"""
        self.graphWidget.clear()
        self.sensor_list.clearSelection()
        self.plots.clear()
        self.plotted_sensors.clear()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SensorPlotter()
    window.show()
    sys.exit(app.exec())
