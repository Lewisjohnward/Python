"""
Dialog-style application.

A dialog is always an independent window. 
If a dialog has a parent, then it'll display centered on top of the parent widget.

"""
import sys


from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
)

# Defines a Window class for the app's GUI by inherting from QDialog
class Window(QDialog):
    # Initalise this class
    def __init__(self):
        super().__init__(parent=None)
        # Set window title
        self.setWindowTitle("QDialog")
        # Assign a QVBoxLayout object
        dialogLayout = QVBoxLayout()
        # Assign a QFormLayout object
        formLayout = QFormLayout()
        # Add widgets to formLayout
        formLayout.addRow("Name:", QLineEdit())
        formLayout.addRow("Age:", QLineEdit())
        formLayout.addRow("Job:", QLineEdit())
        formLayout.addRow("Hobbies:", QLineEdit())
        # Embeds the form layout into the global dialog box
        dialogLayout.addLayout(formLayout)
        # Defines button box
        buttons = QDialogButtonBox()
        # Adds two buttons
        buttons.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )
        dialogLayout.addWidget(buttons)
        self.setLayout(dialogLayout)

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
