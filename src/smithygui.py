# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "click>=8.4.1",
#     "polars>=1.41.0",
#     "pyside6>=6.11.1",
#     "rich>=15.0.0",
#     "rustworkx>=0.17.1",
# ]
# ///
from PySide6.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)

window = QWidget()
window.show()

app.exec()
