import re
from agents.sales_agent import SalesAgent
from agents.verification_agent import VerificationAgent
from agents.underwriting_agent import UnderwritingAgent
from agents.sanction_agent import generate_sanction_letter

class MasterAgent:
    def __init__(self):
        self.sales_agent = SalesAgent()
        self.verification_agent = VerificationAgent()
        self.underwriting_agent = UnderwritingAgent()

    def parse_loan_amount(self, user_input, pre_approved_limit):
        """
        Convert user input into numeric loan amount.
        Accepts commas, spaces, Rs./₹, k suffix.
        Returns float or None if invalid.
        """
        ui = user_input.lower().replace('rs.', '').replace('₹','').strip()
        ui = ui.replace(',', '').replace(' ', '')

        # Handle k or K suffix (350k → 350000)
        m = re.match(r'^(\d+(\.\d+)?)(k)?$', ui)
        if m:
            amount = float(m.group(1))
            if m.group(3):
                amount *= 1000
            return amount

        if ui == 'accept' or ui == '':
            return pre_approved_limit

        try:
            return float(ui)
        except:
            return None

    def start_chat(self, customer, user_input, context=None):
        """
        context: dict storing step, requested_amount, uploaded_salary_file etc.
        Returns: (responses_list, pdf_path_or_None, completed_flag, updated_context)
        """
        responses = []
        context = context or {}
        step = context.get('step', 0)

        # Step 0: Sales
        if step == 0:
            responses.append(self.sales_agent.propose_loan(customer))
            responses.append("Enter requested loan amount (e.g., 350000, 3,50,000, 350k) or type 'accept'.")
            context['step'] = 1
            return responses, None, False, context

        # Step 1: Verification
        if step == 1:
            responses.append(self.verification_agent.verify_kyc(customer))
            responses.append("Proceeding to credit evaluation...")
            context['step'] = 2
            return responses, None, False, context

        # Step 2: Underwriting
        if step == 2:
            if 'requested_amount' not in context:
                requested_amount = self.parse_loan_amount(user_input, customer.get('pre_approved_limit', 0))
                if requested_amount is None:
                    responses.append("Please enter a valid loan amount (e.g., 350000, 3,50,000, 350k) or type 'accept'.")
                    return responses, None, False, context
                context['requested_amount'] = requested_amount
            else:
                requested_amount = context['requested_amount']

            salary_input = user_input.strip()
            uploaded_file = context.get('uploaded_salary_file')
            status, message, approved = self.underwriting_agent.evaluate_loan(
                customer, requested_amount,
                salary_from_input=salary_input,
                uploaded_salary_file=uploaded_file
            )
            responses.append(message)

            if status == 'require_salary_slip':
                responses.append("Please upload a salary slip (PDF/JPG) or type your monthly salary.")
                context['require_salary_upload'] = True
                return responses, None, False, context
            elif status == 'approved' and approved:
                pdf_path = generate_sanction_letter(customer)
                responses.append("✅ Sanction letter generated!")
                context['step'] = 3
                return responses, pdf_path, True, context
            else:
                context['step'] = 3
                return responses, None, True, context

        # Step 3+: chat ended
        responses.append("Chat completed! Thank you for using BFSI Personal Loan Chatbot.")
        return responses, None, True, context
