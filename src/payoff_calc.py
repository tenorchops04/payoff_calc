class Loan:
    def __init__(
        self,
        principal: float,
        term: float,
        interest_rate: float,
        loan_payment: float
    ):
        self.principal = principal
        self.term = term
        self.interest_rate = interest_rate
        self.loan_payment = loan_payment
        self.total_accrued_interest = 0

    def accrue_interest(self, days: int = 1):
        daily_interest_accrual = (self.principal * self.interest_rate) / 365.25
        interest_accrued = daily_interest_accrual * days

        self.total_accrued_interest += interest_accrued

        return interest_accrued

    def make_payment(self, amount):
        # Payments are first applied to accrued interest
        payment_to_interest = self.total_accrued_interest % amount
        payment_to_principal = amount - payment_to_interest

        self.total_accrued_interest -= payment_to_interest
        self.principal -= payment_to_principal

        return payment_to_interest, payment_to_principal
