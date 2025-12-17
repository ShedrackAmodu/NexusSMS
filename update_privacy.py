#!/usr/bin/env python
import os
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.development')
django.setup()

from apps.support.models import LegalDocument

def update_privacy_policy():
    try:
        # Get the existing privacy policy
        pp = LegalDocument.objects.get(document_type='privacy_policy')

        # Enhanced privacy policy content
        enhanced_content = """<h2>Executive Summary</h2>
<p>At Nexus School Management System ("we," "our," or "us"), we are committed to protecting your privacy and ensuring the security of your personal information. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our school management platform.</p>
<p>This policy applies to all users of our services, including administrators, teachers, students, parents, and other authorized personnel who access our platform.</p>

<h2>1. Information We Collect</h2>

<h3>1.1 Personal Information You Provide</h3>
<p>We collect information you provide directly to us, including:</p>
<ul>
<li><strong>Account Information:</strong> Name, email address, phone number, and role-specific details when you create an account</li>
<li><strong>Student Information:</strong> Academic records, attendance data, grades, and performance metrics</li>
<li><strong>Communication Data:</strong> Messages, announcements, and feedback submitted through our platform</li>
<li><strong>Support Requests:</strong> Information provided when contacting our support team</li>
</ul>

<h3>1.2 Information We Collect Automatically</h3>
<ul>
<li><strong>Usage Data:</strong> How you interact with our platform, including pages visited, features used, and time spent</li>
<li><strong>Device Information:</strong> IP address, browser type, operating system, and device identifiers</li>
<li><strong>Log Data:</strong> Server logs, error reports, and performance metrics</li>
<li><strong>Cookies and Tracking:</strong> Information collected through cookies and similar technologies</li>
</ul>

<h3>1.3 Information from Third Parties</h3>
<p>We may receive information from third-party services you connect to our platform, such as:</p>
<ul>
<li>Single sign-on providers (Google, Microsoft, etc.)</li>
<li>Educational institutions for data integration</li>
<li>Payment processors for billing information</li>
</ul>

<h2>2. How We Use Your Information</h2>
<p>We use the information we collect for the following purposes:</p>

<h3>2.1 Service Provision</h3>
<ul>
<li>To provide, maintain, and improve our school management services</li>
<li>To process transactions and manage subscriptions</li>
<li>To deliver personalized educational content and features</li>
<li>To ensure platform security and prevent unauthorized access</li>
</ul>

<h3>2.2 Communication</h3>
<ul>
<li>To send important updates, security alerts, and service notifications</li>
<li>To respond to your inquiries and provide customer support</li>
<li>To send educational announcements and academic communications</li>
<li>To provide technical assistance and troubleshooting</li>
</ul>

<h3>2.3 Analytics and Improvement</h3>
<ul>
<li>To analyze usage patterns and improve user experience</li>
<li>To develop new features and enhance existing functionality</li>
<li>To monitor system performance and identify issues</li>
<li>To conduct research and generate insights for educational improvement</li>
</ul>

<h3>2.4 Legal and Compliance</h3>
<ul>
<li>To comply with legal obligations and regulatory requirements</li>
<li>To protect against fraud, abuse, and security threats</li>
<li>To enforce our terms of service and acceptable use policies</li>
<li>To respond to legal requests and protect our rights</li>
</ul>

<h2>3. Information Sharing and Disclosure</h2>

<h3>3.1 With Your Consent</h3>
<p>We share your information when you explicitly consent to such sharing, including:</p>
<ul>
<li>When you authorize third-party integrations</li>
<li>When you share information through social features</li>
<li>When you participate in collaborative educational activities</li>
</ul>

<h3>3.2 Service Providers</h3>
<p>We share information with trusted third-party service providers who assist us in:</p>
<ul>
<li>Hosting and maintaining our platform infrastructure</li>
<li>Processing payments and managing subscriptions</li>
<li>Providing customer support and communication services</li>
<li>Analyzing platform usage and performance</li>
</ul>

<h3>3.3 Legal Requirements</h3>
<p>We may disclose your information if required by law or to protect rights and safety:</p>
<ul>
<li>In response to legal requests, court orders, or government inquiries</li>
<li>To protect against imminent harm to individuals or property</li>
<li>To investigate potential violations of our terms or policies</li>
<li>To enforce our agreements and protect our legal rights</li>
</ul>

<h3>3.4 Business Transfers</h3>
<p>In the event of a merger, acquisition, or sale of assets, your information may be transferred to the new entity, subject to continued protection under this privacy policy.</p>

<h2>4. Data Security</h2>
<p>We implement comprehensive security measures to protect your personal information:</p>

<h3>4.1 Technical Safeguards</h3>
<ul>
<li><strong>Encryption:</strong> Data encrypted in transit and at rest using industry-standard protocols</li>
<li><strong>Access Controls:</strong> Role-based access controls and multi-factor authentication</li>
<li><strong>Network Security:</strong> Firewalls, intrusion detection, and regular security audits</li>
<li><strong>Data Backup:</strong> Regular encrypted backups with secure storage</li>
</ul>

<h3>4.2 Administrative Controls</h3>
<ul>
<li><strong>Staff Training:</strong> Regular security awareness training for all personnel</li>
<li><strong>Access Management:</strong> Least-privilege access and regular access reviews</li>
<li><strong>Incident Response:</strong> Established procedures for security incidents</li>
<li><strong>Vendor Assessment:</strong> Security evaluations of third-party providers</li>
</ul>

<h3>4.3 Monitoring and Updates</h3>
<ul>
<li><strong>Security Monitoring:</strong> Continuous monitoring for suspicious activities</li>
<li><strong>Regular Audits:</strong> Periodic security assessments and penetration testing</li>
<li><strong>Software Updates:</strong> Timely application of security patches and updates</li>
</ul>

<h2>5. Your Rights and Controls</h2>

<h3>5.1 Access and Portability</h3>
<p>You have the right to:</p>
<ul>
<li><strong>Access:</strong> Request a copy of your personal information we hold</li>
<li><strong>Portability:</strong> Receive your data in a structured, machine-readable format</li>
<li><strong>Correction:</strong> Request correction of inaccurate or incomplete information</li>
</ul>

<h3>5.2 Deletion and Restriction</h3>
<ul>
<li><strong>Deletion:</strong> Request deletion of your personal information (subject to legal requirements)</li>
<li><strong>Restriction:</strong> Request limitation of processing in certain circumstances</li>
<li><strong>Objection:</strong> Object to processing based on legitimate interests</li>
</ul>

<h3>5.3 Communication Preferences</h3>
<ul>
<li><strong>Marketing Opt-out:</strong> Unsubscribe from marketing communications</li>
<li><strong>Notification Settings:</strong> Control notification preferences in your account</li>
<li><strong>Cookie Controls:</strong> Manage cookie preferences through your browser</li>
</ul>

<h2>6. Data Retention</h2>
<p>We retain your information only as long as necessary for the purposes outlined in this policy:</p>
<ul>
<li><strong>Account Data:</strong> Retained while your account is active and for a reasonable period after deactivation</li>
<li><strong>Educational Records:</strong> Retained according to educational record retention requirements</li>
<li><strong>Communication Logs:</strong> Retained for customer service and legal compliance purposes</li>
<li><strong>Analytics Data:</strong> Aggregated and anonymized data may be retained indefinitely</li>
</ul>

<h2>7. International Data Transfers</h2>
<p>Our services may involve transfers of data to countries outside your own. We ensure appropriate safeguards:</p>
<ul>
<li><strong>Adequacy Decisions:</strong> Transfers to countries with adequate data protection</li>
<li><strong>Standard Contracts:</strong> Use of approved contractual clauses</li>
<li><strong>Certification Schemes:</strong> Compliance with recognized certification frameworks</li>
<li><strong>Your Consent:</strong> Where required, obtaining explicit consent for transfers</li>
</ul>

<h2>8. Children's Privacy</h2>
<p>We are committed to protecting children's privacy in accordance with applicable laws:</p>
<ul>
<li><strong>Age Restrictions:</strong> Services may be restricted to users 13 years and older</li>
<li><strong>Parental Consent:</strong> Where required, we obtain parental consent for data collection</li>
<li><strong>Educational Data:</strong> Student information is handled in compliance with FERPA and similar regulations</li>
<li><strong>Privacy Notices:</strong> Clear communication about data collection to parents and guardians</li>
</ul>

<h2>9. Third-party Services</h2>

<h3>9.1 External Links</h3>
<p>Our platform may contain links to third-party websites. We are not responsible for the privacy practices of these external sites.</p>

<h3>9.2 Analytics Services</h3>
<p>We use analytics services to understand platform usage and improve our services. These services may collect anonymous usage data.</p>

<h3>9.3 Payment Processing</h3>
<p>Payment information is processed by secure third-party payment processors. We do not store payment card details on our servers.</p>

<h2>10. Cookies and Tracking Technologies</h2>
<p>We use cookies and similar technologies to enhance your experience:</p>

<h3>10.1 Essential Cookies</h3>
<p>Required for platform functionality, authentication, and security.</p>

<h3>10.2 Analytics Cookies</h3>
<p>Help us understand how users interact with our platform to improve services.</p>

<h3>10.3 Preference Cookies</h3>
<p>Remember your settings and preferences for a personalized experience.</p>

<h3>10.4 Marketing Cookies</h3>
<p>Used to deliver relevant advertisements and measure campaign effectiveness.</p>

<h2>11. Changes to This Privacy Policy</h2>

<h3>11.1 Updates</h3>
<p>We may update this privacy policy periodically to reflect changes in our practices or legal requirements.</p>

<h3>11.2 Notification</h3>
<ul>
<li><strong>Email Notification:</strong> We will notify you via email of material changes</li>
<li><strong>Platform Notice:</strong> Updates will be posted on our platform with effective dates</li>
<li><strong>Review History:</strong> Previous versions available upon request</li>
</ul>

<h3>11.3 Your Responsibility</h3>
<p>Please review this policy periodically. Continued use of our services after changes constitutes acceptance of the updated policy.</p>

<h2>12. Contact Information</h2>

<h3>12.1 Data Protection Officer</h3>
<div class="contact-info">
<p>For privacy-related inquiries, please contact our Data Protection Officer:</p>
<ul>
<li><strong>Email:</strong> privacy@nordalms.pythonanywhere.com</li>
<li><strong>Response Time:</strong> Within 30 days for data requests</li>
</ul>
</div>

<h3>12.2 General Support</h3>
<ul>
<li><strong>Email:</strong> support@nordalms.pythonanywhere.com</li>
<li><strong>Phone:</strong> +1 (555) 123-4567</li>
<li><strong>Hours:</strong> Monday - Friday, 9 AM - 6 PM EST</li>
</ul>

<h3>12.3 Postal Address</h3>
<address>
Nexus School Management System<br>
Attn: Data Protection Officer<br>
[Your Business Address]<br>
[City, State, ZIP Code]<br>
[Country]
</address>

<h2>13. Additional Resources</h2>
<ul>
<li><a href="/support/terms-of-service/">Terms of Service</a></li>
<li><a href="/support/cookie-policy/">Cookie Policy</a></li>
<li><a href="/support/data-protection/">Data Protection Policy</a></li>
<li><a href="/support/accessibility/">Accessibility Statement</a></li>
</ul>

<p><em>This privacy policy was last updated on December 17, 2025. Version 2.0</em></p>"""

        # Update the privacy policy
        pp.content = enhanced_content
        pp.version = '2.0'
        pp.title = 'Privacy Policy'
        pp.save()

        print('✅ Privacy policy successfully updated!')
        print(f'ID: {pp.id}')
        print(f'Version: {pp.version}')
        print(f'Content length: {len(pp.content)} characters')
        print(f'Title: {pp.title}')

    except LegalDocument.DoesNotExist:
        print('❌ Privacy policy not found in database')
    except Exception as e:
        print(f'❌ Error updating privacy policy: {e}')

if __name__ == '__main__':
    update_privacy_policy()
