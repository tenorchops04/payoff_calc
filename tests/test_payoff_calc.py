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

        interest_paid, principal_paid, amount_remaining = loan.make_payment(amount = 365.25)

        self.assertEqual(loan.total_accrued_interest, 0.0)
        self.assertEqual(loan.principal, 0.0)
        self.assertEqual(interest_paid, 0)
        self.assertEqual(principal_paid, 365.25)
        self.assertEqual(amount_remaining, 0)

    def test_make_payment_all_to_principal(self):
        principal = 365.25
        min_payment = 10.0

        loan = Loan(
            principal = principal,
            term = 12,
            interest_rate = 1.0,
            loan_payment = min_payment
        )

        interest_paid, principal_paid, amount_remaining = loan.make_payment(amount = min_payment)

        self.assertEqual(loan.total_accrued_interest, 0.0)
        self.assertEqual(loan.principal, principal - min_payment)
        self.assertEqual(interest_paid, 0)
        self.assertEqual(principal_paid, min_payment)
        self.assertEqual(amount_remaining, 0)

    def test_make_payment_min_all_to_interest(self):
        principal = 365.25
        min_payment = 10.0
        accrued_interest = 30.0

        loan = Loan(
            principal = principal,
            term = 12,
            interest_rate = 1.0,
            loan_payment = min_payment
        )
        loan.total_accrued_interest = accrued_interest

        interest_paid, principal_paid, amount_remaining = loan.make_payment(amount = min_payment)

        self.assertEqual(loan.total_accrued_interest, accrued_interest-min_payment)
        self.assertEqual(loan.principal, principal)
        self.assertEqual(interest_paid, min_payment)
        self.assertEqual(principal_paid, 0)
        self.assertEqual(amount_remaining, 0)

    def test_make_payment_principal_and_interest(self):
        principal = 365.25
        min_payment = 10.0
        accrued_interest = 30.0
        amount_paid = 50.0

        loan = Loan(
            principal = principal,
            term = 12,
            interest_rate = 1.0,
            loan_payment = min_payment
        )
        loan.total_accrued_interest = accrued_interest

        interest_paid, principal_paid, amount_remaining = loan.make_payment(amount = amount_paid)

        expected_interest_paid = accrued_interest
        expected_principal_paid = amount_paid-accrued_interest

        self.assertEqual(loan.total_accrued_interest, accrued_interest - expected_interest_paid)
        self.assertEqual(loan.principal, principal-expected_principal_paid)
        self.assertEqual(interest_paid, expected_interest_paid)
        self.assertEqual(principal_paid, expected_principal_paid)
        self.assertEqual(amount_remaining, 0)

    def test_make_payment_negative_amount(self):
        principal = 365.25
        min_payment = 10.0
        accrued_interest = 30.0
        amount_paid = -50.0

        loan = Loan(
            principal = principal,
            term = 12,
            interest_rate = 1.0,
            loan_payment = min_payment
        )
        loan.total_accrued_interest = accrued_interest

        with self.assertRaises(ValueError):
            interest_paid, principal_paid, amount_remaining = loan.make_payment(amount = amount_paid)

    def test_make_payment_overpayment(self):
        principal = 365.25
        min_payment = 10.0
        accrued_interest = 30.0
        amount_paid = 400.0

        loan = Loan(
            principal = principal,
            term = 12,
            interest_rate = 1.0,
            loan_payment = min_payment
        )
        loan.total_accrued_interest = accrued_interest

        interest_paid, principal_paid, amount_remaining = loan.make_payment(amount = amount_paid)

        expected_interest_paid = accrued_interest
        expected_principal_paid = principal
        expected_amount_remaining = amount_paid - (principal + accrued_interest)

        self.assertEqual(loan.total_accrued_interest, accrued_interest - expected_interest_paid)
        self.assertEqual(loan.principal, principal-expected_principal_paid)
        self.assertEqual(interest_paid, expected_interest_paid)
        self.assertEqual(principal_paid, expected_principal_paid)
        self.assertEqual(amount_remaining, expected_amount_remaining)

    def test_make_payment_zero_amount(self):
        principal = 365.25
        min_payment = 10.0
        accrued_interest = 30.0
        amount_paid = 0.0

        loan = Loan(
            principal = principal,
            term = 12,
            interest_rate = 1.0,
            loan_payment = min_payment
        )
        loan.total_accrued_interest = accrued_interest

        interest_paid, principal_paid, amount_remaining = loan.make_payment(amount = amount_paid)

        expected_interest_paid = 0
        expected_principal_paid = 0
        expected_amount_remaining = 0

        self.assertEqual(loan.total_accrued_interest, accrued_interest - expected_interest_paid)
        self.assertEqual(loan.principal, principal-expected_principal_paid)
        self.assertEqual(interest_paid, expected_interest_paid)
        self.assertEqual(principal_paid, expected_principal_paid)
        self.assertEqual(amount_remaining, expected_amount_remaining)

