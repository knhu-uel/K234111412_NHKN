import pandas as pd
import sys

import matplotlib.pyplot as plt
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QFrame, QTableWidgetItem, QMessageBox, QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np


class StockAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI file
        uic.loadUi('stock_analysis.ui', self)

        # Set window properties
        self.setWindowTitle("Stock Data Analyzer - Dark Edition")

        # Apply custom styling
        self.apply_dark_theme()

        # Load data
        self.load_data()

        # Set up matplotlib figure and canvas with dark background
        self.figure = plt.figure(figsize=(12, 4))
        self.figure.patch.set_facecolor('#2D2D30')
        self.canvas = FigureCanvas(self.figure)
        chart_layout = QVBoxLayout(self.chartWidget)
        chart_layout.addWidget(self.canvas)

        # Connect buttons to functions
        self.searchButton.clicked.connect(self.search_and_modify)
        self.addButton.clicked.connect(self.add_data)
        self.deleteButton.clicked.connect(self.delete_data)
        self.sortButton.clicked.connect(self.sort_by_price)
        self.statsButton.clicked.connect(self.calculate_stats)
        self.chartButton.clicked.connect(self.generate_charts)

        # Update table with initial data
        self.update_table()

        # Generate initial charts
        self.generate_charts()

    def apply_dark_theme(self):
        # Set dark theme colors
        dark_bg = "#1E1E1E"
        darker_bg = "#252526"
        accent_color = "#007ACC"
        text_color = "#D4D4D4"
        border_color = "#3F3F46"

        # Additional accent colors
        green_accent = "#6A9955"
        orange_accent = "#CE9178"
        purple_accent = "#C586C0"
        yellow_accent = "#DCDCAA"

        # Set application style
        self.setStyleSheet(f"""
            QMainWindow, QDialog, QWidget {{
                background-color: {dark_bg};
                color: {text_color};
            }}

            QGroupBox {{
                font-weight: bold;
                border: 1px solid {border_color};
                border-radius: 4px;
                margin-top: 12px;
                background-color: {darker_bg};
                color: {text_color};
            }}

            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                color: {text_color};
            }}

            QPushButton {{
                background-color: {accent_color};
                color: white;
                border: none;
                border-radius: 2px;
                padding: 8px 16px;
                font-weight: bold;
                min-width: 80px;
            }}

            QPushButton:hover {{
                background-color: #005F9E;
            }}

            QPushButton:pressed {{
                background-color: #004275;
            }}

            QLineEdit {{
                border: 1px solid {border_color};
                border-radius: 2px;
                padding: 6px;
                background-color: {darker_bg};
                color: {text_color};
                selection-background-color: {accent_color};
            }}

            QComboBox {{
                border: 1px solid {border_color};
                border-radius: 2px;
                padding: 6px;
                background-color: {darker_bg};
                color: {text_color};
                selection-background-color: {accent_color};
            }}

            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}

            QTableWidget {{
                background-color: {darker_bg};
                color: {text_color};
                gridline-color: {border_color};
                border: 1px solid {border_color};
                border-radius: 2px;
                selection-background-color: {accent_color};
                selection-color: white;
                alternate-background-color: #2D2D30;
            }}

            QHeaderView::section {{
                background-color: #333337;
                color: {text_color};
                padding: 6px;
                border: 1px solid {border_color};
                font-weight: bold;
            }}

            QLabel {{
                color: {text_color};
            }}

            QScrollBar:vertical {{
                border: none;
                background: {darker_bg};
                width: 10px;
                margin: 0px;
            }}

            QScrollBar::handle:vertical {{
                background: #5A5A5A;
                min-height: 20px;
                border-radius: 5px;
            }}

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
                height: 0px;
            }}
        """)

        # Set different accent colors for different buttons
        self.searchButton.setStyleSheet(f"background-color: {purple_accent}; color: white;")
        self.addButton.setStyleSheet(f"background-color: {green_accent}; color: white;")
        self.deleteButton.setStyleSheet(f"background-color: {orange_accent}; color: black;")
        self.sortButton.setStyleSheet(f"background-color: {yellow_accent}; color: black;")
        self.statsButton.setStyleSheet(f"background-color: {yellow_accent}; color: black;")
        self.chartButton.setStyleSheet(f"background-color: {accent_color}; color: white;")

        # Set alternating row colors for table
        self.tableWidget.setAlternatingRowColors(True)

        # Add a title label with custom styling
        title_label = QLabel("STOCK MARKET DATA ANALYSIS", self)
        title_label.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: white;
            background-color: {accent_color};
            padding: 8px;
            border-radius: 2px;
        """)
        # Fix: Change Qt.AlignCenter to Qt.AlignmentFlag.AlignCenter
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Insert the title at the top of the layout
        main_layout = self.centralWidget().layout()
        main_layout.insertWidget(0, title_label)

        # Add separator lines between sections - FIXED HERE
        separator = QFrame(self)
        separator.setFrameShape(QFrame.Shape.HLine)  # Changed from QFrame.HLine
        separator.setFrameShadow(QFrame.Shadow.Sunken)  # Changed from QFrame.Sunken
        separator.setStyleSheet(f"background-color: {border_color};")
        main_layout.insertWidget(2, separator)

        separator2 = QFrame(self)
        separator2.setFrameShape(QFrame.Shape.HLine)  # Changed from QFrame.HLine
        separator2.setFrameShadow(QFrame.Shadow.Sunken)  # Changed from QFrame.Sunken
        separator2.setStyleSheet(f"background-color: {border_color};")
        main_layout.insertWidget(4, separator2)

    def load_data(self):
        try:
            # For this example, we'll use a local file path
            # In a real application, you would use the URL: https://tranduythanh.com/datasets/SampleData2.csv
            # self.df = pd.read_csv("https://tranduythanh.com/datasets/SampleData2.csv")

            # For demonstration, I'll create sample data similar to what might be in the file
            data = {
                'Symbol': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'JPM'],
                'Price': [180.5, 350.2, 140.8, 130.5, 300.7, 250.3, 450.2, 140.6],
                'PE': [28.5, 32.1, 25.7, 40.2, 22.3, 60.5, 45.8, 12.3],
                'Group': ['Tech', 'Tech', 'Tech', 'Retail', 'Tech', 'Auto', 'Tech', 'Finance']
            }
            self.df = pd.DataFrame(data)

            # Add USD column (requirement 4)
            self.df['USD'] = self.df['Price'] / 23

            print("Data loaded successfully:")
            print(self.df)  # Requirement 1: Print all data
        except Exception as e:
            print(f"Error loading data: {e}")
            # Create empty DataFrame with the same structure if loading fails
            self.df = pd.DataFrame(columns=['Symbol', 'Price', 'PE', 'Group', 'USD'])

    def update_table(self):
        # Update the table with current DataFrame data
        self.tableWidget.setRowCount(len(self.df))
        self.tableWidget.setColumnCount(len(self.df.columns))
        self.tableWidget.setHorizontalHeaderLabels(self.df.columns)

        # Fill the table with data
        for row in range(len(self.df)):
            for col in range(len(self.df.columns)):
                value = str(self.df.iloc[row, col])
                item = QTableWidgetItem(value)

                # Set text alignment
                # Fix: Change Qt.AlignCenter to Qt.AlignmentFlag.AlignCenter
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                # Color-code cells based on group
                if col == 3:  # Group column
                    group = self.df.iloc[row, col]
                    if group == 'Tech':
                        item.setBackground(QColor(0, 122, 204, 100))  # Blue with alpha
                    elif group == 'Retail':
                        item.setBackground(QColor(206, 145, 120, 100))  # Orange with alpha
                    elif group == 'Auto':
                        item.setBackground(QColor(106, 153, 85, 100))  # Green with alpha
                    elif group == 'Finance':
                        item.setBackground(QColor(197, 134, 192, 100))  # Purple with alpha

                # Color-code price cells based on value
                if col == 1:  # Price column
                    price = self.df.iloc[row, col]
                    if price > 300:
                        item.setForeground(QColor(106, 153, 85))  # Green text for high prices
                    elif price < 150:
                        item.setForeground(QColor(206, 145, 120))  # Orange text for low prices

                self.tableWidget.setItem(row, col, item)

        # Resize columns to content
        self.tableWidget.resizeColumnsToContents()

        # Set row height
        for row in range(len(self.df)):
            self.tableWidget.setRowHeight(row, 30)

    def search_and_modify(self):
        # Requirement 3: Search by Symbol and reduce Price by 1/2
        symbol = self.symbolInput.text().strip()
        if not symbol:
            QMessageBox.warning(self, "Input Error", "Please enter a symbol to search.")
            return

        if symbol in self.df['Symbol'].values:
            self.df.loc[self.df['Symbol'] == symbol, 'Price'] /= 2
            # Update USD column after price change
            self.df['USD'] = self.df['Price'] / 23
            self.update_table()
            QMessageBox.information(self, "Success", f"Price for {symbol} reduced by half.")
        else:
            QMessageBox.warning(self, "Not Found", f"Symbol {symbol} not found in the data.")

    def add_data(self):
        # Requirement 5: Add new data to DataFrame
        try:
            symbol = self.newSymbol.text().strip()
            price = float(self.newPrice.text().strip())
            pe = float(self.newPE.text().strip())
            group = self.newGroup.text().strip()

            if not all([symbol, self.newPrice.text(), self.newPE.text(), group]):
                QMessageBox.warning(self, "Input Error", "All fields are required.")
                return

            # Calculate USD
            usd = price / 23

            # Add new row to DataFrame
            new_row = pd.DataFrame({
                'Symbol': [symbol],
                'Price': [price],
                'PE': [pe],
                'Group': [group],
                'USD': [usd]
            })

            self.df = pd.concat([self.df, new_row], ignore_index=True)
            self.update_table()

            # Clear input fields
            self.newSymbol.clear()
            self.newPrice.clear()
            self.newPE.clear()
            self.newGroup.clear()

            QMessageBox.information(self, "Success", "New data added successfully.")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Price and PE must be numeric values.")

    def delete_data(self):
        # Requirement 7: Delete rows by Symbol
        symbol = self.deleteSymbol.text().strip()
        if not symbol:
            QMessageBox.warning(self, "Input Error", "Please enter a symbol to delete.")
            return

        initial_len = len(self.df)
        self.df = self.df[self.df['Symbol'] != symbol]

        if len(self.df) < initial_len:
            self.update_table()
            QMessageBox.information(self, "Success", f"Rows with Symbol {symbol} deleted.")
        else:
            QMessageBox.warning(self, "Not Found", f"Symbol {symbol} not found in the data.")

    def sort_by_price(self):
        # Requirement 2: Sort by Price ascending
        self.df = self.df.sort_values(by='Price')
        self.update_table()
        QMessageBox.information(self, "Success", "Data sorted by Price (ascending).")

    def calculate_stats(self):
        # Requirement 6: Group by Group column and calculate statistics
        stat_func = self.statsCombo.currentText()

        try:
            if stat_func == "mean":
                result = self.df.groupby('Group').mean()
            elif stat_func == "sum":
                result = self.df.groupby('Group').sum()
            elif stat_func == "count":
                result = self.df.groupby('Group').count()
            elif stat_func == "min":
                result = self.df.groupby('Group').min()
            elif stat_func == "max":
                result = self.df.groupby('Group').max()

            # Display results in a message box
            QMessageBox.information(self, f"Group {stat_func.capitalize()}",
                                    f"Results of {stat_func} by Group:\n\n{result}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error calculating statistics: {e}")

    def generate_charts(self):
        # Clear previous charts
        self.figure.clear()

        # Set dark background for plots
        plt.style.use('dark_background')

        # Create two subplots
        ax1 = self.figure.add_subplot(121)
        ax2 = self.figure.add_subplot(122)

        # Custom colors for the charts - neon colors for dark theme
        colors = ['#00FFFF', '#FF00FF', '#00FF00', '#FFFF00', '#FF7F00', '#FF0000', '#7F00FF', '#0000FF']

        # Chart 1: Horizontal bar chart of prices by symbol (different from previous vertical bars)
        y_pos = np.arange(len(self.df))
        bars = ax1.barh(y_pos, self.df['Price'], color=colors[:len(self.df)])
        ax1.set_yticks(y_pos)
        ax1.set_yticklabels(self.df['Symbol'])
        ax1.set_title('Price by Symbol', fontweight='bold', fontsize=12, color='white')
        ax1.set_xlabel('Price', fontweight='bold', color='white')

        # Add value labels inside bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax1.text(width - 40, bar.get_y() + bar.get_height() / 2,
                     f'{width:.1f}', ha='right', va='center',
                     color='black', fontweight='bold')

        # Chart 2: Donut chart instead of pie chart
        group_counts = self.df['Group'].value_counts()

        # Create a donut chart (pie chart with a hole in the middle)
        wedges, texts, autotexts = ax2.pie(
            group_counts,
            labels=group_counts.index,
            autopct='%1.1f%%',
            colors=colors[:len(group_counts)],
            wedgeprops={'edgecolor': 'black', 'linewidth': 1, 'alpha': 0.8}
        )

        # Make the texts more visible on dark background
        for text in texts:
            text.set_color('white')
            text.set_fontweight('bold')

        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontweight('bold')

        # Add a circle at the center to create a donut chart
        centre_circle = plt.Circle((0, 0), 0.5, fc='#1E1E1E')
        ax2.add_artist(centre_circle)

        ax2.set_title('Distribution by Group', fontweight='bold', fontsize=12, color='white')

        self.figure.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockAnalysisApp()
    window.show()
    sys.exit(app.exec())

