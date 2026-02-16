"""
Signal handlers for automated report card generation.
Triggers automatic report card creation when results are finalized.
"""

import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

logger = logging.getLogger(__name__)


@receiver(post_save, sender='assessment.Result')
def auto_generate_report_card(sender, instance, created, **kwargs):
    """
    Automatically generate a report card when a Result is created or updated.
    This signal triggers report card generation when results are finalized.
    """
    if not created and not kwargs.get('update_fields'):
        # Only trigger on creation or significant updates
        return
    
    # Check if result is complete enough to generate report card
    if not _is_result_complete(instance):
        logger.debug(f"Result {instance.id} not complete for report card generation")
        return
    
    # Get or create the institution
    try:
        # Try to get institution from result
        institution = getattr(instance, 'institution', None)
        if not institution:
            # Try from student enrollment
            enrollment = instance.student.enrollments.filter(
                academic_session=instance.academic_class.academic_session
            ).first()
            if enrollment:
                institution = getattr(enrollment, 'institution', None)
        
        if not institution:
            logger.warning(f"Could not determine institution for result {instance.id}")
            return
        
        # Check if auto-generation is enabled (you can make this configurable)
        from .models import ReportCard
        from apps.academics.models import Teacher
        
        # Get a default teacher for generated_by (in production, this would be a system user)
        teacher = Teacher.objects.filter(user__is_staff=True).first()
        
        # Generate report card
        report_card, rc_created = ReportCard.objects.get_or_create(
            student=instance.student,
            academic_class=instance.academic_class,
            exam_type=instance.exam_type,
            institution=institution,
            defaults={
                'result': instance,
                'generated_by': teacher,
                'auto_generated': True,
                'generation_trigger': 'result_finalized',
                'entry_mode': ReportCard.EntryMode.AUTO
            }
        )
        
        if rc_created:
            logger.info(f"Auto-generated report card for student {instance.student.id}, exam type {instance.exam_type.id}")
            
            # Optionally auto-approve if configured
            # Uncomment if you want auto-approval
            # if teacher:
            #     report_card.is_approved = True
            #     report_card.approved_by = teacher
            #     report_card.approved_at = timezone.now()
            #     report_card.save()
        else:
            logger.debug(f"Report card already exists for result {instance.id}")
            
    except Exception as e:
        logger.error(f"Error auto-generating report card: {str(e)}")


@receiver(post_save, sender='assessment.ResultSubject')
def generate_report_card_on_subject_marks_save(sender, instance, created, **kwargs):
    """
    Generate report card when a subject mark is added or updated to a result.
    """
    # Get the result from the subject mark
    result = instance.result
    
    # Check if all required marks are entered
    if not _is_result_complete(result):
        return
    
    # Trigger report card generation
    auto_generate_report_card(sender, result, created=False, update_fields=None)


def _is_result_complete(result):
    """
    Check if a result has all required data for report card generation.
    
    Args:
        result: Result object
    
    Returns:
        bool: True if result is complete
    """
    # Check basic fields
    if not result.marks_obtained or not result.total_marks:
        return False
    
    # Check if result has subject marks
    if not hasattr(result, 'subject_marks') or result.subject_marks.count() == 0:
        # Check if we can generate from exam marks
        from .models import Mark
        exam_marks = Mark.objects.filter(
            student=result.student,
            exam__exam_type=result.exam_type,
            exam__academic_class=result.academic_class
        )
        
        if exam_marks.count() == 0:
            return False
    
    # Check percentage is calculated
    if not result.percentage:
        return False
    
    return True


@receiver(post_save, sender='assessment.Mark')
def check_exam_marks_complete(sender, instance, created, **kwargs):
    """
    Check if all marks for an exam are entered, then trigger result generation.
    This helps track when an exam's marking is complete.
    """
    if not created:
        return
    
    exam = instance.exam
    
    # Get total students enrolled in the class
    try:
        from apps.academics.models import Enrollment
        total_students = Enrollment.objects.filter(
            class_enrolled=exam.academic_class,
            academic_session=exam.academic_session,
            enrollment_status='active'
        ).count()
        
        if total_students == 0:
            return
        
        # Get marks entered for this exam
        marks_entered = exam.marks.count()
        
        # If all marks are entered, you could trigger notification or auto-calculate results
        if marks_entered >= total_students:
            logger.info(f"All marks entered for exam {exam.id} ({marks_entered}/{total_students})")
            
            # Here you could add logic to:
            # 1. Auto-calculate results
            # 2. Notify teachers that grading is complete
            # 3. Trigger report card generation
    except Exception as e:
        logger.error(f"Error checking exam marks completion: {str(e)}")


# Signal to notify when report card is approved
@receiver(post_save, sender='assessment.ReportCard')
def report_card_approval_notification(sender, instance, created, **kwargs):
    """
    Send notifications (SMS/Email) when a report card is approved.
    """
    if created:
        return
    
    # Check if just approved
    if not instance.is_approved:
        return
    
    # Check if this is a new approval (not previously approved)
    if not kwargs.get('update_fields') or 'is_approved' not in kwargs.get('update_fields', set()):
        # Only trigger on explicit approval
        pass
    else:
        # Send notification via SMS if enabled
        try:
            from django.conf import settings
            if getattr(settings, 'SMS_NOTIFY_STUDENT_ON_REPORT', False):
                from apps.communication.sms_service import send_report_card_notification_sms
                
                send_report_card_notification_sms(instance.student, instance)
                logger.info(f"Sent report card notification SMS for student {instance.student.id}")
        except Exception as e:
            logger.error(f"Error sending report card SMS notification: {str(e)}")
