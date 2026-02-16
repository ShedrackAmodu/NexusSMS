# apps/assessment/report_card_service.py
"""
Service module for handling report card generation and management.
Ensures seamless report card generation with proper multi-tenancy isolation.
"""

from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .models import ReportCard, Result
from apps.academics.models import Student, Class
from apps.core.models import Institution


class ReportCardService:
    """Service class for report card operations."""
    
    @staticmethod
    def generate_report_card(result, teacher, institution, auto_approve=False):
        """
        Generate a report card for a result with proper validation and multi-tenancy.
        
        Args:
            result: The Result object to generate a report card for
            teacher: The Teacher profile of the user generating the report
            institution: The Institution the report card belongs to
            auto_approve: Whether to automatically approve the report card
        
        Returns:
            Tuple of (report_card, created) where created is a boolean
        
        Raises:
            ValidationError: If validation fails
        """
        if not result:
            raise ValidationError(_("Result object is required."))
        
        if not teacher:
            raise ValidationError(_("Teacher profile is required."))
        
        if not institution:
            raise ValidationError(_("Institution is required."))
        
        # Validate result belongs to the same institution
        if result.institution != institution:
            raise ValidationError(
                _("Result does not belong to your institution.")
            )
        
        # Validate student belongs to the same institution
        student_enrollments = result.student.enrollments.filter(
            academic_session=result.academic_class.academic_session,
            institution=institution
        )
        
        if not student_enrollments.exists():
            raise ValidationError(
                _("Student is not enrolled in your institution for this academic session.")
            )
        
        # Create or get report card
        with transaction.atomic():
            report_card, created = ReportCard.objects.get_or_create(
                student=result.student,
                academic_class=result.academic_class,
                exam_type=result.exam_type,
                institution=institution,
                defaults={
                    'result': result,
                    'generated_by': teacher,
                    'is_approved': auto_approve,
                    'approved_by': teacher if auto_approve else None,
                    'approved_at': timezone.now() if auto_approve else None,
                }
            )
        
        return report_card, created
    
    @staticmethod
    def bulk_generate_report_cards(results, teacher, institution, auto_approve=False):
        """
        Generate report cards for multiple results.
        
        Args:
            results: QuerySet or list of Result objects
            teacher: The Teacher profile
            institution: The Institution
            auto_approve: Whether to automatically approve
        
        Returns:
            Dictionary with statistics about generation
        """
        stats = {
            'total': 0,
            'created': 0,
            'already_exists': 0,
            'errors': 0,
            'error_details': []
        }
        
        for result in results:
            try:
                report_card, created = ReportCardService.generate_report_card(
                    result, teacher, institution, auto_approve
                )
                
                stats['total'] += 1
                if created:
                    stats['created'] += 1
                else:
                    stats['already_exists'] += 1
            
            except ValidationError as e:
                stats['errors'] += 1
                stats['error_details'].append({
                    'result_id': result.id,
                    'student': str(result.student),
                    'error': str(e)
                })
        
        return stats
    
    @staticmethod
    def approve_report_card(report_card, teacher, institution):
        """
        Approve a report card with validation.
        
        Args:
            report_card: The ReportCard object to approve
            teacher: The Teacher profile approving
            institution: The Institution
        
        Raises:
            ValidationError: If validation fails
        """
        if not report_card:
            raise ValidationError(_("Report card is required."))
        
        if report_card.institution != institution:
            raise ValidationError(
                _("You do not have permission to approve this report card.")
            )
        
        if report_card.is_approved:
            raise ValidationError(
                _("This report card has already been approved.")
            )
        
        with transaction.atomic():
            report_card.is_approved = True
            report_card.approved_by = teacher
            report_card.approved_at = timezone.now()
            report_card.save(update_fields=[
                'is_approved', 'approved_by', 'approved_at', 'updated_at'
            ])
    
    @staticmethod
    def get_institution_report_cards(institution, filters=None):
        """
        Get all report cards for an institution with optional filters.
        
        Args:
            institution: The Institution object
            filters: Optional dictionary of filter criteria
        
        Returns:
            QuerySet of ReportCard objects
        """
        queryset = ReportCard.objects.filter(
            institution=institution
        ).select_related(
            'student__user', 'academic_class', 'exam_type', 'result', 'institution'
        ).prefetch_related('result__subject_marks__subject')
        
        if filters:
            if 'approved' in filters:
                queryset = queryset.filter(is_approved=filters['approved'])
            
            if 'class' in filters:
                queryset = queryset.filter(academic_class=filters['class'])
            
            if 'exam_type' in filters:
                queryset = queryset.filter(exam_type=filters['exam_type'])
            
            if 'student' in filters:
                queryset = queryset.filter(student=filters['student'])
            
            if 'date_from' in filters:
                queryset = queryset.filter(generated_at__gte=filters['date_from'])
            
            if 'date_to' in filters:
                queryset = queryset.filter(generated_at__lte=filters['date_to'])
        
        return queryset
    
    @staticmethod
    def get_student_report_cards(student, institution, approved_only=True):
        """
        Get report cards for a student in a specific institution.
        
        Args:
            student: The Student object
            institution: The Institution object
            approved_only: Whether to return only approved report cards
        
        Returns:
            QuerySet of ReportCard objects
        """
        queryset = ReportCard.objects.filter(
            student=student,
            institution=institution
        ).select_related('academic_class', 'exam_type', 'result')
        
        if approved_only:
            queryset = queryset.filter(is_approved=True)
        
        return queryset.order_by('-generated_at')
    
    @staticmethod
    def validate_report_card_data(report_card):
        """
        Validate a report card has all necessary data for display.
        
        Args:
            report_card: The ReportCard object
        
        Returns:
            Dictionary with validation results
        """
        validation_results = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }
        
        # Check required relationships
        if not report_card.result:
            validation_results['errors'].append(_("Report card missing result data."))
            validation_results['is_valid'] = False
        
        if not report_card.student:
            validation_results['errors'].append(_("Report card missing student data."))
            validation_results['is_valid'] = False
        
        if not report_card.academic_class:
            validation_results['errors'].append(_("Report card missing class data."))
            validation_results['is_valid'] = False
        
        if not report_card.institution:
            validation_results['errors'].append(_("Report card missing institution data."))
            validation_results['is_valid'] = False
        
        # Check for subject marks
        if report_card.result and not report_card.result.subject_marks.exists():
            validation_results['warnings'].append(
                _("Report card has no subject marks.")
            )
        
        # Check approval status
        if not report_card.is_approved:
            validation_results['warnings'].append(
                _("Report card has not been approved yet.")
            )
        
        return validation_results
    
    @staticmethod
    def get_report_card_summary(institution):
        """
        Get summary statistics for report cards in an institution.
        
        Args:
            institution: The Institution object
        
        Returns:
            Dictionary with summary statistics
        """
        from django.db.models import Count, Q
        
        report_cards = ReportCard.objects.filter(institution=institution)
        
        summary = {
            'total_report_cards': report_cards.count(),
            'approved': report_cards.filter(is_approved=True).count(),
            'pending': report_cards.filter(is_approved=False).count(),
            'with_parent_signature': report_cards.filter(parent_signature=True).count(),
            'unique_students': report_cards.values('student').distinct().count(),
            'unique_classes': report_cards.values('academic_class').distinct().count(),
        }
        
        return summary
