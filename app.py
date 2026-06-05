import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

st.set_page_config(
    page_title="Professional Loan EMI Calculator",
    page_icon="💰",
    layout="wide"
)

# CSS
st.markdown("""
<style>
.title {
    text-align:center;
    color:#1E3A8A;
    font-size:42px;
    font-weight:bold;
}

.subtitle {
    text-align:center;
    color:gray;
    font-size:18px;
}

.result-box {
    background-color:white;
    padding:20px;
    border-radius:10px;
    border:1px solid #ddd;
    color:black;
    box-shadow:0px 4px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">💰 Loan EMI Calculator</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Professional FinTech Project</p>', unsafe_allow_html=True)

st.write("---")

# Inputs
loan_amount = st.sidebar.number_input("Loan Amount", 1000.0, value=100000.0)
interest_rate = st.sidebar.number_input("Interest Rate (%)", 0.0, value=12.0)
years = st.sidebar.number_input("Tenure (Years)", 1.0, value=5.0)

# PDF Class
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(200, 10, "Loan EMI Report", ln=True, align="C")

if st.sidebar.button("🚀 Calculate EMI"):

    r = interest_rate / (12 * 100)
    n = int(years * 12)

    emi = (loan_amount*r*(1+r)**n)/((1+r)**n - 1) if r != 0 else loan_amount/n

    balance = loan_amount
    interest_list = []
    principal_list = []
    month_list = []

    for m in range(1, n+1):
        interest = balance * r
        principal = emi - interest
        balance -= principal

        interest_list.append(interest)
        principal_list.append(principal)
        month_list.append(m)

    # Metrics
    st.success("Calculation Done!")

    col1, col2, col3 = st.columns(3)

    col1.metric("Monthly EMI", f"Rs {emi:,.2f}")
    col2.metric("Total Payment", f"Rs {emi*n:,.2f}")
    col3.metric("Total Interest", f"Rs {(emi*n)-loan_amount:,.2f}")

    # 📊 GRAPH
    st.subheader("📊 EMI Breakdown Chart")

    fig, ax = plt.subplots()
    ax.plot(month_list[:12], interest_list[:12], label="Interest")
    ax.plot(month_list[:12], principal_list[:12], label="Principal")

    ax.set_xlabel("Month")
    ax.set_ylabel("Amount")
    ax.legend()

    st.pyplot(fig)

    # 📥 PDF DOWNLOAD
    st.subheader("📥 Download Report")

    if st.button("Generate PDF"):

        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt=f"Loan Amount: {loan_amount}", ln=True)
        pdf.cell(200, 10, txt=f"Interest Rate: {interest_rate}", ln=True)
        pdf.cell(200, 10, txt=f"Tenure: {years} years", ln=True)
        pdf.cell(200, 10, txt=f"Monthly EMI: {emi:.2f}", ln=True)

        file_path = "loan_report.pdf"
        pdf.output(file_path)

        with open(file_path, "rb") as f:
            st.download_button(
                "⬇ Download PDF",
                f,
                file_name="loan_report.pdf"
            )
