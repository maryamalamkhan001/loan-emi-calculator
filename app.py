import streamlit as st
import matplotlib.pyplot as plt
from fpdf import FPDF

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Loan EMI Calculator",
    page_icon="💰",
    layout="wide"
)

# ---------------- HEADER ----------------
st.markdown(
    "<h1 style='text-align:center;color:#FFFFFF;'>💰 Loan EMI Calculator</h1>",
    unsafe_allow_html=True
)

st.write("---")

# ---------------- SIDEBAR ----------------
st.sidebar.header("📋 Loan Details")

loan_amount = st.sidebar.number_input("Loan Amount (Rs)", 1000.0, value=100000.0)
interest_rate = st.sidebar.number_input("Interest Rate (%)", 0.0, value=12.0)
years = st.sidebar.number_input("Tenure (Years)", 1.0, value=5.0)

loan_amount = float(loan_amount)
interest_rate = float(interest_rate)
years_int = int(years)

# ---------------- SESSION ----------------
if "calculated" not in st.session_state:
    st.session_state.calculated = False

# ---------------- CALCULATION ----------------
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

# ---------------- DASHBOARD ----------------
if st.session_state.calculated:

    st.write("## 📊 Dashboard Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="background:#0F172A;color:white;padding:20px;border-radius:12px;text-align:center;">
        💰<h2>Rs {st.session_state.emi:,.0f}</h2>
        <p>Monthly EMI</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background:#0F172A;color:white;padding:20px;border-radius:12px;text-align:center;">
        📊<h2>Rs {st.session_state.total_payment:,.0f}</h2>
        <p>Total Payment</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="background:#0F172A;color:white;padding:20px;border-radius:12px;text-align:center;">
        📌<h2>Rs {st.session_state.total_interest:,.0f}</h2>
        <p>Total Interest</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")

    # ---------------- CHART ----------------
    st.subheader("📈 EMI Breakdown (First 12 Months)")

    fig, ax = plt.subplots()
    ax.plot(st.session_state.month_list[:12], st.session_state.interest_list[:12], label="Interest")
    ax.plot(st.session_state.month_list[:12], st.session_state.principal_list[:12], label="Principal")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount")
    ax.legend()

    st.pyplot(fig)

    # ---------------- LOAN SUMMARY ----------------
    st.subheader("📄 Loan Summary")

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #0F172A, #1E293B);
            padding: 22px;
            border-radius: 14px;
            color: white;
            box-shadow: 0px 8px 20px rgba(0,0,0,0.35);
            line-height: 2;
            font-size: 16px;
        ">
            <h3 style="color:#38BDF8; margin-bottom:10px;">📄 Loan Information</h3>
            <hr style="border: 0.5px solid #334155; margin-bottom:12px;">
            💰 <b>Loan Amount:</b> Rs {st.session_state.loan_amount:,.0f} <br>
            📊 <b>Interest Rate:</b> {st.session_state.interest_rate:.2f}% <br>
            📅 <b>Loan Tenure:</b> {st.session_state.years} Years <br>
            ⏳ <b>Total Months:</b> {st.session_state.n} <br>
            📌 <b>Total Interest:</b> Rs {st.session_state.total_interest:,.2f} <br>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- PDF ----------------
    st.write("")
    st.subheader("📥 Download Report")

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
st.caption("👩‍💻 FinTech Dashboard | Streamlit Project")
