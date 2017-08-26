from PyQt5.QtWidgets import QApplication,QDialog,QTabWidget,QWidget,QTableWidget,QTableWidgetItem,QVBoxLayout
import pymysql

class TabDialog(QDialog):
    def __init__(self, parent=None):
        super(TabDialog, self).__init__(parent)
        self.infos = []
        self.tabWidget = QTabWidget()
        self.tabWidget.setFixedSize(700,500)

    def pushInfos(self):
        self.tabWidget.addTab(InfoListTab(self.infos), "基本信息")
        self.tabWidget.addTab(CoursesListTab(), "课程表")
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.tabWidget)
        self.setLayout(mainLayout)
        self.setWindowTitle("YNU")

    def setInfos(self, infos):
        self.infos = infos

class InfoListTab(QWidget):
    def __init__(self, infos, parent=None):
        super(InfoListTab, self).__init__(parent)
        infoListBox = QTableWidget(10, 4)
        for row in range(0, len(infos)):
            for col in range(0, len(infos[row])):
                infoListBox.setItem(row, col, QTableWidgetItem(infos[row][col]))
        layout = QVBoxLayout()
        layout.addWidget(infoListBox)
        self.setLayout(layout)


class CoursesListTab(QWidget):
    def __init__(self, parent=None):
        super(CoursesListTab, self).__init__(parent)
        coursesListBox = QTableWidget()
        infos = []
        db = pymysql.connect('localhost', 'root', 'gotoAnd@123', 'urp', use_unicode=True, charset="utf8")
        cursor = db.cursor()
        sql = "SELECT * FROM GRADE WHERE course_grade >= 90"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for r in results:
                infos.append(r)
        except:
            db.rollback()
        db.close()
        coursesListBox.setColumnCount(8)
        coursesListBox.setRowCount(len(infos))
        headers = ["学期","教学班代码","课程名称","课程性质","开课学院","学分","绩点","总成绩"]
        coursesListBox.setHorizontalHeaderLabels(headers)
        for row in range(0,len(infos)):
            for col in range(0,len(infos[row])):
                coursesListBox.setItem(row, col, QTableWidgetItem(str(infos[row][col])))

        layout = QVBoxLayout()
        layout.addWidget(coursesListBox)
        self.setLayout(layout)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    login = TabDialog()
    login.show()
    sys.exit(app.exec_())
