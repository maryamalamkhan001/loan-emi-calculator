import streamlit as st

st.set_page_config(page_title="Loan EMI Calculator", page_icon="💰")

st.title("💰 Professional Loan EMI Calculator")

loan_amount = st.number_input(
    "Enter Loan Amount (Rs)",
    min_value=1.0,
    value=100000.0
)

interest_rate = st.number_input(
    "Annual Interest Rate (%)",
    min_value=0.0,
    value=12.0
)

years = st.number_input(
    "Loan Tenure (Years)",
    min_value=1.0,
    value=5.0
)

if st.button("Calculate EMI"):

    monthly_rate = interest_rate / (12 * 100)
    months = int(years * 12)

    if monthly_rate == 0:
        emi = loan_amount / months
    else:
        emi = (
            loan_amount
            * monthly_rate
            * (1 + monthly_rate) ** months
        ) / (
            (1 + monthly_rate) ** months - 1
        )

    total_payment = emi * months
    total_interest = total_payment - loan_amount

    st.success("Calculation Completed!")

    st.metric("Monthly EMI", f"Rs {emi:,.2f}")
    st.metric("Total Payment", f"Rs {total_payment:,.2f}")
    st.metric("Total Interest", f"Rs {total_interest:,.2f}")

    st.write("---")
    st.subheader("Loan Summary")

    st.write(f"**Loan Amount:** Rs {loan_amount:,.2f}")
    st.write(f"**Interest Rate:** {interest_rate}%")
    st.write(f"**Tenure:** {years} Years")
