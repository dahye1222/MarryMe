# financial_products/utils.py

def calculate_equal_installment(principal, annual_rate, months):
    """원리금균등상환 방식"""
    monthly_rate = annual_rate / 12 / 100
    if monthly_rate == 0:
        monthly_payment = principal / months
    else:
        monthly_payment = (principal * monthly_rate * (1 + monthly_rate) ** months) / \
                          ((1 + monthly_rate) ** months - 1)
    total_payment = monthly_payment * months
    total_interest = total_payment - principal
    return round(total_payment), principal, round(total_interest)


def calculate_equal_principal(principal, annual_rate, months):
    """원금균등상환 방식"""
    monthly_principal = principal / months
    total_payment = 0
    for i in range(months):
        interest = (principal - monthly_principal * i) * (annual_rate / 12 / 100)
        total_payment += monthly_principal + interest
    total_interest = total_payment - principal
    return round(total_payment), principal, round(total_interest)


def calculate_maturity_lump_sum(principal, annual_rate, months):
    """만기일시상환 방식"""
    monthly_interest = principal * (annual_rate / 100) / 12
    total_interest = monthly_interest * months
    total_payment = principal + total_interest
    return round(total_payment), principal, round(total_interest)
