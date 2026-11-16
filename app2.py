import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Visualizer App")
        self.resize(800, 600)

        # Variables to store selected file and data
        self.filename = None
        self.month_list = []
        self.rainfall_list = []

        # Central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Top Button: "Load Data"
        self.load_button = QPushButton("Load Data", self)
        self.load_button.clicked.connect(self.load_data)
        layout.addWidget(self.load_button)

        # Matplotlib Graph Area
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        layout.addWidget(self.canvas)

        # Draw initial graph
        self.draw_graph()

    def load_data(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Data File",
            "",
            "All Files (*.*);;CSV Files (*.csv);;Text Files (*.txt)",
        )
        if filename:
            self.filename = filename
            self.month_list = []
            self.rainfall_list = []

            with open(filename, "r", encoding="utf-8") as f:
                next(f)  # Skip header row
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(",")
                    self.month_list.append(parts[0].strip())
                    self.rainfall_list.append(float(parts[1].strip()))

            self.draw_graph()

    def draw_graph(self):
        self.ax.clear()

        if self.month_list and self.rainfall_list:
            self.ax.bar(self.month_list, self.rainfall_list, color="#1f77b4")
            title = self.filename.replace("\\", "/").split("/")[-1] if self.filename else "Data Plot"
            self.ax.set_title(title)
            self.ax.set_xlabel("Month")
            self.ax.set_ylabel("Rainfall (mm)")
            self.ax.grid(axis="y", linestyle="--", alpha=0.7)
        else:
            self.ax.set_title("No Data Loaded - Click 'Load Data'")
            self.ax.set_xlabel("X Axis")
            self.ax.set_ylabel("Y Axis")

        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
