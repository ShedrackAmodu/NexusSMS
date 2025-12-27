"""Quick test script to verify student and employee ID generation.

Run with:

    python scripts/test_sequence_ids.py

It will bootstrap Django, create a test institution (if missing),
create a student user and a staff user, then print generated IDs.
"""

import os
import sys
import django
from datetime import date

# Ensure project root is on PYTHONPATH so `config` package can be imported
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
try:
    django.setup()
except Exception as e:
    raise RuntimeError(
        "Django setup failed — ensure you're running this from the project root and the virtualenv is activated."
    ) from e

from apps.core.models import Institution, SequenceGenerator
from apps.academics.models import Student
from apps.users.models import User, generate_employee_id


def main():
    inst, created = Institution.objects.get_or_create(
        code="SCH1",
        defaults={
            "name": "School One",
            "institution_type": "high_school",
            "ownership_type": "private",
        },
    )

    print("Institution:", inst.code)

    # Ensure sequence rows exist
    SequenceGenerator.objects.get_or_create(
        sequence_type=SequenceGenerator.SequenceType.STUDENT_ID,
        institution=inst,
        defaults={"prefix": f"{inst.code}-STU-", "padding": 3},
    )
    SequenceGenerator.objects.get_or_create(
        sequence_type=SequenceGenerator.SequenceType.EMPLOYEE_ID,
        institution=inst,
        defaults={"prefix": f"{inst.code}-EMP-", "padding": 3},
    )

    # Create or get a student user and profile
    student_user, created = User.objects.get_or_create(
        email="test_student@example.com",
        defaults={"is_active": True},
    )
    if created:
        student_user.set_password("test123")
        student_user.save()

    student, screated = Student.objects.get_or_create(
        user=student_user,
        defaults={
            "admission_date": date(2024, 1, 1),
            "date_of_birth": date(2010, 1, 1),
            "gender": "male",
            "institution": inst,
        },
    )

    print("Generated student_id:", student.student_id)

    # Create or get a staff user (we only need an employee id for demo)
    staff_user, created = User.objects.get_or_create(
        email="test_staff@example.com",
        defaults={"is_active": True},
    )
    if created:
        staff_user.set_password("test123")
        staff_user.save()

    emp_id = generate_employee_id(inst)
    print("Generated employee_id:", emp_id)


if __name__ == "__main__":
    main()
