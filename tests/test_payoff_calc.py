import unittest

from payoff_calc import Loan

class TestPayoffCalc(unittest.TestCase):
    def setUp(self):
        pass

    def test_accrue_interest_default(self):
        loan = Loan(
            principal = 365.25,
            term = 12,
            interest_rate = 1.0,
            loan_payment = 10.0
        )

        interest_accrued = loan.accrue_interest()

        self.assertEqual(loan.total_accrued_interest, 1.0)
        self.assertEqual(interest_accrued, 1.0)

    def test_accrue_interest_mult_days(self):
        loan = Loan(
            principal = 365.25,
            term = 12,
            interest_rate = 1.0,
            loan_payment = 10.0
        )

        interest_accrued = loan.accrue_interest(days = 5)

        self.assertEqual(loan.total_accrued_interest, 5.0)
        self.assertEqual(interest_accrued, 5.0)

    def test_make_payment(self):
        loan = Loan(
            principal = 365.25,
            term = 12,
            interest_rate = 1.0,
            loan_payment = 10.0
        )

        interest_paid, principal_paid = loan.make_payment(amount = 365.25)

        self.assertEqual(loan.total_accrued_interest, 0.0)
        self.assertEqual(loan.principal, 0.0)
        self.assertEqual(interest_paid, 0)
        self.assertEqual(principal_paid, 365.25)




