from apps.core.models import Institution
from apps.academics.models import Student, AcademicSession
from apps.finance.models import Invoice
from apps.users.models import User
from datetime import date

# Get or create a test institution
institution, created = Institution.objects.get_or_create(
    code="TEST",
    defaults={
        "name": "Test School",
        "institution_type": "high_school",
        "ownership_type": "private",
    },
)
print(f"Institution: {institution.code}")

# Get an academic session
academic_session = AcademicSession.objects.filter(institution=institution).first()
if not academic_session:
    academic_session = AcademicSession.objects.filter(is_current=True).first()
if not academic_session:
    academic_session = AcademicSession.objects.first()
print(f"Academic Session: {academic_session}")

# Test student ID generation
student = None
try:
    user = User.objects.create_user(
        email="test_student@example.com", password="test123"
    )
    student = Student.objects.create(
        user=user,
        admission_date=date(2024, 1, 1),
        date_of_birth=date(2010, 1, 1),
        gender="male",
        institution=institution,
    )
    print(f"Student ID: {student.student_id}")
except Exception as e:
    print(f"Student creation error: {e}")

# Test invoice ID generation
if student and academic_session:
    try:
        invoice = Invoice.objects.create(
            student=student,
            billing_period="Test Period",
            issue_date=date(2024, 1, 1),
            due_date=date(2024, 2, 1),
            total_amount=100.00,
            institution=institution,
        )
        print(f"Invoice ID: {invoice.invoice_number}")
    except Exception as e:
        print(f"Invoice creation error: {e}")
else:
    print("Cannot test invoice - missing student or academic session")
