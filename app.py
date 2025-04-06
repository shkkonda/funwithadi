import streamlit as st
from forex_python.converter import CurrencyRates
def calculate_tax_2025(salary, business=False):
    tax_slabs = [
        (400000, 0.00),
        (800000, 0.05),
        (1200000, 0.10),
        (1600000, 0.15),
        (2000000, 0.20),
        (2400000, 0.25),
        (float('inf'), 0.30)
    ]
    rebate = 60000
    standard_deduction = 75000
    if business:
        salary /= 2 
    taxable_income = max(0, salary - standard_deduction)
    if taxable_income <= 1200000:
        return 0, 0, 0, 0  
    tax, prev_limit = 0, 400000
    for limit, rate in tax_slabs[1:]:
        if taxable_income > 0:
            slab_amount = min(taxable_income, limit - prev_limit)
            tax += slab_amount * rate
            taxable_income -= slab_amount
            prev_limit = limit
        else:
            break
    surcharge = 0
    if taxable_income > 5000000:
        if taxable_income <= 10000000:
            surcharge = tax * 0.10
        elif taxable_income <= 20000000:
            surcharge = tax * 0.15
        elif taxable_income <= 50000000:
            surcharge = tax * 0.25
        else:
            surcharge = tax * 0.37
    cess = (tax + surcharge) * 0.04
    total_tax = tax + surcharge + cess
    return round(tax, 2), round(surcharge, 2), round(cess, 2), round(total_tax, 2)
def calculate_ctc(desired_inhand):
    return round(desired_inhand / 0.5, 2) 
st.title("Tax Calculator with 44ADA Comparison")
salary_input = st.number_input("Enter your Salary/Package", min_value=0.0, step=1000.0)
frequency = st.selectbox("Salary Frequency", ["Annual", "Monthly"])
currency = st.selectbox("Currency", ["INR", "USD"])
business = st.checkbox("Apply 44ADA Method (50% Taxable)")
desired_inhand = None
if business:
    desired_inhand = st.number_input("Desired In-hand Amount (Annual)", min_value=0.0, step=1000.0)
conversion_rate = 1
if currency == "USD":
    try:
        conversion_rate = CurrencyRates().get_rate('USD', 'INR')
    except:
        conversion_rate = 83  
    salary_input *= conversion_rate
tax_std, surcharge_std, cess_std, total_tax_std = calculate_tax_2025(salary_input, business=False)
tax_44ada, surcharge_44ada, cess_44ada, total_tax_44ada = calculate_tax_2025(salary_input, business=True)
inhand_std = salary_input - total_tax_std
inhand_44ada = salary_input - total_tax_44ada
required_ctc = calculate_ctc(desired_inhand) if business and desired_inhand else None
st.subheader("Tax Calculation Results")
col1, col2 = st.columns(2)
with col1:
    st.write("### Standard Salary Calculation")
    st.write(f"**Tax:** ₹{tax_std}")
    st.write(f"**Surcharge:** ₹{surcharge_std}")
    st.write(f"**Cess:** ₹{cess_std}")
    st.write(f"**Total Tax:** ₹{total_tax_std}")
    st.write(f"**In-hand Amount (Annual):** ₹{inhand_std}")
    st.write(f"**In-hand Amount (Monthly):** ₹{inhand_std / 12:.2f}")
with col2:
    st.write("### 44ADA Calculation")
    st.write(f"**Tax:** ₹{tax_44ada}")
    st.write(f"**Surcharge:** ₹{surcharge_44ada}")
    st.write(f"**Cess:** ₹{cess_44ada}")
    st.write(f"**Total Tax:** ₹{total_tax_44ada}")
    st.write(f"**In-hand Amount (Annual):** ₹{inhand_44ada}")
    st.write(f"**In-hand Amount (Monthly):** ₹{inhand_44ada / 12:.2f}")
if business and required_ctc:
    st.subheader("Required CTC for Desired In-hand Amount")
    st.write(f"**Required CTC:** ₹{required_ctc}")
