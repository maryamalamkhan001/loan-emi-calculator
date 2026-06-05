import streamlit as st
import matplotlib.pyplot as plt
from fpdf import FPDF

st.set_page_config(
    page_title="Professional Loan EMI Calculator",
    page_icon="💰",
    layout="wide"
)

# ---------------- UI ----------------
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

# ---------------- INPUTS ----------------
st.sidebar.header("📋 Loan Details")

loan_amount = st.sidebar.number_input("Loan Amount (Rs)", 1000.0, value=100000.0)
interest_rate = st.sidebar.number_input("Interest Rate (%)", 0.0, value=12.0)
years = st.sidebar.number_input("Tenure (Years)", 1.0, value=5.0)

# FIX: clean values (no decimals in UI)
loan_amount = float(loan_amount)
interest_rate = float(interest_rate)
years_int = int(years)

# ---------------- SESSION STATE ----------------
if "calculated" not in st.session_state:
    st.session_state.calculated = False

if st.sidebar.button("🚀 Calculate EMI"):

    r = interest_rate / (12 * 100)
    n = years_int * 12

    emi = (loan_amount * r * (1 + r) ** n) / ((1 + r) ** n - 1) if r != 0 else loan_amount / n

    balance = loan_amount
    interest_list = []
    principal_list = []
    month_list = []

    for m in range(1, n + 1):
        interest = balance * r
        principal = emi - interest
        balance -= principal

        interest_list.append(interest)
        principal_list.append(principal)
        month_list.append(m)

    # SAVE DATA
    st.session_state.calculated = True
    st.session_state.emi = emi
    st.session_state.total_payment = emi * n
    st.session_state.total_interest = (emi * n) - loan_amount
    st.session_state.loan_amount = loan_amount
    st.session_state.interest_rate = interest_rate
    st.session_state.years = years_int
    st.session_state.n = n
    st.session_state.month_list = month_list
    st.session_state.interest_list = interest_list
    st.session_state.principal_list = principal_list

    st.success("✅ Calculation Completed Successfully!")

# ---------------- SHOW RESULTS ----------------
if st.session_state.calculated:

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Monthly EMI", f"Rs {st.session_state.emi:,.2f}")
    col2.metric("📊 Total Payment", f"Rs {st.session_state.total_payment:,.2f}")
    col3.metric("📌 Total Interest", f"Rs {st.session_state.total_interest:,.2f}")

    st.write("---")

    # ---------------- GRAPH ----------------
    st.subheader("📊 EMI Breakdown Chart")

    fig, ax = plt.subplots()
    ax.plot(st.session_state.month_list[:12], st.session_state.interest_list[:12], label="Interest")
    ax.plot(st.session_state.month_list[:12], st.session_state.principal_list[:12], label="Principal")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount")
    ax.legend()

    st.pyplot(fig)

    # ---------------- SUMMARY ----------------
    st.subheader("📊 Loan Summary")

    st.markdown(f"""
    <div class="result-box">
        <h4>Loan Information</h4>
        <hr>

        <b>Loan Amount:</b> Rs {st.session_state.loan_amount:,.0f}<br><br>
        <b>Interest Rate:</b> {st.session_state.interest_rate:.2f}%<br><br>
        <b>Loan Tenure:</b> {st.session_state.years} Years<br><br>
        <b>Total Months:</b> {st.session_state.n}<br><br>
        <b>Total Interest:</b> Rs {st.session_state.total_interest:,.2f}<br>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- PDF ----------------
    st.subheader("📥 Download Report (PDF)")

    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 14)
            self.cell(200, 10, "Loan EMI Report", ln=True, align="C")

    if st.button("Generate PDF"):

        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt=f"Loan Amount: Rs {st.session_state.loan_amount:,.0f}", ln=True)
        pdf.cell(200, 10, txt=f"Interest Rate: {st.session_state.interest_rate:.2f}%", ln=True)
        pdf.cell(200, 10, txt=f"Tenure: {st.session_state.years} Years", ln=True)
        pdf.cell(200, 10, txt=f"Monthly EMI: Rs {st.session_state.emi:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Total Payment: Rs {st.session_state.total_payment:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Total Interest: Rs {st.session_state.total_interest:.2f}", ln=True)

        pdf_bytes = pdf.output(dest="S").encode("latin-1")

        st.download_button(
            label="⬇ Download PDF",
            data=pdf_bytes,
            file_name="loan_report.pdf",
            mime="application/pdf"
        )

st.write("---")
st.caption("👩‍💻 Developed by Alishba Qureshi | BS FinTech Student")
