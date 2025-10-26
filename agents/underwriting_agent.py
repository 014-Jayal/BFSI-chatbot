import re
import math

def fetch_credit_score_from_bureau(customer=None):
    if customer and 'credit_score' in customer:
        return customer['credit_score']
    return 700

def calculate_monthly_emi(principal, annual_interest_rate_percent, months):
    if months <= 0:
        return float('inf')
    r = annual_interest_rate_percent / 12 / 100
    if r == 0:
        return principal / months
    emi = principal * r * (1 + r)**months / ((1 + r)**months - 1)
    return emi

class UnderwritingAgent:
    def __init__(self, annual_interest=12.5, tenure_months=24):
        self.annual_interest = annual_interest
        self.tenure_months = tenure_months

    def evaluate_loan(self, customer, requested_amount, salary_from_input=None, uploaded_salary_file=None):
        credit_score = fetch_credit_score_from_bureau(customer)
        pre_limit = customer.get('pre_approved_limit', 0)

        if credit_score < 700:
            return 'rejected', f"Loan rejected due to low credit score ({credit_score}).", False

        if requested_amount <= pre_limit:
            return 'approved', "Loan within pre-approved limit. Approved.", True

        if requested_amount <= 2 * pre_limit:
            salary = None
            if salary_from_input:
                try:
                    salary = float(re.sub(r'[^\d.]','',salary_from_input))
                except: salary = None
            if not salary and uploaded_salary_file:
                m = re.search(r'(\d{4,7})', uploaded_salary_file.name)
                if m: salary = float(m.group(1))
            if not salary:
                return 'require_salary_slip', "Requested amount requires salary-slip verification. Please upload salary slip or enter monthly salary.", False

            emi = calculate_monthly_emi(requested_amount, self.annual_interest, self.tenure_months)
            if emi <= 0.5 * salary:
                return 'approved', f"Salary verified (Rs.{salary:.0f}). EMI Rs.{emi:.0f} <= 50% of salary. Loan approved.", True
            else:
                return 'rejected', f"Loan rejected: EMI Rs.{emi:.0f} exceeds 50% of salary Rs.{salary:.0f}.", False

        return 'rejected', f"Loan rejected: requested amount Rs.{requested_amount:.0f} exceeds allowable limit (2× pre-approved).", False
