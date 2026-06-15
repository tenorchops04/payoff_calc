import sys

from PySide6.QtCore import QDate, QDateTime
from PySide6.QtWidgets import(
    QMainWindow,
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QDateEdit,
    QLabel,
    QTableWidget,
    QTableWidgetItem
)
from payoff_calc import (
    Schedule,
    Loan,
    Statement
)

class LoanCalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loan Payoff Calculator")
        self.resize(600, 400)

        main_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        output_layout = QVBoxLayout()

        self.calculate_btn = QPushButton("Calculate")

        self.amount_input = QLineEdit(placeholderText="Loan amount ($))")
        self.rate_input = QLineEdit(placeholderText="Interest rate (%))")
        self.payment_input = QLineEdit(placeholderText="Payment amount ($)")
        self.term_input = QLineEdit(placeholderText="Loan term length")

        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("MM-dd-yyyy")

        self.due_date_edit = QDateEdit()
        self.due_date_edit.setDate(QDate.currentDate())
        self.due_date_edit.setCalendarPopup(True)
        self.due_date_edit.setDisplayFormat("MM-dd-yyyy")

        self.calculate_btn.clicked.connect(self.run_calculation)

        self.schedule_table = QTableWidget()

        input_layout.addWidget(self.amount_input)
        input_layout.addWidget(self.rate_input)
        input_layout.addWidget(self.payment_input)
        input_layout.addWidget(self.term_input)
        input_layout.addWidget(self.date_edit)
        input_layout.addWidget(self.due_date_edit)
        input_layout.addWidget(self.calculate_btn)

        self.date_paid_label = QLabel("Estimated payoff date: ")
        self.total_paid_label = QLabel("Total paid: $0.00")
        self.total_principal_paid_label = QLabel("Total principal paid: $0.00")
        self.total_interest_paid_label = QLabel("Total interest paid: $0.00")

        output_layout.addWidget(self.date_paid_label)
        output_layout.addWidget(self.total_paid_label)
        output_layout.addWidget(self.total_principal_paid_label)
        output_layout.addWidget(self.total_interest_paid_label)
        output_layout.addWidget(self.schedule_table)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def run_calculation(self):
        self.start_date = self.date_edit.date().toString("yyyy-MM-dd")
        self.due_date = self.due_date_edit.date().toString("yyyy-MM-dd")

        loan = Loan(
            principal = float(self.amount_input.text().strip()),
            term = int(self.term_input.text().strip()),
            interest_rate = float(self.rate_input.text())/100,
            loan_payment = float(self.payment_input.text()),
            due_date = self.due_date,
            borrower_id = "test"
        )
        schedule = Schedule(
            loan=loan,
            start_date=self.start_date
        )

        schedule.payoff_schedule(float(self.payment_input.text()))

        self.schedule_table.setColumnCount(len(Statement._fields))
        self.schedule_table.setHorizontalHeaderLabels(["Date", "Principal", "Interest"])
        self.schedule_table.setRowCount(len(schedule.schedule))

        for i, statement in enumerate(schedule.schedule):
            print(statement.date)
            print(statement.principal)
            print(statement.interest)
            item_date = QTableWidgetItem(statement.date)
            item_principal = QTableWidgetItem(f"{statement.principal:.2f}")
            item_interest = QTableWidgetItem(f"{statement.interest:.2f}")
            self.schedule_table.setItem(i, 0, item_date)
            self.schedule_table.setItem(i, 1, item_principal)
            self.schedule_table.setItem(i, 2, item_interest)

        self.date_paid_label.setText(
            f"Estimated payoff date: {schedule.payoff_date}"
        )
        self.total_paid_label.setText(
            f"Total paid: ${loan.total_paid:.2f}"
        )
        self.total_principal_paid_label.setText(
            f"Total principal paid: ${loan.total_paid_principal:.2f}"
        )
        self.total_interest_paid_label.setText(
            f"Total interest paid: ${loan.total_paid_interest:.2f}"
        )


app = QApplication(sys.argv)
window = LoanCalculatorApp()
window.show()
sys.exit(app.exec())

