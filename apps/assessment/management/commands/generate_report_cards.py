"""
Management command to generate report cards for all students.
Usage: python manage.py generate_report_cards [--class_id CLASS_ID] [--exam_type EXAM_TYPE] [--auto_approve]
"""

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from apps.assessment.models import ReportCard, Result, ExamType
from apps.academics.models import Class, AcademicSession


class Command(BaseCommand):
    help = 'Generate report cards for students based on results'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--class_id',
            type=int,
            help='Generate report cards for a specific class'
        )
        parser.add_argument(
            '--exam_type',
            type=str,
            help='Generate report cards for a specific exam type (use code)'
        )
        parser.add_argument(
            '--auto_approve',
            action='store_true',
            help='Auto-approve generated report cards'
        )
        parser.add_argument(
            '--dry_run',
            action='store_true',
            help='Show what would be generated without actually generating'
        )
    
    def handle(self, *args, **options):
        class_id = options.get('class_id')
        exam_type_code = options.get('exam_type')
        auto_approve = options.get('auto_approve')
        dry_run = options.get('dry_run')
        
        # Get current session
        current_session = AcademicSession.objects.filter(is_current=True).first()
        if not current_session:
            self.stdout.write(self.style.ERROR('No current academic session found'))
            return
        
        # Build query
        results = Result.objects.filter(
            academic_class__academic_session=current_session
        ).select_related(
            'student__user', 'academic_class', 'exam_type', 'grade'
        )
        
        if class_id:
            results = results.filter(academic_class_id=class_id)
        
        if exam_type_code:
            results = results.filter(exam_type__code=exam_type_code)
        
        # Filter out results that already have report cards
        existing_report_cards = ReportCard.objects.filter(
            academic_class__academic_session=current_session
        ).values_list('result_id', flat=True)
        
        results = results.exclude(id__in=existing_report_cards)
        
        # Filter for complete results only
        results = [r for r in results if self._is_result_complete(r)]
        
        self.stdout.write(self.style.SUCCESS(f'Found {len(results)} results without report cards'))
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - No report cards will be generated'))
            for result in results[:10]:  # Show first 10
                self.stdout.write(
                    f"  - {result.student.user.get_full_name()} - "
                    f"{result.academic_class.name} - {result.exam_type.name}"
                )
            if len(results) > 10:
                self.stdout.write(f"  ... and {len(results) - 10} more")
            return
        
        # Generate report cards
        created_count = 0
        skipped_count = 0
        error_count = 0
        
        for result in results:
            try:
                # Get institution from enrollment
                enrollment = result.student.enrollments.filter(
                    academic_session=current_session
                ).first()
                
                if not enrollment:
                    skipped_count += 1
                    continue
                
                institution = getattr(enrollment, 'institution', None)
                if not institution:
                    skipped_count += 1
                    continue
                
                # Get a teacher for generated_by
                from apps.academics.models import Teacher
                teacher = Teacher.objects.filter(user__is_staff=True).first()
                
                # Create report card
                report_card = ReportCard.objects.create(
                    student=result.student,
                    academic_class=result.academic_class,
                    exam_type=result.exam_type,
                    result=result,
                    institution=institution,
                    generated_by=teacher,
                    auto_generated=True,
                    generation_trigger='management_command',
                    entry_mode=ReportCard.EntryMode.AUTO
                )
                
                if auto_approve and teacher:
                    report_card.is_approved = True
                    report_card.approved_by = teacher
                    report_card.approved_at = timezone.now()
                    report_card.save()
                
                created_count += 1
                
                if created_count % 50 == 0:
                    self.stdout.write(f'Generated {created_count} report cards...')
                    
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'Error generating report card for result {result.id}: {str(e)}')
                )
        
        self.stdout.write(self.style.SUCCESS(
            f'\nReport card generation complete!\n'
            f'  Created: {created_count}\n'
            f'  Skipped: {skipped_count}\n'
            f'  Errors: {error_count}'
        ))
    
    def _is_result_complete(self, result):
        """Check if result has enough data for report card."""
        if not result.marks_obtained or not result.total_marks:
            return False
        if not result.percentage:
            return False
        return True
