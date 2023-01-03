from PyQt5.QtWidgets import QApplication, QWidget, QLabel

# For accessing command line args
import sys

# Allow command lines args for app
app = QApplication(sys.argv)

# Create a Qt widget, will be window
window = QWidget()

# Add text to window
textLabel = QLabel(window)
textLabel.setText("Hello, World!")

# Set window title
window.setWindowTitle("PyQt5 Example")

# Windows are hidden by default
window.show()

# Start event loop
app.exec()
