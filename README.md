# BFSI Chatbot - Agentic AI for Personal Loan Sales

## 1. Overview
The **BFSI Chatbot** is an Agentic AI solution designed to simulate an intelligent loan officer for Non-Banking Financial Companies (NBFCs).  
It automates the personal loan process—from customer engagement and KYC verification to credit evaluation and sanction letter generation—through a conversational interface.  

The chatbot is designed to handle multiple customers simultaneously and maintain context throughout the interaction. It provides a personalized, human-like experience by dynamically responding to user inputs, evaluating eligibility, and guiding applicants through each step of the loan process.  
This system demonstrates how modular AI agents can collaboratively deliver complex financial services efficiently while ensuring compliance with predefined business rules.

Developed for **EY Techathon 6.0 – Challenge II: BFSI (Tata Capital)**, it showcases how Agentic AI principles can improve operational efficiency, reduce processing time, and enhance the digital customer experience.



## 2. Objective
- Build an **Agentic AI framework** for conversational loan processing.  
- Use a **Master Agent** to orchestrate multiple Worker Agents.  
- Simulate real-world BFSI operations, including KYC, underwriting, and sanctioning.  
- Demonstrate transparency and rule-based automation in financial decision-making.



## 3. Architecture & Workflow
The BFSI Chatbot is a **multi-agent system** coordinated by a **Master Agent**:

- **Master Agent:** Maintains conversation context, interprets user input, and orchestrates the workflow.  
- **Sales Agent:** Proposes pre-approved or custom loan offers and collects requested amounts.  
- **Verification Agent:** Validates KYC details, ensuring essential information is present and accurate.  
- **Underwriting Agent:** Evaluates eligibility based on credit score, requested loan amount, and salary verification. It approves, conditionally approves, or rejects loans using EMI calculations.  
- **Sanction Agent:** Generates a PDF sanction letter for approved loans.  

The process is sequential and context-aware:
1. **SalesAgent** presents loan offers and captures user input.  
2. **VerificationAgent** validates KYC information.  
3. **UnderwritingAgent** assesses creditworthiness and salary-based EMI feasibility.  
4. **SanctionAgent** generates the official sanction letter if approved.  
5. **MasterAgent** concludes the conversation and provides the final outcome.



## 4. Project Structure

```

bfsi_chatbot/
│
├── app.py                           # Main entry point
├── requirements.txt                 # Dependency list
│
├── agent/
│   ├── master_agent.py              # Central orchestrator
│   ├── sales_agent.py               # Loan proposal logic
│   ├── verification_agent.py        # KYC validation
│   ├── underwriting_agent.py        # Credit and EMI evaluation
│   ├── sanction_agent.py            # PDF sanction generation
│
├── fonts/
│   └── DejaVuSans.ttf               # Font for PDF generation
│
├── outputs/
│   └── sanction_<customer>.pdf      # Generated sanction letters
│
└── README.md                        # Project documentation

````



## 5. Core Logic

### Loan Evaluation Criteria
- **Approved:** Loan ≤ pre-approved limit  
- **Conditionally Approved:** Loan ≤ 2× pre-approved limit (requires salary verification)  
- **Rejected:** Loan > 2× pre-approved limit or credit score < 700  

### EMI Calculation
The EMI is calculated as:

$$
EMI = \frac{P \times r \times (1 + r)^n}{(1 + r)^n - 1}
$$

where:  
- $$\(P\)$$ = Principal loan amount  
- $$\(r\)$$ = Monthly interest rate  
- $$\(n\)$$ = Loan tenure (in months)  

Approval is granted only if **EMI ≤ 50% of the applicant’s monthly salary**.



## 6. Installation & Setup

### Step 1: Clone Repository
```bash
git clone https://github.com/<your-username>/bfsi_chatbot.git
cd bfsi_chatbot
````

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Chatbot

```bash
python app.py
```



## 7. Sample Outputs

### Accepted Loan Case

Customer meets credit and salary requirements.

<img width="825" height="669" alt="Image" src="https://github.com/user-attachments/assets/829f6ee6-ad07-47ca-892a-44de3cdeb9ff" />


### Rejected Loan Case

Customer exceeds eligibility criteria (EMI or credit score).

<img width="838" height="485" alt="Image" src="https://github.com/user-attachments/assets/3594a078-2ed5-401c-9673-6e16d329ad99" />


## 8. Conclusion

The BFSI Chatbot demonstrates a **modular Agentic AI framework** for personal loan processing.
By coordinating multiple worker agents under a Master Agent, it replicates real-world BFSI operations efficiently and transparently.
The system can be extended to other financial products or integrated with real-time APIs for production deployment.
