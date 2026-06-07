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
    QLabel
)
from payoff_calc import (
    Schedule,
    Loan
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
        self.start_date = self.date_edit.date().toString("yyyy-MM-dd")
        self.calculate_btn.clicked.connect(self.run_calculation)

        input_layout.addWidget(self.amount_input)
        input_layout.addWidget(self.rate_input)
        input_layout.addWidget(self.payment_input)
        input_layout.addWidget(self.term_input)
        input_layout.addWidget(self.date_edit)
        input_layout.addWidget(self.calculate_btn)

        self.date_paid_label = QLabel("Estimated payoff date: ")
        self.total_paid_label = QLabel("Total paid: $0.00")
        self.total_principal_paid_label = QLabel("Total principal paid: $0.00")
        self.total_interest_paid_label = QLabel("Total interest paid: $0.00")

        output_layout.addWidget(self.date_paid_label)
        output_layout.addWidget(self.total_paid_label)
        output_layout.addWidget(self.total_principal_paid_label)
        output_layout.addWidget(self.total_interest_paid_label)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def run_calculation(self):
        loan = Loan(
            principal = float(self.amount_input.text().strip()),
            term = int(self.term_input.text().strip()),
            interest_rate = float(self.rate_input.text())/100,
            loan_payment = float(self.payment_input.text()),
            due_date = self.start_date,
            borrower_id = "test"
        )
        schedule = Schedule(
            loan=loan,
            start_date=self.start_date
        )

        schedule.payoff_schedule(float(self.payment_input.text()))

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

