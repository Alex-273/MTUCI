# UIBot
--
Database visualization on Python that uses PostgreSQL and PyQt5 module. Displays the database in the form of a tabbed table and allows you to edit its lines, as well as add and delete the contents of the database.
--
Written in Python using PostgreSQL:
```python
import psycopg2
import sys
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox)
```
