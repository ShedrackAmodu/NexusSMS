"""
Public payment portal views for parents/students to pay school fees.
Accessible without login via payment links.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

from .models import Invoice, Payment
from .paystack_service import PaystackService, get_payment_link, generate_payment_reference
from apps.communication.sms_service import send_payment_link_sms


class PublicPaymentView(View):
    """
    Public view for making payments on an invoice.
    Accessed via /finance/pay/<invoice_number>/
    """
    
    def get(self, request, invoice_number):
        """Display payment page for an invoice."""
        invoice = get_object_or_404(
            Invoice,
            invoice_number__iexact=invoice_number
        )
        
        # Check if invoice has balance
        if invoice.balance_due <= 0:
            messages.success(request, 'This invoice is already fully paid!')
            return render(request, 'finance/payment/already_paid.html', {
                'invoice': invoice
            })
        
        context = {
            'invoice': invoice,
            'student': invoice.student,
            'student_name': invoice.student.user.get_full_name(),
            'balance_due': invoice.balance_due,
            'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
        }
        
        return render(request, 'finance/payment/public_payment.html', context)
    
    def post(self, request, invoice_number):
        """Initialize Paystack payment."""
        import django.utils.timezone
        invoice = get_object_or_404(
            Invoice,
            invoice_number__iexact=invoice_number
        )
        
        if invoice.balance_due <= 0:
            return JsonResponse({
                'success': False,
                'message': 'Invoice is already fully paid'
            })
        
        # Generate payment link
        result = get_payment_link(invoice, student=invoice.student)
        
        if result['success']:
            # Create a pending payment record
            payment = Payment.objects.create(
                invoice=invoice,
                student=invoice.student,
                amount=invoice.balance_due,
                payment_method=Payment.PaymentMethod.ONLINE,
                payment_date=django.utils.timezone.now().date(),
                status=Payment.PaymentStatus.PENDING,
                paystack_reference=result['reference'],
                payment_url=result['payment_url']
            )
            
            return JsonResponse({
                'success': True,
                'payment_url': result['payment_url'],
                'reference': result['reference']
            })
        else:
            return JsonResponse({
                'success': False,
                'message': result.get('message', 'Failed to initialize payment')
            })


class PaymentCallbackView(View):
    """Handle Paystack payment callback."""
    
    def get(self, request):
        """Handle successful payment redirect from Paystack."""
        reference = request.GET.get('reference')
        invoice_number = request.GET.get('invoice')
        
        if not reference:
            messages.error(request, 'Payment reference not found')
            return redirect('finance:invoice_list')
        
        # Verify payment with Paystack
        service = PaystackService()
        result = service.verify_payment(reference)
        
        if result['success']:
            # Update payment status
            try:
                payment = Payment.objects.get(paystack_reference=reference)
                payment.status = Payment.PaymentStatus.COMPLETED
                payment.transaction_id = result['data'].get('id', '')
                payment.gateway_response = 'Payment successful'
                payment.save()
                
                # Update invoice
                invoice = payment.invoice
                invoice.amount_paid += payment.amount
                invoice.save()
                
                messages.success(request, f'Payment successful! Receipt: {payment.payment_number}')
                return render(request, 'finance/payment/success.html', {
                    'payment': payment,
                    'invoice': invoice
                })
                
            except Payment.DoesNotExist:
                messages.error(request, 'Payment record not found')
        else:
            messages.error(request, 'Payment verification failed')
        
        return redirect('finance:invoice_list')


class PaymentCancelView(View):
    """Handle cancelled payment."""
    
    def get(self, request):
        """Handle cancelled payment redirect from Paystack."""
        reference = request.GET.get('reference')
        
        if reference:
            try:
                payment = Payment.objects.get(paystack_reference=reference)
                payment.status = Payment.PaymentStatus.CANCELLED
                payment.gateway_response = 'Payment cancelled by user'
                payment.save()
            except Payment.DoesNotExist:
                pass
        
        messages.warning(request, 'Payment was cancelled')
        return render(request, 'finance/payment/cancel.html')


@method_decorator(csrf_exempt, name='dispatch')
class PaystackWebhookView(View):
    """Handle Paystack webhook events."""
    
    def post(self, request):
        """Process webhook events from Paystack."""
        import json
        
        # Verify webhook signature
        signature = request.headers.get('X-Paystack-Signature')
        if not PaystackService.verify_webhook_signature(request.body, signature):
            return HttpResponse('Invalid signature', status=401)
        
        # Parse event data
        try:
            event_data = json.loads(request.body)
            event_type = event_data.get('event')
            data = event_data.get('data', {})
        except json.JSONDecodeError:
            return HttpResponse('Invalid JSON', status=400)
        
        # Process event
        result = PaystackService.process_webhook_event(event_type, data)
        
        return JsonResponse(result)


class GeneratePaymentLinkView(View):
    """Admin view to generate payment links for invoices."""
    
    def post(self, request):
        """Generate and send payment link for an invoice."""
        invoice_id = request.POST.get('invoice_id')
        send_sms = request.POST.get('send_sms', 'false').lower() == 'true'
        send_email = request.POST.get('send_email', 'false').lower() == 'true'
        
        invoice = get_object_or_404(Invoice, id=invoice_id)
        
        if invoice.balance_due <= 0:
            messages.error(request, 'Invoice is already fully paid')
            return redirect('finance:invoice_detail', pk=invoice_id)
        
        # Generate payment link
        result = get_payment_link(invoice, student=invoice.student)
        
        if result['success']:
            payment_url = result['payment_url']
            
            # Send SMS if requested
            if send_sms:
                try:
                    sms_result = send_payment_link_sms(invoice.student, invoice, payment_url)
                    if sms_result['success']:
                        messages.success(request, 'Payment link sent via SMS')
                    else:
                        messages.warning(request, 'Payment link generated but SMS failed')
                except Exception as e:
                    messages.warning(request, f'Payment link generated but SMS error: {str(e)}')
            
            # TODO: Send email if requested
            # if send_email:
            #     send_payment_link_email(invoice, payment_url)
            
            messages.success(request, f'Payment link: {payment_url}')
        else:
            messages.error(request, f'Failed to generate payment link: {result.get("message")}')
        
        return redirect('finance:invoice_detail', pk=invoice_id)
