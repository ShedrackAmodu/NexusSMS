"""
Paystack Payment Gateway Service for NexusSMS
Handles payment initialization, verification, and webhook processing
"""

import requests
import hashlib
import hmac
import logging
from django.conf import settings
from django.utils import timezone
from decimal import Decimal

logger = logging.getLogger(__name__)


class PaystackService:
    """Service class for Paystack payment gateway integration."""
    
    def __init__(self):
        self.secret_key = settings.PAYSTACK_SECRET_KEY
        self.public_key = settings.PAYSTACK_PUBLIC_KEY
        self.base_url = settings.PAYSTACK_PAYMENT_URL
        self.test_mode = settings.PAYSTACK_TEST_MODE
        
    def _get_headers(self):
        """Get headers for Paystack API requests."""
        return {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/json',
        }
    
    def initialize_payment(self, amount, email, reference=None, callback_url=None):
        """
        Initialize a payment transaction.
        
        Args:
            amount: Amount in kobo (Naira * 100)
            email: Customer email address
            reference: Optional custom reference (generated if not provided)
            callback_url: Optional custom callback URL
            
        Returns:
            dict: Response from Paystack API
        """
        url = f"{self.base_url}/transaction/initialize"
        
        # Convert amount to kobo if it's in naira
        if amount < 10000:  # Assume if less than 10000, it's in naira
            amount_kobo = int(amount * 100)
        else:
            amount_kobo = int(amount)
        
        data = {
            'amount': amount_kobo,
            'email': email,
            'reference': reference,
            'callback_url': callback_url or settings.PAYSTACK_CALLBACK_URL,
        }
        
        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}
        
        try:
            response = requests.post(url, json=data, headers=self._get_headers())
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"Paystack payment initialized: {result.get('data', {}).get('reference')}")
            return {
                'success': True,
                'data': result.get('data', {}),
                'message': result.get('message', '')
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Paystack initialization error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to initialize payment'
            }
    
    def verify_payment(self, reference):
        """
        Verify a payment transaction.
        
        Args:
            reference: Payment reference to verify
            
        Returns:
            dict: Verification result from Paystack
        """
        url = f"{self.base_url}/transaction/verify/{reference}"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            result = response.json()
            
            if result.get('status') and result.get('data', {}).get('status') == 'success':
                return {
                    'success': True,
                    'data': result.get('data', {}),
                    'message': 'Payment verified successfully'
                }
            else:
                return {
                    'success': False,
                    'data': result.get('data', {}),
                    'message': result.get('message', 'Payment verification failed')
                }
        except requests.exceptions.RequestException as e:
            logger.error(f"Paystack verification error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to verify payment'
            }
    
    def create_customer(self, email, first_name=None, last_name=None, phone=None):
        """
        Create a Paystack customer.
        
        Args:
            email: Customer email
            first_name: Customer first name
            last_name: Customer last name
            phone: Customer phone number
            
        Returns:
            dict: Customer creation result
        """
        url = f"{self.base_url}/customer"
        
        data = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
        }
        
        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}
        
        try:
            response = requests.post(url, json=data, headers=self._get_headers())
            response.raise_for_status()
            result = response.json()
            
            return {
                'success': result.get('status', False),
                'data': result.get('data', {}),
                'message': result.get('message', '')
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Paystack create customer error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to create customer'
            }
    
    def get_customer(self, email_or_code):
        """
        Get a Paystack customer by email or customer code.
        
        Args:
            email_or_code: Customer email or customer code
            
        Returns:
            dict: Customer details
        """
        url = f"{self.base_url}/customer/{email_or_code}"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            result = response.json()
            
            return {
                'success': result.get('status', False),
                'data': result.get('data', {}),
                'message': result.get('message', '')
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Paystack get customer error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to get customer'
            }
    
    def list_customers(self, per_page=50, page=1):
        """
        List Paystack customers.
        
        Args:
            per_page: Number of customers per page
            page: Page number
            
        Returns:
            dict: List of customers
        """
        url = f"{self.base_url}/customer"
        params = {
            'perPage': per_page,
            'page': page,
        }
        
        try:
            response = requests.get(url, params=params, headers=self._get_headers())
            response.raise_for_status()
            result = response.json()
            
            return {
                'success': result.get('status', False),
                'data': result.get('data', []),
                'meta': result.get('meta', {}),
                'message': result.get('message', '')
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Paystack list customers error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to list customers'
            }
    
    def refund_transaction(self, reference, amount=None):
        """
        Refund a transaction.
        
        Args:
            reference: Transaction reference
            amount: Optional specific amount to refund (in kobo)
            
        Returns:
            dict: Refund result
        """
        url = f"{self.base_url}/refund"
        
        data = {
            'transaction': reference,
        }
        
        if amount:
            data['amount'] = amount
            
        try:
            response = requests.post(url, json=data, headers=self._get_headers())
            response.raise_for_status()
            result = response.json()
            
            return {
                'success': result.get('status', False),
                'data': result.get('data', {}),
                'message': result.get('message', '')
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Paystack refund error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to process refund'
            }
    
    def get_transaction_logs(self, reference):
        """
        Get transaction timeline/logs.
        
        Args:
            reference: Transaction reference
            
        Returns:
            dict: Transaction logs
        """
        url = f"{self.base_url}/transaction/timeline/{reference}"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            result = response.json()
            
            return {
                'success': result.get('status', False),
                'data': result.get('data', {}),
                'message': result.get('message', '')
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Paystack transaction logs error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to get transaction logs'
            }
    
    @staticmethod
    def verify_webhook_signature(payload, signature):
        """
        Verify the webhook signature from Paystack.
        
        Args:
            payload: Raw request body
            signature: X-Paystack-Signature header value
            
        Returns:
            bool: True if signature is valid
        """
        if not settings.PAYSTACK_WEBHOOK_SECRET:
            logger.warning("Paystack webhook secret not configured")
            return False
            
        expected_signature = hmac.new(
            settings.PAYSTACK_WEBHOOK_SECRET.encode('utf-8'),
            payload,
            hashlib.sha512
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    
    @staticmethod
    def process_webhook_event(event_type, event_data):
        """
        Process webhook events from Paystack.
        
        Args:
            event_type: Type of event (e.g., 'charge.success', 'transfer.failed')
            event_data: Event data from Paystack
            
        Returns:
            dict: Processing result
        """
        from apps.finance.models import Payment, Invoice
        
        logger.info(f"Processing Paystack webhook: {event_type}")
        
        if event_type == 'charge.success':
            return PaystackService._process_charge_success(event_data)
        elif event_type == 'charge.failed':
            return PaystackService._process_charge_failed(event_data)
        elif event_type == 'refund.created':
            return PaystackService._process_refund_created(event_data)
        else:
            logger.info(f"Unhandled webhook event: {event_type}")
            return {'success': True, 'message': 'Event acknowledged'}
    
    @staticmethod
    def _process_charge_success(event_data):
        """Process successful charge event."""
        from apps.finance.models import Payment, Invoice
        
        reference = event_data.get('reference')
        amount = event_data.get('amount', 0)
        
        # Find the payment by reference
        try:
            payment = Payment.objects.get(paystack_reference=reference)
            
            # Update payment status
            payment.status = payment.PaymentStatus.COMPLETED
            payment.transaction_id = event_data.get('id', '')
            payment.gateway_response = event_data.get('gateway_response', '')
            
            # Store authorization code for future payments
            authorization = event_data.get('authorization', {})
            payment.authorization_code = authorization.get('authorization_code', '')
            
            payment.save()
            
            # Update invoice
            invoice = payment.invoice
            invoice.amount_paid += payment.amount
            invoice.save()
            
            logger.info(f"Payment completed: {reference}")
            return {'success': True, 'message': 'Payment processed'}
            
        except Payment.DoesNotExist:
            logger.error(f"Payment not found for reference: {reference}")
            return {'success': False, 'message': 'Payment not found'}
    
    @staticmethod
    def _process_charge_failed(event_data):
        """Process failed charge event."""
        from apps.finance.models import Payment
        
        reference = event_data.get('reference')
        
        try:
            payment = Payment.objects.get(paystack_reference=reference)
            payment.status = payment.PaymentStatus.FAILED
            payment.gateway_response = event_data.get('gateway_response', 'Payment failed')
            payment.save()
            
            logger.info(f"Payment failed: {reference}")
            return {'success': True, 'message': 'Payment failure recorded'}
            
        except Payment.DoesNotExist:
            logger.error(f"Payment not found for reference: {reference}")
            return {'success': False, 'message': 'Payment not found'}
    
    @staticmethod
    def _process_refund_created(event_data):
        """Process refund created event."""
        from apps.finance.models import Payment, Invoice
        
        reference = event_data.get('reference')
        
        try:
            payment = Payment.objects.get(paystack_reference=reference)
            payment.status = payment.PaymentStatus.REFUNDED
            payment.save()
            
            # Reverse the payment on invoice
            invoice = payment.invoice
            invoice.amount_paid -= payment.amount
            invoice.save()
            
            logger.info(f"Refund processed: {reference}")
            return {'success': True, 'message': 'Refund processed'}
            
        except Payment.DoesNotExist:
            logger.error(f"Payment not found for reference: {reference}")
            return {'success': False, 'message': 'Payment not found'}


def generate_payment_reference(prefix='PAY'):
    """Generate a unique payment reference."""
    import uuid
    from datetime import datetime
    
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_id = str(uuid.uuid4())[:8].upper()
    return f"{prefix}-{timestamp}-{unique_id}"


def get_payment_link(invoice, student=None, parent=None):
    """
    Generate a payment link for an invoice.
    
    Args:
        invoice: The Invoice object
        student: The Student object (optional)
        parent: The Parent object (optional)
        
    Returns:
        dict: Payment link details including URL
    """
    service = PaystackService()
    
    # Determine email and name
    if student:
        email = student.user.email
        name = student.user.get_full_name()
    elif parent:
        email = parent.user.email if parent.user else parent.email
        name = parent.user.get_full_name() if parent.user else f"{parent.first_name} {parent.last_name}"
    else:
        # Fallback to invoice student
        email = invoice.student.user.email
        name = invoice.student.user.get_full_name()
    
    # Generate reference
    reference = generate_payment_reference()
    
    # Initialize payment
    # Convert to kobo
    amount_kobo = int(invoice.balance_due * 100)
    
    callback_url = f"{settings.PAYSTACK_CALLBACK_URL}?invoice={invoice.invoice_number}&reference={reference}"
    
    result = service.initialize_payment(
        amount=amount_kobo,
        email=email,
        reference=reference,
        callback_url=callback_url
    )
    
    if result['success']:
        return {
            'success': True,
            'payment_url': result['data'].get('authorization_url'),
            'reference': reference,
            'access_code': result['data'].get('access_code'),
            'amount': invoice.balance_due,
            'email': email,
            'name': name
        }
    else:
        return {
            'success': False,
            'error': result.get('error'),
            'message': result.get('message')
        }
