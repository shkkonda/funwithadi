import streamlit as st
import requests
USD_TO_INR = 83.0
REBATE_LIMIT = 1200000
REBATE_AMOUNT = 750000
CESS_RATE = 0.04
TAX_SLABS = [
    (400000, 0.0),
    (800000, 0.05),
    (1200000, 0.10),
    (1600000, 0.15),
    (2000000, 0.20),
    (2400000, 0.25),
    (float('inf'), 0.30),
]
def convert_to_annual(salary, period):
    return salary * 12 if period == "Monthly" else salary
def convert_currency(amount, currency):
    if currency == "INR":
        return amount, 1.0
    try:
        API_KEY = '54c096a912b7517a0423c068'
        response = requests.get(f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD')
        data = response.json()
        if data['result'] == 'success':
            rate = data['conversion_rates'].get('INR')
            if rate:
                return amount * rate, rate
            else:
                st.warning("INR conversion rate not found. Using fallback.")
        else:
            st.warning(f"API Error: {data.get('error-type', 'Unknown')}. Using fallback.")
    except Exception as e:
        st.warning(f"Live currency conversion failed: {e}. Using default rate.")
    return amount * USD_TO_INR, USD_TO_INR
def calculate_taxable_income_44ada(gross):
    return gross * 0.50
def calculate_tax(income):
    tax = 0
    prev_limit = 0
    for limit, rate in TAX_SLABS:
        if income > limit:
            tax += (limit - prev_limit) * rate
            prev_limit = limit
        else:
            tax += (income - prev_limit) * rate
            break
    if income <= REBATE_LIMIT:
        tax = max(0, tax - REBATE_AMOUNT)
    cess = tax * CESS_RATE
    return tax, cess
def compute_44ada(gross):
    taxable = calculate_taxable_income_44ada(gross)
    tax, cess = calculate_tax(taxable)
    net = gross - tax - cess
    return gross, taxable, tax, cess, net
def compute_standard(gross):
    taxable = gross
    tax, cess = calculate_tax(taxable)
    net = gross - tax - cess
    return gross, taxable, tax, cess, net
def reverse_ctc_standard(desired_inhand):
    for ctc in range(int(desired_inhand), int(desired_inhand * 3)):
        gross, _, tax, cess, net = compute_standard(ctc)
        if net >= desired_inhand:
            return ctc
    return None
st.title("💰 Salary Tax Comparator: Standard vs 44ADA")
salary_input = st.number_input("Enter your Salary / Package", min_value=0.0, value=00.0)
period = st.selectbox("Select Input Type", ["Annual", "Monthly"])
currency = st.selectbox("Currency", ["INR", "USD"])
salary_inr_annual = convert_to_annual(salary_input, period)
salary_inr_annual, fx_rate = convert_currency(salary_inr_annual, currency)
if currency == "USD":
    st.info(f"💱 1 USD = ₹{fx_rate:.2f} INR (live rate)")
std_gross, std_taxable, std_tax, std_cess, std_net = compute_standard(salary_inr_annual)
ada_gross, ada_taxable, ada_tax, ada_cess, ada_net = compute_44ada(salary_inr_annual)
st.subheader("📊 Tax Breakdown")
col1, col2 = st.columns(2)
with col1:
    st.markdown("### Standard Tax Method")
    st.write(f"**Gross Income:** ₹{std_gross:,.2f}")
    st.write(f"**Taxable Income:** ₹{std_taxable:,.2f}")
    st.write(f"**Tax Payable:** ₹{std_tax:,.2f}")
    st.write(f"**Cess:** ₹{std_cess:,.2f}")
    st.write(f"**Net In-hand:** ₹{std_net:,.2f}")
    st.write(f"**Monthly In-hand:** ₹{std_net/12:,.2f}")
with col2:
    st.markdown("### 44ADA Method")
    st.write(f"**Gross Income:** ₹{ada_gross:,.2f}")
    st.write(f"**Taxable Income (50%):** ₹{ada_taxable:,.2f}")
    st.write(f"**Tax Payable:** ₹{ada_tax:,.2f}")
    st.write(f"**Cess:** ₹{ada_cess:,.2f}")
    st.write(f"**Net In-hand:** ₹{ada_net:,.2f}")
    st.write(f"**Monthly In-hand:** ₹{ada_net/12:,.2f}")
st.markdown("---")
st.subheader("🎯 Reverse CTC Calculator")
st.markdown("### Standard Method")
desired_inhand_std = st.number_input(
    "Desired In-hand (Standard)",
    min_value=0.0,
    value=ada_net,  
    key="standard"
)
required_ctc_std = reverse_ctc_standard(desired_inhand_std)
if required_ctc_std:
    st.write(f"Required CTC to get the Desired In-hand amount under Standard Method: ₹{required_ctc_std:,.2f}")
else:
    st.error("Could not compute CTC for the given in-hand amount (Standard).")
