import os
import sys
import django
import random
from faker import Faker

# settings 경로 지정 (Django가 설정을 로드할 수 있도록)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weddingProject.settings")
django.setup()

from accounts.models import User

fake = Faker()

for i in range(100):
    username = f"user_{i}_{random.randint(1000, 9999)}"
    birth_date = fake.date_of_birth(minimum_age=20, maximum_age=60)
    salary = random.randint(3000, 20000) * 1000
    wealth = random.randint(100, 20000) * 1000

    User.objects.create_user(
        username=username,
        password="test1234",
        birth_date=birth_date,
        salary=salary,
        wealth=wealth,
    )

print("✅ 더미 유저 생성 완료!")
