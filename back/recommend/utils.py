from datetime import date
import pandas as pd
from accounts.models import User
from financial_products.models import DepositOption, SavingOption, LoanProduct

def calculate_age(birth_date):
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

# 예금 추천 함수수
def recommend_deposit_options(user):
    user_age = calculate_age(user.birth_date)

    all_users = User.objects.exclude(id=user.id).exclude(birth_date=None).values('id', 'birth_date', 'salary', 'wealth')
    df = pd.DataFrame(list(all_users))

    if df.empty:
        return fallback_deposit_options()

    df['age'] = df['birth_date'].apply(calculate_age)
    df['age_diff'] = abs(df['age'] - user_age)
    df['salary_diff'] = abs(df['salary'] - user.salary)
    df['wealth_diff'] = abs(df['wealth'] - user.wealth)
    df['total_diff'] = df['age_diff'] + df['salary_diff'] + df['wealth_diff']

    similar_users = df.sort_values(by='total_diff').head(20)

    option_counter = {}
    for uid in similar_users['id']:
        u = User.objects.get(id=uid)
        for opt in u.wishlist_deposits_options.all():
            option_counter[opt.id] = option_counter.get(opt.id, 0) + 1

    if option_counter:
        top_ids = sorted(option_counter, key=option_counter.get, reverse=True)[:3]
        return DepositOption.objects.select_related('deposit_product').filter(id__in=top_ids)
    return fallback_deposit_options()

def fallback_deposit_options():
    option_counter = {}
    for u in User.objects.all():
        for opt in u.wishlist_deposits_options.all():
            option_counter[opt.id] = option_counter.get(opt.id, 0) + 1

    if option_counter:
        top_ids = sorted(option_counter, key=option_counter.get, reverse=True)[:3]
        return DepositOption.objects.select_related('deposit_product').filter(id__in=top_ids)

    return DepositOption.objects.select_related('deposit_product').order_by('?')[:3]


# 적금 추천 함수
def recommend_saving_options(user):
    user_age = calculate_age(user.birth_date)

    all_users = User.objects.exclude(id=user.id).exclude(birth_date=None).values('id', 'birth_date', 'salary', 'wealth')
    df = pd.DataFrame(list(all_users))

    if df.empty:
        return fallback_saving_options()

    df['age'] = df['birth_date'].apply(calculate_age)
    df['age_diff'] = abs(df['age'] - user_age)
    df['salary_diff'] = abs(df['salary'] - user.salary)
    df['wealth_diff'] = abs(df['wealth'] - user.wealth)
    df['total_diff'] = df['age_diff'] + df['salary_diff'] + df['wealth_diff']

    similar_users = df.sort_values(by='total_diff').head(20)

    option_counter = {}
    for uid in similar_users['id']:
        u = User.objects.get(id=uid)
        for opt in u.wishlist_savings_options.all():
            option_counter[opt.id] = option_counter.get(opt.id, 0) + 1

    if option_counter:
        top_ids = sorted(option_counter, key=option_counter.get, reverse=True)[:3]
        return SavingOption.objects.select_related('saving_product').filter(id__in=top_ids)

    return fallback_saving_options()


def fallback_saving_options():
    option_counter = {}
    for u in User.objects.all():
        for opt in u.wishlist_savings_options.all():
            option_counter[opt.id] = option_counter.get(opt.id, 0) + 1

    if option_counter:
        top_ids = sorted(option_counter, key=option_counter.get, reverse=True)[:3]
        return SavingOption.objects.select_related('saving_product').filter(id__in=top_ids)

    return SavingOption.objects.select_related('saving_product').order_by('?')[:3]

# 대출 추천 함수
def recommend_loan_products(user):
    user_age = calculate_age(user.birth_date)

    all_users = User.objects.exclude(id=user.id).exclude(birth_date=None).values('id', 'birth_date', 'salary', 'wealth')
    df = pd.DataFrame(list(all_users))
    df['age'] = df['birth_date'].apply(calculate_age)

    df['age_diff'] = abs(df['age'] - user_age)
    df['salary_diff'] = abs(df['salary'] - user.salary)
    df['wealth_diff'] = abs(df['wealth'] - user.wealth)
    df['total_diff'] = df['age_diff'] + df['salary_diff'] + df['wealth_diff']

    similar_users = df.sort_values(by='total_diff').head(20)

    product_counter = {}
    for uid in similar_users['id']:
        u = User.objects.get(id=uid)
        for product in u.wishlist_loans.all():  # ✅ 전세대출은 LoanProduct 자체를 찜
            product_counter[product.id] = product_counter.get(product.id, 0) + 1

    top_product_ids = sorted(product_counter, key=product_counter.get, reverse=True)[:3]
    return LoanProduct.objects.filter(id__in=top_product_ids)