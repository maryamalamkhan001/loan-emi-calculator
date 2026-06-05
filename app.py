import streamlit as st

st.set_page_config(
page_title="Professional Loan EMI Calculator",
page_icon="💰",
layout="wide"
)

# Custom CSS

st.markdown("""

<style>
.main {
    padding-top: 1rem;
}
.title {
    text-align:center;
    color:#1E3A8A;
    font-size:40px;
    font-weight:bold;
}
.subtitle {
    text-align:center;
    color:gray;
    font-size:18px;
}
.result-box {
    background-color:#f8f9fa;
    padding:20px;
    border-radius:10px;
    border:1px solid #ddd;
}
</style>

""", unsafe_allow_html=True)

# Header

st.markdown('<p class="title">💰 Professional Loan EMI Calculator</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Calculate your monthly loan installment instantly</p>', unsafe_allow_html=True)

st.write("---")

# Sidebar

st.sidebar.header("📋 Loan Details")

loan_amount = st.sidebar.number_input(
"Loan Amount (Rs)",
min_value=1000.0,
value=100000.0
)

interest_rate = st.sidebar.number_input(
"Annual Interest Rate (%)",
min_value=0.0,
value=12.0
)

years = st.sidebar.number_input(
"Loan Tenure (Years)",
min_value=1.0,
value=5.0
)

if st.sidebar.button("🚀 Calculate EMI"):

    monthly_rate = interest_rate / (12 * 100)
    months = int(years * 12)

    if monthly_rate == 0:
        emi = loan_amount / months
    else:
        emi = (
            loan_amount * monthly_rate * (1 + monthly_rate) ** months
        ) / (
            (1 + monthly_rate) ** months - 1
        )

    total_payment = emi * months
    total_interest = total_payment - loan_amount

    st.success("✅ Calculation Completed Successfully")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Monthly EMI", f"Rs {emi:,.2f}")

    with col2:
        st.metric("Total Payment", f"Rs {total_payment:,.2f}")

    with col3:
        st.metric("Total Interest", f"Rs {total_interest:,.2f}")

    st.write("")

    st.markdown("### 📊 Loan Summary")

    st.markdown(f"""
    <div class="result-box">
    <h4>Loan Information</h4>

    <b>Loan Amount:</b> Rs {loan_amount:,.2f}<br>
    <b>Interest Rate:</b> {interest_rate}%<br>
    <b>Loan Tenure:</b> {years} Years<br>
    <b>Total Months:</b> {months}<br>
    <b>Interest Percentage:</b> {(total_interest/loan_amount)*100:.2f}%<br>

    </div>
    """, unsafe_allow_html=True)

st.write("---")
st.caption("Developed by Maryam Alam Khan | BS FinTech Student")
