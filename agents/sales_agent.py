class SalesAgent:
    def propose_loan(self, customer):
        limit = customer.get('pre_approved_limit', 0)
        return f"Based on our analysis, your pre-approved personal loan limit is Rs.{limit:.0f}. Would you like to take this loan or request a different amount?"
