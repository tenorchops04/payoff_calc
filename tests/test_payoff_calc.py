import unittest

from uuid import uuid4
from payoff_calc import Loan, Schedule

class TestPayoffCalc(unittest.TestCase):
    def setUp(self):
        pass

    def test_accrue_interest_default(self):
        loan = Loan(
            principal = 365.25,
            term = 12,
            interest_rate = 1.0,
            loan_payment = 10.0,
            borrower_id = str(uuid4())
        )

        interest_accrued = loan.accrue_interest()

        self.assertEqual(loan.total_accrued_interest, 1.0)
        self.assertEqual(interest_accrued, 1.0)

    def test_accrue_interest_mult_days(self):
        loan = Loan(
            principal = 365.25,
            term = 12,
            interest_rate = 1.0,
            loan_payment = 10.0,
            borrower_id = str(uuid4())
        )

        interest_accrued = loan.accrue_interest(days = 5)

        self.assertEqual(loan.total_accrued_interest, 5.0)
        self.assertEqual(interest_accrued, 5.0)

    def test_make_payment(self):
        amount_paid = 365.25

        loan = Loan(
            principal = 365.25,
            term = 12,
            interest_rate = 1.0,
            loan_payment = 10.0,
            borrower_id = str(uuid4())
        )

        accrued_interest = loan.total_accrued_interest

        interest_paid, principal_paid, amount_remaining = loan.make_payment(amount = amount_paid)

        expected_interest_paid = accrued_interest
        expected_principal_paid = amount_paid-accrued_interest

        self.assertEqual(loan.total_accrued_interest, 0.0)
        self.assertEqual(loan.principal, 0.0)

        self.assertEqual(loan.total_paid, amount_paid)
        self.assertEqual(loan.total_paid_interest, expected_interest_paid)
        self.assertEqual(loan.total_paid_principal, expected_principal_paid)

        self.assertEqual(interest_paid, expected_interest_paid)
        self.assertEqual(principal_paid, amount_paid)
        self.assertEqual(amount_remaining, 0)

    def test_make_payment_all_to_principal(self):
        principal = 365.25
        min_payment = 10.0
        amount_paid = min_payment

        loan = Loan(
            principal = principal,
            term = 12,
            interest_rate = 1.0,
            loan_payment = min_payment,
            borrower_id = str(uuid4())
        )
        accrued_interest = loan.total_accrued_interest

        interest_paid, principal_paid, amount_remaining = loan.make_payment(amount = amount_paid)

        expected_interest_paid = accrued_interest
        expected_principal_paid = amount_paid-accrued_interest

        self.assertEqual(loan.total_accrued_interest, 0.0)
        self.assertEqual(loan.principal, principal - min_payment)

        self.assertEqual(loan.total_paid, amount_paid)
        self.assertEqual(loan.total_paid_interest, expected_interest_paid)
        self.assertEqual(loan.total_paid_principal, expected_principal_paid)

        self.assertEqual(interest_paid, 0)
        self.assertEqual(principal_paid, min_payment)
        self.assertEqual(amount_remaining, 0)

    def test_make_payment_min_all_to_interest(self):
        principal = 365.25
        min_payment = 10.0
        accrued_interest = 30.0
        amount_paid = min_payment

        loan = Loan(
            principal = principal,
            term = 12,
            interest_rate = 1.0,
            loan_payment = min_payment,
            borrower_id = str(uuid4())
        )
        loan.total_accrued_interest = accrued_interest

        interest_paid, principal_paid, amount_remaining = loan.make_payment(amount = min_payment)

        expected_interest_paid = amount_paid
        expected_principal_paid = amount_paid - expected_interest_paid

        self.assertEqual(loan.total_accrued_interest, accrued_interest-min_payment)
        self.assertEqual(loan.principal, principal)

        self.assertEqual(loan.total_paid, amount_paid)
        self.assertEqual(loan.total_paid_interest, expected_interest_paid)
        self.assertEqual(loan.total_paid_principal, expected_principal_paid)

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
            loan_payment = min_payment,
            borrower_id = str(uuid4())
        )
        loan.total_accrued_interest = accrued_interest

        interest_paid, principal_paid, amount_remaining = loan.make_payment(amount = amount_paid)

        expected_interest_paid = accrued_interest
        expected_principal_paid = amount_paid-accrued_interest

        self.assertEqual(loan.total_accrued_interest, accrued_interest - expected_interest_paid)
        self.assertEqual(loan.principal, principal-expected_principal_paid)

        self.assertEqual(loan.total_paid, amount_paid)
        self.assertEqual(loan.total_paid_interest, expected_interest_paid)
        self.assertEqual(loan.total_paid_principal, expected_principal_paid)

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
            loan_payment = min_payment,
            borrower_id = str(uuid4())
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
            loan_payment = min_payment,
            borrower_id = str(uuid4())
        )
        loan.total_accrued_interest = accrued_interest

        interest_paid, principal_paid, amount_remaining = loan.make_payment(amount = amount_paid)

        expected_interest_paid = accrued_interest
        expected_principal_paid = principal
        expected_amount_remaining = amount_paid - (principal + accrued_interest)

        self.assertEqual(loan.total_accrued_interest, accrued_interest - expected_interest_paid)
        self.assertEqual(loan.principal, principal-expected_principal_paid)

        self.assertEqual(loan.total_paid, amount_paid)
        self.assertEqual(loan.total_paid_interest, expected_interest_paid)
        self.assertEqual(loan.total_paid_principal, expected_principal_paid)

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
            loan_payment = min_payment,
            borrower_id = str(uuid4())
        )
        loan.total_accrued_interest = accrued_interest

        interest_paid, principal_paid, amount_remaining = loan.make_payment(amount = amount_paid)

        expected_interest_paid = 0
        expected_principal_paid = 0
        expected_amount_remaining = 0

        self.assertEqual(loan.total_accrued_interest, accrued_interest - expected_interest_paid)
        self.assertEqual(loan.principal, principal-expected_principal_paid)

        self.assertEqual(loan.total_paid, amount_paid)
        self.assertEqual(loan.total_paid_interest, expected_interest_paid)
        self.assertEqual(loan.total_paid_principal, expected_principal_paid)

        self.assertEqual(interest_paid, expected_interest_paid)
        self.assertEqual(principal_paid, expected_principal_paid)
        self.assertEqual(amount_remaining, expected_amount_remaining)

    def test_schedule(self):
        principal = 10000
        term = 36
        interest_rate = 0.10
        loan_payment = 100
        due_date = "2026-02-01"
        borrower_id = str(uuid4())

        loan = Loan(
            principal=principal,
            term=term,
            interest_rate=interest_rate,
            loan_payment=loan_payment,
            due_date=due_date,
            borrower_id=borrower_id
        )

        start_date = "2026-01-01"
        pay_amount = 100

        schedule = Schedule(
            loan=loan,
            start_date=start_date
        )

        schedule.generate_month(pay_amount=pay_amount)

        expected_total_paid = pay_amount
        self.assertEqual(loan.total_paid, expected_total_paid)

        expected_total_paid_interest = (principal*interest_rate) / 365.25 * 31
        self.assertAlmostEqual(loan.total_paid_interest, expected_total_paid_interest)

        expected_total_paid_principal = pay_amount - expected_total_paid_interest
        self.assertAlmostEqual(loan.total_paid_principal, expected_total_paid_principal)

    def test_payoff_schedule(self):
        principal = 9606.71
        term = 36
        interest_rate = 0.0503
        loan_payment = 100
        due_date = "2026-06-05"
        borrower_id = str(uuid4())

        loan = Loan(
            principal=principal,
            term=term,
            interest_rate=interest_rate,
            loan_payment=loan_payment,
            due_date=due_date,
            borrower_id=borrower_id
        )

        start_date = "2026-05-06"
        pay_amount = 1205.40

        schedule = Schedule(
            loan=loan,
            start_date=start_date
        )

        schedule.payoff_schedule(pay_amount=pay_amount)


