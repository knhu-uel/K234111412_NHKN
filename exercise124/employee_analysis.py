import pandas as pd
import numpy as np
from datetime import datetime
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
                             QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel,
                             QComboBox, QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor


def download_and_add_employees():
    url = "https://tranduythanh.com/datasets/employee.csv"
    try:
        df = pd.read_csv(url)
        print("Data downloaded successfully!")
    except Exception as e:
        print(f"Error downloading data: {e}")
        df = pd.DataFrame(columns=['ID', 'Name', 'BirthDate', 'Role', 'Department', 'Salary'])

    new_employees = [
        {'ID': 'E101', 'Name': 'Nguyen Van A', 'BirthDate': '2001-05-15', 'Role': 'Developer', 'Department': 'IT',
         'Salary': 15000000},
        {'ID': 'E102', 'Name': 'Tran Thi B', 'BirthDate': '1995-08-22', 'Role': 'Tester', 'Department': 'QA',
         'Salary': 12000000},
        {'ID': 'E103', 'Name': 'Le Van C', 'BirthDate': '1990-03-10', 'Role': 'Manager', 'Department': 'HR',
         'Salary': 25000000},
        {'ID': 'E104', 'Name': 'Pham Thi D', 'BirthDate': '2001-11-30', 'Role': 'Designer', 'Department': 'Marketing',
         'Salary': 14000000},
        {'ID': 'E105', 'Name': 'Hoang Van E', 'BirthDate': '1985-07-18', 'Role': 'Tester', 'Department': 'QA',
         'Salary': 18000000}
    ]

    df = pd.concat([df, pd.DataFrame(new_employees)], ignore_index=True)
    df['BirthDate'] = pd.to_datetime(df['BirthDate'])
    current_year = datetime.now().year
    df['Age'] = current_year - df['BirthDate'].dt.year

    return df


class EmployeeTableWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phân tích dữ liệu nhân viên")
        self.setGeometry(100, 100, 1000, 600)

        self.df = download_and_add_employees()
        self.filtered_df = self.df.copy()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        filter_layout = QHBoxLayout()

        role_label = QLabel("Lọc theo vai trò:")
        self.role_combo = QComboBox()
        self.role_combo.addItem("Tất cả")
        roles = self.df['Role'].unique()
        self.role_combo.addItems(roles)
        self.role_combo.currentTextChanged.connect(self.apply_filters)

        year_label = QLabel("Lọc theo năm sinh:")
        self.year_combo = QComboBox()
        years = sorted(self.df['BirthDate'].dt.year.unique(), reverse=True)
        self.year_combo.addItem("Tất cả")
        self.year_combo.addItems(map(str, years))
        self.year_combo.currentTextChanged.connect(self.apply_filters)

        filter_layout.addWidget(role_label)
        filter_layout.addWidget(self.role_combo)
        filter_layout.addWidget(year_label)
        filter_layout.addWidget(self.year_combo)
        filter_layout.addStretch()

        button_layout = QHBoxLayout()

        self.all_btn = QPushButton("Tất cả nhân viên")
        self.all_btn.clicked.connect(self.show_all_employees)

        self.born_2001_btn = QPushButton("Sinh năm 2001")
        self.born_2001_btn.clicked.connect(self.show_born_2001)

        self.oldest_btn = QPushButton("TOP 3 tuổi cao nhất")
        self.oldest_btn.clicked.connect(self.show_oldest)

        self.tester_btn = QPushButton("Nhân viên Tester")
        self.tester_btn.clicked.connect(self.show_testers)

        self.count_btn = QPushButton("Thống kê theo vai trò")
        self.count_btn.clicked.connect(self.show_role_counts)

        button_layout.addWidget(self.all_btn)
        button_layout.addWidget(self.born_2001_btn)
        button_layout.addWidget(self.oldest_btn)
        button_layout.addWidget(self.tester_btn)
        button_layout.addWidget(self.count_btn)

        self.table = QTableWidget()
        self.table.setFont(QFont("Arial", 10))

        main_layout.addLayout(filter_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)

        self.show_all_employees()

    def populate_table(self, df, headers=None):
        self.table.clear()
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))

        headers = headers or df.columns
        self.table.setHorizontalHeaderLabels(headers)

        header_font = QFont("Arial", 10, QFont.Weight.Bold)
        self.table.horizontalHeader().setFont(header_font)

        for row in range(len(df)):
            for col in range(len(df.columns)):
                value = str(df.iloc[row, col])
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                if 'Role' in df.columns and col == df.columns.get_loc('Role') and value == 'Tester':
                    item.setBackground(QColor(255, 230, 230))

                if 'BirthDate' in df.columns and col == df.columns.get_loc('BirthDate') and '2001' in value:
                    item.setBackground(QColor(230, 255, 230))

                self.table.setItem(row, col, item)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)

    def apply_filters(self):
        selected_role = self.role_combo.currentText()
        selected_year = self.year_combo.currentText()

        filtered_df = self.df.copy()

        if selected_role != "Tất cả":
            filtered_df = filtered_df[filtered_df['Role'] == selected_role]

        if selected_year != "Tất cả":
            try:
                year = int(selected_year)
                filtered_df = filtered_df[filtered_df['BirthDate'].dt.year == year]
                print(f"Filtering for year {year}. Rows found: {len(filtered_df)}")
            except ValueError:
                print(f"Invalid year: {selected_year}")

        self.filtered_df = filtered_df
        self.populate_table(filtered_df)

        print(f"Total rows after filtering: {len(filtered_df)}")
        print(f"Unique years in filtered data: {filtered_df['BirthDate'].dt.year.unique()}")

    def show_all_employees(self):
        self.role_combo.setCurrentText("Tất cả")
        self.year_combo.setCurrentText("Tất cả")
        self.populate_table(self.df)

    def show_born_2001(self):
        employees_2001 = self.df[self.df['BirthDate'].dt.year == 2001]
        self.populate_table(employees_2001)
        self.role_combo.setCurrentText("Tất cả")
        self.year_combo.setCurrentText("2001")
        print(f"Employees born in 2001: {len(employees_2001)}")

    def show_oldest(self):
        oldest_employees = self.df.sort_values(by='Age', ascending=False).head(3)
        self.populate_table(oldest_employees)
        self.role_combo.setCurrentText("Tất cả")
        self.year_combo.setCurrentText("Tất cả")

    def show_testers(self):
        testers = self.df[self.df['Role'] == 'Tester']
        self.populate_table(testers)
        self.role_combo.setCurrentText("Tester")
        self.year_combo.setCurrentText("Tất cả")

    def show_role_counts(self):
        role_counts = self.df['Role'].value_counts().reset_index()
        role_counts.columns = ['Vai trò', 'Số lượng']

        self.table.clear()
        self.table.setRowCount(len(role_counts))
        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels(['Vai trò', 'Số lượng'])

        header_font = QFont("Arial", 10, QFont.Weight.Bold)
        self.table.horizontalHeader().setFont(header_font)

        for row in range(len(role_counts)):
            role_item = QTableWidgetItem(str(role_counts.iloc[row]['Vai trò']))
            count_item = QTableWidgetItem(str(role_counts.iloc[row]['Số lượng']))

            role_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            count_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table.setItem(row, 0, role_item)
            self.table.setItem(row, 1, count_item)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)

        self.role_combo.setCurrentText("Tất cả")
        self.year_combo.setCurrentText("Tất cả")

    def show_error_message(self, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Icon.Warning)
        error_box.setText(message)
        error_box.setWindowTitle("Lỗi")
        error_box.exec()


def main():
    app = QApplication(sys.argv)
    window = EmployeeTableWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()