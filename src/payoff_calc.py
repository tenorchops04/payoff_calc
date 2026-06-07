from uuid import uuid4
from math import isclose
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
        self.interest_accrued = 0
        self.total_owed = self.principal + self.interest_accrued

    def accrue_interest(self, days: int = 1):
        daily_interest_accrual = (self.principal * self.interest_rate) / 365.25
        interest_accrued = daily_interest_accrual * days

        self.total_accrued_interest += interest_accrued
        self.interest_accrued += interest_accrued

        return interest_accrued

    def capitalize_interest(self):
        self.principal += self.interest_accrued

    def make_payment(self, amount):
        if amount < 0:
            raise ValueError("Amount to pay cannot be negative")
        total_owed = self.principal + self.interest_accrued
        #print(
        #    f"{'  Total owed:':<25}{total_owed:>10.2f}\n" +
        #    f"{'  Principal owed:':<25}{self.principal:>10.2f}\n" +
        #    f"{'  Interest accrued:':<25}{self.interest_accrued:>10.2f}"
        #)
        # Payments are first applied to accrued interest
        payment_to_interest = min(amount, self.interest_accrued)
        payment_to_principal = min(self.principal, amount - payment_to_interest)
        amount_remaining = amount - payment_to_interest - payment_to_principal

        self.interest_accrued -= payment_to_interest
        self.principal -= payment_to_principal
        #print(
        #    f"{'  Amount paid:':<25}{amount:>10.2f}\n" +
        #    f"{'  Principal paid:':<25}{payment_to_principal:>10.2f}\n" +
        #    f"{'  Interest paid:':<25}{payment_to_interest:>10.2f}\n" +
        #    f"{'  Interest remaining:':<25}{self.interest_accrued:>10.2f}\n" +
        #    f"{'  Principal remaining:':<25}{self.principal:>10.2f}"
        #)

        self.total_paid += amount - amount_remaining
        self.total_paid_interest += payment_to_interest
        self.total_paid_principal += payment_to_principal

        return payment_to_interest, payment_to_principal, amount_remaining

class Schedule:
    def __init__(self, loan: Loan, start_date: str):
        self.loan = loan
        self.start_date = start_date

    def generate_month(self, pay_amount: float, curr_date: datetime):

        while curr_date <= self.loan.due_date:
            if curr_date == self.loan.due_date:
                total_owed = self.loan.principal+self.loan.interest_accrued
                pay_amount = min(pay_amount, total_owed)
                #print(
                #    f"Payment date: {curr_date:%m-%d-%Y}"
                #)
                interest_payment, principal_payment, _ = self.loan.make_payment(pay_amount)
                total_owed = self.loan.principal+self.loan.interest_accrued
                #print(
                #    f"{'  Remaining balance:':<25}{total_owed:>10.2f}\n" +
                #    f"{'  Total amount paid:':<25}{self.loan.total_paid:>10.2f}\n" +
                #    f"{'  Total principal paid:':<25}{self.loan.total_paid_principal:>10.2f}\n" +
                #    f"{'  Total interest paid:':<25}{self.loan.total_paid_interest:>10.2f}\n"
                #)
            else:
                self.loan.accrue_interest()
            curr_date = curr_date + timedelta(days=1)

        self.loan.due_date += relativedelta(months=1)

        return curr_date

    def payoff_schedule(self, pay_amount: float):
        curr_date = datetime.fromisoformat(self.start_date)
        total_owed = self.loan.principal+self.loan.interest_accrued
        while not isclose(total_owed, 0, abs_tol=1e-2):
            # payment = min(pay_amount, self.loan.total_owed)
            curr_date = self.generate_month(pay_amount, curr_date)
            total_owed = self.loan.principal+self.loan.interest_accrued

        print(f"Pay off date: {curr_date}")
        print(f"{'Total principal paid:':<25}{self.loan.total_paid_principal:>10.2f}")
        print(f"{'Total interest paid:':<25}{self.loan.total_paid_interest:>10.2f}")
        print(f"{'Total amount paid:':<25}{self.loan.total_paid:>10.2f}")
