class VerificationAgent:
    def __init__(self, crm_server=None):
        self.crm_server = crm_server  # mock for demo
    
    def verify_kyc(self, customer):
        required = ['name', 'pre_approved_limit', 'credit_score']
        missing = [k for k in required if k not in customer]
        if missing:
            return f"KYC failed: missing fields {missing}"
        return f"KYC verified successfully for {customer['name']}."
