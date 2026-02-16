"""
PDF Generation Service for Report Cards using WeasyPrint
"""

import logging
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from weasyprint import HTML, CSS
from django.http import HttpResponse

logger = logging.getLogger(__name__)


def generate_report_card_pdf(report_card):
    """
    Generate PDF for a report card.
    
    Args:
        report_card: ReportCard object
    
    Returns:
        bytes: PDF content
    """
    # Prepare context for template
    context = _prepare_report_card_context(report_card)
    
    # Render HTML template
    html_string = render_to_string(
        'assessment/report_cards/report_card_pdf.html',
        context
    )
    
    # Convert HTML to PDF
    try:
        html = HTML(string=html_string)
        
        # Add CSS
        css = CSS(string="""
            @page {
                size: A4;
                margin: 1cm;
            }
            body {
                font-family: Arial, sans-serif;
                font-size: 12pt;
            }
        """)
        
        pdf = html.write_pdf(stylesheets=[css])
        return pdf
        
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        raise


def _prepare_report_card_context(report_card):
    """Prepare context data for report card template."""
    
    # Get student info
    student = report_card.student
    user = student.user
    
    # Get result data
    result = report_card.result
    
    # Get subject marks
    subject_marks = []
    if result:
        for sm in result.subject_marks.all():
            subject_marks.append({
                'name': sm.subject.name,
                'code': sm.subject.code,
                'marks_obtained': sm.marks_obtained,
                'max_marks': sm.max_marks,
                'percentage': sm.percentage,
                'grade': sm.grade.grade if sm.grade else '',
            })
    
    # Get institution
    institution = getattr(report_card, 'institution', None)
    
    context = {
        'report_card': report_card,
        'student': student,
        'student_name': user.get_full_name(),
        'student_admission_number': getattr(student, 'admission_number', ''),
        'academic_class': report_card.academic_class,
        'exam_type': report_card.exam_type,
        'result': result,
        'subject_marks': subject_marks,
        'institution': institution,
        'school_name': institution.name if institution else '',
        'school_address': getattr(institution, 'address', '') if institution else '',
        'school_phone': getattr(institution, 'phone', '') if institution else '',
        'school_email': getattr(institution, 'email', '') if institution else '',
        'generated_at': timezone.now(),
        
        # Report card details
        'total_marks': result.total_marks if result else 0,
        'marks_obtained': result.marks_obtained if result else 0,
        'percentage': result.percentage if result else 0,
        'grade': report_card.grade_override.grade if report_card.grade_override else (result.grade.grade if result and result.grade else ''),
        'rank': result.rank if result else '',
        'attendance_days': report_card.attendance_days,
        'total_school_days': report_card.total_school_days,
        'teacher_remarks': report_card.teacher_remarks,
        'principal_remarks': report_card.principal_remarks,
        'conduct_grade': report_card.conduct_grade,
    }
    
    return context


def generate_report_card_pdf_response(report_card):
    """
    Generate PDF HTTP response for a report card.
    
    Args:
        report_card: ReportCard object
    
    Returns:
        HttpResponse: PDF response
    """
    try:
        pdf_content = generate_report_card_pdf(report_card)
        
        # Create response
        response = HttpResponse(pdf_content, content_type='application/pdf')
        
        # Generate filename
        filename = f"report_card_{report_card.student.user.get_full_name()}_{report_card.exam_type.name}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating PDF response: {str(e)}")
        raise
