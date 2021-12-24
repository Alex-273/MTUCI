import psycopg2
import sys

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.rowNu = [0] * 1000

        self._connect_to_db()

        self.setWindowTitle("Shedule")

        self.vbox = QVBoxLayout(self)

        self.shedule_tab1 = QWidget()
        self.shedule_tab2 = QWidget()
        self.shedule_tab3 = QWidget()
        self.shedule_tab4 = QWidget()
        self.shedule_tab5 = QWidget()

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self.tabs.addTab(self.shedule_tab1, "Monday")
        self.tabs.addTab(self.shedule_tab2, "Tuesday")
        self.tabs.addTab(self.shedule_tab3, "Wednesday")
        self.tabs.addTab(self.shedule_tab4, "Thursday")
        self.tabs.addTab(self.shedule_tab5, "Friday")

        self._create_shedule_tab("monday", "_create_table(\"1\", \"monday\")", "1")
        self._create_shedule_tab("tuesday", "_create_table(\"2\", \"tuesday\")", "2")
        self._create_shedule_tab("wednesday", "_create_table(\"3\", \"wednesday\")", "3")
        self._create_shedule_tab("thursday", "_create_table(\"4\", \"thursday\")", "4")
        self._create_shedule_tab("friday", "_create_table(\"5\", \"friday\")", "5")

        self.tabs.currentChanged.connect(self._onChange)

        self._onChange()

    # Подключение к базе данных
    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="week_db",
                                     user="postgres",
                                     password="1234",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()

    # Создание вкладки
    def _create_shedule_tab(self, day, table, shedule):
        self.setWindowTitle("{}".format(day))
        self.monday_gbox = QGroupBox("{}".format(day))
        self.svbox = QVBoxLayout()
        self.sxbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.shbox1.addWidget(self.monday_gbox)
        exec("self.{}".format(table))
        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)
        exec("self.shedule_tab{}.setLayout(self.svbox)".format(shedule))

    # Создание таблицы QtableWidget
    def _create_table(self, table, day):
        global o
        exec("self.monday_table{} = QTableWidget()".format(table))
        o = self.ooo(day)
        o.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        o.setColumnCount(7)
        o.setHorizontalHeaderLabels(['day', 'subject', 'room', 'time', 'teacher', 'Join', 'delete'])
        self._update_table(day, "{}".format(table))
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(o)
        self.monday_gbox.setLayout(self.mvbox)

    # Заполнение и обовление таблицы для дня day
    def _update_table(self, day, table):
        global o
        self.cursor.execute("SELECT * FROM week.{} order by id;".format(day))
        records = list(self.cursor.fetchall())
        self.cursor.execute("SELECT id FROM week.{} order by id;".format(day))
        records2 = list(self.cursor.fetchall())
        self.addBut = QPushButton("+")
        r = list(enumerate(records2))
        for y, u in enumerate(records2):
            self.rowNu[y] = u[0]

        o = self.ooo(day)

        o.setRowCount(len(records) + 1)
        y = o.setRowCount(len(records) + 1)
        if len(records) == 0:
            o.setCellWidget(0, 0, self.addBut)
        for i, r in enumerate(records):
            if i == len(records) - 1:
                o.setCellWidget(i + 1, 0, self.addBut)
            r = list(r)
            exec("joinButon{} = QPushButton(\"Join\")".format(i))
            exec("delButon{} = QPushButton(\"x\")".format(i))
            exec("join{} = QPushButton(\"Join\")".format(i))

            o.setItem(i, 0,
                      QTableWidgetItem(str(r[1])))
            o.setItem(i, 1,
                      QTableWidgetItem(str(r[2])))
            o.setItem(i, 2,
                      QTableWidgetItem(str(r[3])))
            o.setItem(i, 3,
                      QTableWidgetItem(str(r[4])))
            o.setItem(i, 4,
                      QTableWidgetItem(str(r[5])))
            exec("o.setCellWidget(i, 5, joinButon{})".format(i))
            exec("o.setCellWidget(i, 6, delButon{})".format(i))
            exec("joinButon{}.clicked.connect(lambda: self._change_day_from_table({}, \"{}\"))".format(i, i, day),
                 locals())
            exec("delButon{}.clicked.connect(lambda: self._delete({}, \"{}\"))".format(i, i, day),
                 locals())
        self.addBut.clicked.connect(
            lambda: self._insert(day)
        )
        o.resizeRowsToContents()

    # Изменение таблицы базы данных в соответсвие со значениями в таблице QTableWidget
    def _change_day_from_table(self, rowNum, day):
        global o
        row = list()
        row.clear()
        o = self.ooo(day)
        for i in range(o.columnCount()):
            try:
                row.append(o.item(rowNum, i).text())
                print(day, row[0], row[2], row[4], row[6], row[8], rowNum + 1)
            except:
                row.append(None)
        try:
            print(day, row[0], row[2], row[4], row[6], rowNum + 1)
            self.cursor.execute(
                "UPDATE week.{} SET day='{}', subject='{}', room_num='{}', start_time='{}', teacher='{}' WHERE id='{}'".format(
                    day, row[0], row[2], row[4], row[6], row[8], self.rowNu[rowNum]))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    # Обработчик смены вкладки
    def _update_shedule(self):
        global o
        if self.tabs.currentIndex() == 0:
            o = self.ooo("monday")
        if self.tabs.currentIndex() == 1:
            o = self.ooo("tuesday")
        if self.tabs.currentIndex() == 2:
            o = self.ooo("wednesday")
        if self.tabs.currentIndex() == 3:
            o = self.ooo("thursday")
        if self.tabs.currentIndex() == 4:
            o = self.ooo("friday")

        o.setRowCount(0)
        if self.tabs.currentIndex() == 0:
            self._update_table("monday", "1")
        elif self.tabs.currentIndex() == 1:
            self._update_table("tuesday", "2")
        elif self.tabs.currentIndex() == 2:
            self._update_table("wednesday", "3")
        elif self.tabs.currentIndex() == 3:
            self._update_table("thursday", "4")
        elif self.tabs.currentIndex() == 4:
            self._update_table("friday", "5")

    # Обработчик кнопки Update
    def _onChange(self):
        self._update_shedule()

    # Вспомагательная функция для создания таблиц в зависимости от нажатой вкладки
    def ooo(self, day):
        if day == "monday":
            return self.monday_table1
        elif day == "tuesday":
            return self.monday_table2
        elif day == "wednesday":
            return self.monday_table3
        elif day == "thursday":
            return self.monday_table4
        elif day == "friday":
            return self.monday_table5

    # Обработчик кнопки Join
    def _insert(self, day):
        self.cursor.execute("INSERT INTO week.{} (day, subject, room_num, start_time, teacher) VALUES "
                            "(' ',' ',' ',' ',' ');".format(day))
        self.conn.commit()
        self._update_shedule()

    # Обработчик кнопки delete
    def _delete(self, rowNum, day):
        self.cursor.execute("DELETE FROM week.{} WHERE id='{}'".format(day, self.rowNu[rowNum]))
        self.conn.commit()
        self._update_shedule()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
