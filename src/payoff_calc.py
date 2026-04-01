from uuid import uuid4
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class Loan:
    def __init__(
        self,
        principal: float,
        term: float,
        interest_rate: float,
        loan_payment: float,
        due_date: str,
        borrower_id: str,
        loan_name = "Default",
        loan_id = str(uuid4())
    ):
        self.borrower_id = borrower_id
        self.loan_name = loan_name
        self.loan_id = loan_id
        self.principal = principal
        self.term = term
        self.interest_rate = interest_rate
        self.loan_payment = loan_payment
        self.due_date = datetime.fromisoformat(due_date)
        self.total_accrued_interest = 0
        self.total_paid = 0
        self.total_paid_principal = 0
        self.total_paid_interest = 0

    def accrue_interest(self, days: int = 1):
        daily_interest_accrual = (self.principal * self.interest_rate) / 365.25
        interest_accrued = daily_interest_accrual * days

        self.total_accrued_interest += interest_accrued

        return interest_accrued

    def make_payment(self, amount):
        if amount < 0:
            raise ValueError("Amount to pay cannot be negative")

        # Payments are first applied to accrued interest
        payment_to_interest = min(amount, self.total_accrued_interest)
        payment_to_principal = min(self.principal, amount - payment_to_interest)
        amount_remaining = amount - payment_to_interest - payment_to_principal

        self.total_accrued_interest -= payment_to_interest
        self.principal -= payment_to_principal

        self.total_paid += amount
        self.total_paid_interest += payment_to_interest
        self.total_paid_principal += payment_to_principal

        return payment_to_interest, payment_to_principal, amount_remaining

class Schedule:
    def __init__(self, loan: Loan, start_date: str):
        self.loan = loan
        self.start_date = start_date

    def create_schedule(self, pay_amount: float):
        start_date = datetime.fromisoformat(self.start_date)
        curr_date = datetime.fromisoformat(self.start_date)

        while curr_date <= self.loan.due_date:
            if curr_date == self.loan.due_date:
                self.loan.make_payment(pay_amount)
            else:
                interest_accrued = self.loan.accrue_interest()
            curr_date = curr_date + timedelta(days=1)

        self.loan.due_date += relativedelta(months=1)
