"""
SMS Gateway Service for NexusSMS
Supports multiple Nigerian SMS providers: Termii, Multitexter, Africa's Talking
"""

import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class SMSService:
    """Base SMS Service class."""
    
    def send_sms(self, phone_number, message):
        """Send SMS to a phone number."""
        raise NotImplementedError


class TermiiService(SMSService):
    """Termii SMS service for Nigerian schools."""
    
    def __init__(self):
        self.api_key = settings.TERMII_API_KEY
        self.sender_id = settings.TERMII_SENDER_ID
        self.base_url = settings.TERMII_BASE_URL
    
    def send_sms(self, phone_number, message):
        """Send SMS via Termii API."""
        url = f"{self.base_url}/send"
        
        # Ensure phone number is in correct format
        if not phone_number.startswith('+'):
            if phone_number.startswith('0'):
                phone_number = '+234' + phone_number[1:]
            else:
                phone_number = '+234' + phone_number
        
        payload = {
            'api_key': self.api_key,
            'to': phone_number,
            'from': self.sender_id,
            'sms': message,
            'type': 'plain',
            'channel': 'generic'
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if result.get('code') == 'ok' or result.get('status') == 'success':
                return {
                    'success': True,
                    'message_id': result.get('message_id', ''),
                    'message': 'SMS sent successfully'
                }
            else:
                return {
                    'success': False,
                    'error': result.get('message', 'Failed to send SMS'),
                    'message': 'SMS sending failed'
                }
        except requests.exceptions.RequestException as e:
            logger.error(f"Termii SMS error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to send SMS'
            }
    
    def send_bulk_sms(self, phone_numbers, message):
        """Send bulk SMS via Termii."""
        url = f"{self.base_url}/send/bulk"
        
        # Format phone numbers
        formatted_numbers = []
        for number in phone_numbers:
            if not number.startswith('+'):
                if number.startswith('0'):
                    number = '+234' + number[1:]
                else:
                    number = '+234' + number
            formatted_numbers.append(number)
        
        payload = {
            'api_key': self.api_key,
            'to': formatted_numbers,
            'from': self.sender_id,
            'sms': message,
            'type': 'plain',
            'channel': 'generic'
        }
        
        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            
            return {
                'success': True,
                'data': result,
                'message': 'Bulk SMS sent'
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Termii bulk SMS error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to send bulk SMS'
            }


class MultitexterService(SMSService):
    """Multitexter SMS service."""
    
    def __init__(self):
        self.api_key = settings.MULTITEXTER_API_KEY
    
    def send_sms(self, phone_number, message):
        """Send SMS via Multitexter."""
        url = "https://app.multitexter.com/fundamentals/api/v2/sms/send"
        
        # Format phone number
        if not phone_number.startswith('+'):
            if phone_number.startswith('0'):
                phone_number = '234' + phone_number[1:]
            else:
                phone_number = '234' + phone_number
        
        payload = {
            'api_key': self.api_key,
            'sender_name': settings.TERMII_SENDER_ID,
            'message': message,
            'recipients': [phone_number]
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if result.get('status') == 1 or result.get('error') == 'None':
                return {
                    'success': True,
                    'message_id': result.get('message_id', ''),
                    'message': 'SMS sent successfully'
                }
            else:
                return {
                    'success': False,
                    'error': result.get('error', 'Failed to send SMS'),
                    'message': 'SMS sending failed'
                }
        except requests.exceptions.RequestException as e:
            logger.error(f"Multitexter SMS error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to send SMS'
            }


class AfricaStalkingService(SMSService):
    """Africa's Talking SMS service."""
    
    def __init__(self):
        self.username = settings.AFRICASTALKING_USERNAME
        self.api_key = settings.AFRICASTALKING_API_KEY
    
    def send_sms(self, phone_number, message):
        """Send SMS via Africa's Talking."""
        url = "https://api.africas-talking.com/version1/messaging"
        
        # Format phone number
        if not phone_number.startswith('+'):
            if phone_number.startswith('0'):
                phone_number = '+234' + phone_number[1:]
            else:
                phone_number = '+234' + phone_number
        
        payload = {
            'username': self.username,
            'to': phone_number,
            'message': message
        }
        
        headers = {
            'apiKey': self.api_key,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            response = requests.post(url, data=payload, headers=headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if result.get('SMSMessageData', {}).get('Recipients'):
                return {
                    'success': True,
                    'message_id': result['SMSMessageData']['Recipients'][0].get('messageId', ''),
                    'message': 'SMS sent successfully'
                }
            else:
                return {
                    'success': False,
                    'error': result.get('SMSMessageData', {}).get('Message', 'Failed to send SMS'),
                    'message': 'SMS sending failed'
                }
        except requests.exceptions.RequestException as e:
            logger.error(f"Africa's Talking SMS error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to send SMS'
            }


def get_sms_service():
    """Get the configured SMS service based on settings."""
    provider = getattr(settings, 'SMS_PROVIDER', 'termii').lower()
    
    if provider == 'termii':
        return TermiiService()
    elif provider == 'multitexter':
        return MultitexterService()
    elif provider == 'africastalking':
        return AfricaStalkingService()
    else:
        # Default to Termii
        return TermiiService()


def send_payment_link_sms(student, invoice, payment_url):
    """
    Send payment link via SMS to student and parents.
    
    Args:
        student: Student object
        invoice: Invoice object
        payment_url: Payment URL to send
    
    Returns:
        dict: Result of SMS sending
    """
    service = get_sms_service()
    
    # Build message
    message = f"Hello, {student.user.get_full_name()}. "
    message += f"Your school fees invoice #{invoice.invoice_number} is ready. "
    message += f"Amount: ₦{invoice.balance_due}. "
    message += f"Pay now: {payment_url} "
    message += "- NexusSMS"
    
    results = []
    
    # Send to student if they have phone
    if hasattr(student, 'phone') and student.phone:
        result = service.send_sms(student.phone, message)
        results.append({
            'recipient': 'student',
            'phone': student.phone,
            'result': result
        })
    
    # Send to parents
    try:
        from apps.academics.models import StudentParentRelationship
        parent_relationships = StudentParentRelationship.objects.filter(
            student=student,
            can_access_records=True
        ).select_related('parent')
        
        for relationship in parent_relationships:
            if relationship.parent.phone:
                parent_message = f"Dear Parent, {student.user.get_full_name()}'s school fees invoice "
                parent_message += f"#{invoice.invoice_number} is ready. Amount: ₦{invoice.balance_due}. "
                parent_message += f"Pay now: {payment_url} - NexusSMS"
                
                result = service.send_sms(relationship.parent.phone, parent_message)
                results.append({
                    'recipient': 'parent',
                    'phone': relationship.parent.phone,
                    'result': result
                })
    except ImportError:
        logger.warning("StudentParentRelationship model not found")
    
    return {
        'success': any(r['result'].get('success') for r in results),
        'results': results
    }


def send_report_card_notification_sms(student, report_card):
    """
    Send report card notification via SMS.
    
    Args:
        student: Student object
        report_card: ReportCard object
    
    Returns:
        dict: Result of SMS sending
    """
    service = get_sms_service()
    
    # Build message
    message = f"Hello, {student.user.get_full_name()}'s parent/guardian. "
    message += f"Your child's report card for {report_card.exam_type.name} is now available. "
    if report_card.is_approved:
        message += "It has been approved and is ready for viewing. "
    else:
        message += "It is pending approval. "
    message += "- NexusSMS"
    
    results = []
    
    # Send to parents
    try:
        from apps.academics.models import StudentParentRelationship
        parent_relationships = StudentParentRelationship.objects.filter(
            student=student,
            can_access_records=True
        ).select_related('parent')
        
        for relationship in parent_relationships:
            if relationship.parent.phone:
                result = service.send_sms(relationship.parent.phone, message)
                results.append({
                    'recipient': 'parent',
                    'phone': relationship.parent.phone,
                    'result': result
                })
    except ImportError:
        logger.warning("StudentParentRelationship model not found")
    
    return {
        'success': any(r['result'].get('success') for r in results),
        'results': results
    }
