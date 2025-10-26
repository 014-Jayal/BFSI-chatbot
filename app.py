import streamlit as st
from agents.master_agent import MasterAgent

st.set_page_config(page_title="BFSI Personal Loan Chatbot", layout="wide")
st.title("💬 BFSI Personal Loan Chatbot")

# Dummy customers
customers = [
    {"id":1,"name":"Sahil Desai","age":22,"city":"Mumbai","current_loan":0,"credit_score":750,"pre_approved_limit":400000,"salary":70000},
    {"id":2,"name":"Rohit Sharma","age":28,"city":"Delhi","current_loan":50000,"credit_score":680,"pre_approved_limit":300000,"salary":60000},
    {"id":3,"name":"Anita Desai","age":35,"city":"Bangalore","current_loan":0,"credit_score":800,"pre_approved_limit":500000,"salary":90000},
    {"id":4,"name":"Vinai Bhat","age":30,"city":"Chennai","current_loan":100000,"credit_score":720,"pre_approved_limit":350000,"salary":50000},
    {"id":5,"name":"Neha Gupta","age":26,"city":"Pune","current_loan":0,"credit_score":790,"pre_approved_limit":450000,"salary":80000},
    {"id":6,"name":"Amit Joshi","age":40,"city":"Kolkata","current_loan":200000,"credit_score":710,"pre_approved_limit":300000,"salary":100000},
    {"id":7,"name":"Priya Nair","age":24,"city":"Hyderabad","current_loan":0,"credit_score":670,"pre_approved_limit":200000,"salary":40000},
    {"id":8,"name":"Karan Mehta","age":32,"city":"Ahmedabad","current_loan":150000,"credit_score":730,"pre_approved_limit":350000,"salary":60000},
    {"id":9,"name":"Rina Kapoor","age":29,"city":"Jaipur","current_loan":0,"credit_score":780,"pre_approved_limit":400000,"salary":70000},
    {"id":10,"name":"Suresh Patil","age":36,"city":"Surat","current_loan":50000,"credit_score":695,"pre_approved_limit":250000,"salary":50000},
]

agent = MasterAgent()

# Select customer
customer_name = st.selectbox("Select Customer", [c['name'] for c in customers])
customer = next(c for c in customers if c['name'] == customer_name)

# Session state
if 'chat_log' not in st.session_state: st.session_state.chat_log = []
if 'context' not in st.session_state: st.session_state.context = {'step':0}

# Show chat history
for m in st.session_state.chat_log:
    if m['sender'] == 'user':
        st.markdown(f"<div style='text-align:right;background-color:#DCF8C6;padding:10px;border-radius:10px;margin:5px 0'>{m['message']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align:left;background-color:#ECECEC;padding:10px;border-radius:10px;margin:5px 0'>{m['message']}</div>", unsafe_allow_html=True)

# Input handling
def send_message():
    ui = st.session_state.temp_input.strip()
    if ui == "": return

    # Append user message
    st.session_state.chat_log.append({"sender":"user","message":ui})

    # Pass to MasterAgent
    responses, pdf_path, completed, updated_context = agent.start_chat(customer, ui, context=st.session_state.context)
    st.session_state.context.update(updated_context)

    # Append agent responses
    for r in responses:
        st.session_state.chat_log.append({"sender":"agent","message":r})

    st.session_state.temp_input = ""

st.text_input("Type your message here and press Enter", key="temp_input", on_change=send_message)
st.button("Send", on_click=send_message)

# Show generated PDF
if 'pdf_path' in st.session_state and st.session_state.pdf_path:
    st.success(f"Sanction letter generated: {st.session_state.pdf_path}")
    st.write("Open the outputs folder to retrieve the PDF for your PPT screenshots.")
