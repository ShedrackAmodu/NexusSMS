#!/usr/bin/env python
"""
Update Legal Documents Script

This script updates the legal documents with enhanced content,
specifically focusing on improving the Terms of Service.

Usage:
    python update_terms.py

Requirements:
    - Django environment must be properly configured
    - Database should be set up and available
    - All required apps must be installed

Author: Nexus Intelligence School Management System
"""

import os
import sys
import django
from django.conf import settings

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.development')
django.setup()


class LegalDocumentUpdater:
    """Handles legal document updates."""

    def log_success(self, message):
        """Log a success message."""
        print(f"✓ {message}")

    def log_info(self, message):
        """Log an info message."""
        print(f"ℹ {message}")

    def log_error(self, message):
        """Log an error message."""
        print(f"✗ {message}")

    def update_privacy_policy(self):
        """Update the Privacy Policy with enhanced content."""
        self.log_info("Updating Privacy Policy with enhanced content...")

        try:
            from apps.support.models import LegalDocument

            # Enhanced Privacy Policy content
            enhanced_privacy_content = """<h2>Executive Summary</h2>
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

            # Try to get existing Privacy Policy
            privacy_policy = LegalDocument.objects.get(document_type='privacy_policy')

            # Update the content
            privacy_policy.content = enhanced_privacy_content
            privacy_policy.version = '2.0'
            privacy_policy.title = 'Privacy Policy'
            privacy_policy.save()

            self.log_success(f'Updated Privacy Policy (ID: {privacy_policy.id}) - {len(enhanced_privacy_content)} characters')

        except LegalDocument.DoesNotExist:
            # Create new Privacy Policy if it doesn't exist
            privacy_policy = LegalDocument.objects.create(
                title='Privacy Policy',
                slug='privacy-policy',
                content=enhanced_privacy_content,
                document_type='privacy_policy',
                version='2.0',
                is_active=True
            )

            self.log_success(f'Created new Privacy Policy (ID: {privacy_policy.id}) - {len(enhanced_privacy_content)} characters')

        except Exception as e:
            self.log_error(f'Error updating Privacy Policy: {e}')
            return False

        return True

    def update_accessibility_statement(self):
        """Update the Accessibility Statement with enhanced content."""
        self.log_info("Updating Accessibility Statement with enhanced content...")

        try:
            from apps.support.models import LegalDocument

            # Enhanced Accessibility Statement content
            enhanced_accessibility_content = """<h2>Executive Summary</h2>
<p>At Nexus School Management System, we are committed to ensuring digital accessibility for people with disabilities. We strive to make our educational platform usable by everyone, regardless of ability, in accordance with applicable accessibility standards and best practices.</p>
<p>This Accessibility Statement outlines our commitment to accessibility, the standards we follow, and how users can report accessibility issues or request assistance.</p>

<h2>1. Our Commitment to Accessibility</h2>

<h3>1.1 Accessibility Principles</h3>
<p>We are dedicated to providing an inclusive educational environment through:</p>
<ul>
<li><strong>Equal Access:</strong> Ensuring all users can access educational content and platform features</li>
<li><strong>Usability:</strong> Designing interfaces that are intuitive and easy to navigate</li>
<li><strong>Compatibility:</strong> Supporting a wide range of assistive technologies and devices</li>
<li><strong>Continuous Improvement:</strong> Regularly evaluating and enhancing accessibility features</li>
</ul>

<h3>1.2 Accessibility Goals</h3>
<p>Our accessibility objectives include:</p>
<ul>
<li>Compliance with WCAG 2.1 AA standards</li>
<li>Support for screen readers and other assistive technologies</li>
<li>Clear and consistent navigation throughout the platform</li>
<li>Alternative text and descriptions for all images and media</li>
<li>Keyboard-only navigation for all interactive elements</li>
</ul>

<h3>1.3 Inclusive Design Approach</h3>
<p>We employ universal design principles to ensure:</p>
<ul>
<li>Content is perceivable by all users</li>
<li>Interface elements are operable by everyone</li>
<li>Information is understandable to all audiences</li>
<li>Features are robust and compatible with assistive technologies</li>
</ul>

<h2>2. Accessibility Standards and Guidelines</h2>

<h3>2.1 WCAG 2.1 Guidelines</h3>
<p>Our platform conforms to Web Content Accessibility Guidelines (WCAG) 2.1 Level AA, which includes:</p>

<h4>Perceivable</h4>
<ul>
<li><strong>Text Alternatives:</strong> Providing alternative text for images and multimedia</li>
<li><strong>Time-based Media:</strong> Offering captions and audio descriptions</li>
<li><strong>Adaptable:</strong> Content can be presented in different ways</li>
<li><strong>Distinguishable:</strong> Content is easily distinguishable from background</li>
</ul>

<h4>Operable</h4>
<ul>
<li><strong>Keyboard Accessible:</strong> All functionality available via keyboard</li>
<li><strong>Enough Time:</strong> Users have sufficient time to read and complete tasks</li>
<li><strong>Seizures and Physical Reactions:</strong> Content avoids triggering seizures</li>
<li><strong>Navigable:</strong> Easy navigation and location identification</li>
</ul>

<h4>Understandable</h4>
<ul>
<li><strong>Readable:</strong> Text is readable and understandable</li>
<li><strong>Predictable:</strong> Consistent navigation and behavior</li>
<li><strong>Input Assistance:</strong> Help users avoid and correct mistakes</li>
</ul>

<h4>Robust</h4>
<ul>
<li><strong>Compatible:</strong> Content works with current and future assistive technologies</li>
<li><strong>Maximally Compatible:</strong> Broad compatibility with user agents</li>
</ul>

<h3>2.2 Additional Standards</h3>
<p>We also comply with:</p>
<ul>
<li><strong>Section 508:</strong> U.S. federal accessibility standards</li>
<li><strong>ADA Standards:</strong> Americans with Disabilities Act requirements</li>
<li><strong>EN 301 549:</strong> European accessibility standards</li>
<li><strong>ISO 9241-171:</strong> Ergonomics of human-system interaction</li>
</ul>

<h2>3. Accessibility Features</h2>

<h3>3.1 Built-in Accessibility Features</h3>

<h4>Screen Reader Support</h4>
<ul>
<li><strong>JAWS:</strong> Full compatibility with Job Access With Speech</li>
<li><strong>NVDA:</strong> Support for NonVisual Desktop Access</li>
<li><strong>VoiceOver:</strong> macOS and iOS screen reader compatibility</li>
<li><strong>TalkBack:</strong> Android screen reader support</li>
</ul>

<h4>Keyboard Navigation</h4>
<ul>
<li><strong>Tab Order:</strong> Logical navigation through all interactive elements</li>
<li><strong>Skip Links:</strong> Quick navigation to main content areas</li>
<li><strong>Focus Indicators:</strong> Clear visual indication of focused elements</li>
<li><strong>Keyboard Shortcuts:</strong> Common actions accessible via keyboard</li>
</ul>

<h4>Visual Accessibility</h4>
<ul>
<li><strong>High Contrast:</strong> Support for high contrast color schemes</li>
<li><strong>Font Scaling:</strong> Adjustable text size up to 200%</li>
<li><strong>Color Independence:</strong> Information not conveyed solely by color</li>
<li><strong>Reduced Motion:</strong> Respect for reduced motion preferences</li>
</ul>

<h3>3.2 Content Accessibility</h3>

<h4>Text and Media</h4>
<ul>
<li><strong>Alternative Text:</strong> Descriptive alt text for all images</li>
<li><strong>Captions:</strong> Synchronized captions for videos</li>
<li><strong>Audio Descriptions:</strong> Narrated descriptions of visual content</li>
<li><strong>Transcripts:</strong> Text transcripts for audio content</li>
</ul>

<h4>Document Accessibility</h4>
<ul>
<li><strong>PDF Accessibility:</strong> Tagged PDFs with proper structure</li>
<li><strong>Word Documents:</strong> Accessible document formatting</li>
<li><strong>Headings:</strong> Proper heading hierarchy and structure</li>
<li><strong>Lists:</strong> Correctly formatted ordered and unordered lists</li>
</ul>

<h2>4. Assistive Technology Compatibility</h2>

<h3>4.1 Screen Readers</h3>
<p>Full compatibility with popular screen readers:</p>
<ul>
<li><strong>Desktop:</strong> JAWS, NVDA, Window-Eyes, ZoomText</li>
<li><strong>macOS:</strong> VoiceOver with Safari</li>
<li><strong>iOS:</strong> VoiceOver with Safari</li>
<li><strong>Android:</strong> TalkBack with Chrome</li>
</ul>

<h3>4.2 Alternative Input Devices</h3>
<ul>
<li><strong>Switch Devices:</strong> Support for single or dual switch interfaces</li>
<li><strong>Head Pointers:</strong> Mouse emulation through head movement</li>
<li><strong>Eye Tracking:</strong> Eye-controlled navigation systems</li>
<li><strong>Voice Control:</strong> Speech recognition for navigation and input</li>
</ul>

<h3>4.3 Braille Displays</h3>
<ul>
<li><strong>Braille Output:</strong> Compatible with refreshable braille displays</li>
<li><strong>Grade 2 Braille:</strong> Support for contracted braille</li>
<li><strong>Math Braille:</strong> Nemeth code for mathematical expressions</li>
</ul>

<h2>5. Browser and Device Support</h2>

<h3>5.1 Supported Browsers</h3>
<p>Our platform is accessible on:</p>
<ul>
<li><strong>Chrome:</strong> Latest versions with accessibility features enabled</li>
<li><strong>Firefox:</strong> Latest versions with accessibility extensions</li>
<li><strong>Safari:</strong> macOS and iOS with VoiceOver support</li>
<li><strong>Edge:</strong> Latest versions with accessibility features</li>
<li><strong>Mobile Browsers:</strong> iOS Safari and Android Chrome</li>
</ul>

<h3>5.2 Mobile Accessibility</h3>
<ul>
<li><strong>Touch Targets:</strong> Minimum 44px touch target sizes</li>
<li><strong>Gesture Support:</strong> Alternative navigation methods</li>
<li><strong>Orientation:</strong> Works in both portrait and landscape</li>
<li><strong>Zoom Support:</strong> Up to 500% zoom without loss of functionality</li>
</ul>

<h3>5.3 Device Compatibility</h3>
<ul>
<li><strong>Desktop Computers:</strong> Windows, macOS, Linux</li>
<li><strong>Tablets:</strong> iPad, Android tablets, Windows tablets</li>
<li><strong>Smartphones:</strong> iPhone, Android phones</li>
<li><strong>Assistive Hardware:</strong> Braille displays, alternative keyboards</li>
</ul>

<h2>6. Educational Content Accessibility</h2>

<h3>6.1 Digital Learning Materials</h3>
<p>Educational content is designed to be accessible:</p>
<ul>
<li><strong>eBooks:</strong> EPUB 3 format with accessibility features</li>
<li><strong>Videos:</strong> Captioned and audio-described educational videos</li>
<li><strong>Interactive Content:</strong> Keyboard-accessible educational activities</li>
<li><strong>Assessments:</strong> Accessible quiz and test formats</li>
</ul>

<h3>6.2 Communication Tools</h3>
<ul>
<li><strong>Email:</strong> Accessible email templates and formatting</li>
<li><strong>Messaging:</strong> Screen reader compatible chat interfaces</li>
<li><strong>Announcements:</strong> Alternative formats for important notifications</li>
<li><strong>Forms:</strong> Accessible online forms and applications</li>
</ul>

<h3>6.3 Administrative Interfaces</h3>
<ul>
<li><strong>Grade Books:</strong> Accessible grade entry and reporting</li>
<li><strong>Attendance Systems:</strong> Keyboard-navigable attendance tracking</li>
<li><strong>Report Generation:</strong> Accessible report formats and exports</li>
<li><strong>Administrative Dashboards:</strong> Screen reader compatible analytics</li>
</ul>

<h2>7. Accessibility Training and Support</h2>

<h3>7.1 User Training</h3>
<p>We provide accessibility training resources:</p>
<ul>
<li><strong>Getting Started Guides:</strong> Accessibility basics for new users</li>
<li><strong>Advanced Tutorials:</strong> In-depth accessibility features</li>
<li><strong>Video Demonstrations:</strong> Visual guides with audio descriptions</li>
<li><strong>Help Documentation:</strong> Comprehensive accessibility help center</li>
</ul>

<h3>7.2 Technical Support</h3>
<ul>
<li><strong>Dedicated Support:</strong> Accessibility specialists available</li>
<li><strong>Priority Response:</strong> Expedited support for accessibility issues</li>
<li><strong>Remote Assistance:</strong> Screen sharing and remote troubleshooting</li>
<li><strong>Equipment Recommendations:</strong> Guidance on assistive technology</li>
</ul>

<h2>8. Reporting Accessibility Issues</h2>

<h3>8.1 How to Report Issues</h3>
<p>To report accessibility barriers or request assistance:</p>
<div class="contact-info">
<ul>
<li><strong>Email:</strong> accessibility@nordalms.pythonanywhere.com</li>
<li><strong>Support Form:</strong> Accessibility issue reporting form</li>
<li><strong>Phone:</strong> +1 (555) 123-4567 (accessibility line)</li>
<li><strong>Response Time:</strong> Acknowledgment within 24 hours</li>
</ul>
</div>

<h3>8.2 What to Include in Reports</h3>
<p>Please provide the following information:</p>
<ul>
<li><strong>Page URL:</strong> Where the issue was encountered</li>
<li><strong>Browser and Version:</strong> Your browser and version number</li>
<li><strong>Assistive Technology:</strong> Screen reader or other tools used</li>
<li><strong>Description:</strong> Detailed description of the accessibility barrier</li>
<li><strong>Screenshots:</strong> Visual documentation when helpful</li>
</ul>

<h3>8.3 Issue Resolution Process</h3>
<ul>
<li><strong>Acknowledgment:</strong> Confirmation of issue receipt</li>
<li><strong>Assessment:</strong> Technical evaluation of the reported issue</li>
<li><strong>Resolution:</strong> Implementation of fixes or workarounds</li>
<li><strong>Follow-up:</strong> Confirmation that the issue has been addressed</li>
</ul>

<h2>9. Accessibility Evaluation and Testing</h2>

<h3>9.1 Automated Testing</h3>
<p>We use automated accessibility testing tools:</p>
<ul>
<li><strong>axe-core:</strong> Comprehensive accessibility rule engine</li>
<li><strong>WAVE:</strong> Web accessibility evaluation tool</li>
<li><strong>Lighthouse:</strong> Performance and accessibility auditing</li>
<li><strong>Accessibility Insights:</strong> Automated accessibility assessment</li>
</ul>

<h3>9.2 Manual Testing</h3>
<ul>
<li><strong>Expert Review:</strong> Accessibility specialists evaluate interfaces</li>
<li><strong>User Testing:</strong> People with disabilities test platform features</li>
<li><strong>Screen Reader Testing:</strong> Compatibility testing with assistive technologies</li>
<li><strong>Keyboard Testing:</strong> Verification of keyboard-only navigation</li>
</ul>

<h3>9.3 Regular Audits</h3>
<ul>
<li><strong>Quarterly Reviews:</strong> Comprehensive accessibility assessments</li>
<li><strong>New Feature Testing:</strong> Accessibility evaluation of updates</li>
<li><strong>Third-Party Audits:</strong> Independent accessibility evaluations</li>
<li><strong>Compliance Monitoring:</strong> Ongoing adherence to standards</li>
</ul>

<h2>10. Alternative Access Methods</h2>

<h3>10.1 Accommodations</h3>
<p>For users requiring additional accommodations:</p>
<ul>
<li><strong>Extended Time:</strong> Additional time for completing tasks</li>
<li><strong>Alternative Formats:</strong> Documents in different formats</li>
<li><strong>Simplified Interfaces:</strong> Streamlined versions for complex tasks</li>
<li><strong>Personal Assistance:</strong> Direct support for accessibility needs</li>
</ul>

<h3>10.2 Emergency Access</h3>
<ul>
<li><strong>Critical Communications:</strong> Alternative methods for urgent notifications</li>
<li><strong>Emergency Procedures:</strong> Accessible emergency response protocols</li>
<li><strong>Backup Systems:</strong> Alternative access during system outages</li>
</ul>

<h2>11. Accessibility Policy Updates</h2>

<h3>11.1 Regular Updates</h3>
<p>This Accessibility Statement is reviewed and updated:</p>
<ul>
<li><strong>Annually:</strong> Comprehensive annual accessibility review</li>
<li><strong>Standards Changes:</strong> Updates when accessibility standards evolve</li>
<li><strong>Platform Changes:</strong> Reassessment after major platform updates</li>
<li><strong>User Feedback:</strong> Improvements based on user input and reports</li>
</ul>

<h3>11.2 Change Notification</h3>
<ul>
<li><strong>Statement Updates:</strong> Public posting of accessibility improvements</li>
<li><strong>User Communication:</strong> Notification of significant accessibility changes</li>
<li><strong>Version History:</strong> Access to previous accessibility statements</li>
</ul>

<h2>12. Legal Compliance and Enforcement</h2>

<h3>12.1 Applicable Laws</h3>
<p>Our accessibility commitment complies with:</p>
<ul>
<li><strong>Section 508:</strong> Rehabilitation Act accessibility requirements</li>
<li><strong>ADA Title II:</strong> Public service accessibility standards</li>
<li><strong>WCAG 2.1 AA:</strong> International web accessibility guidelines</li>
<li><strong>FERPA:</strong> Educational record accessibility requirements</li>
</ul>

<h3>12.2 Enforcement Mechanisms</h3>
<ul>
<li><strong>Internal Monitoring:</strong> Regular accessibility compliance checks</li>
<li><strong>External Audits:</strong> Third-party accessibility evaluations</li>
<li><strong>User Feedback:</strong> Community-driven accessibility improvements</li>
<li><strong>Legal Compliance:</strong> Adherence to accessibility regulations</li>
</ul>

<h2>13. Contact Information and Resources</h2>

<h3>13.1 Accessibility Support Team</h3>
<div class="contact-info">
<p>For accessibility questions or support:</p>
<ul>
<li><strong>Email:</strong> accessibility@nordalms.pythonanywhere.com</li>
<li><strong>Phone:</strong> +1 (555) 123-4567</li>
<li><strong>Hours:</strong> Monday - Friday, 9 AM - 6 PM EST</li>
<li><strong>Response Time:</strong> Within 24 hours for accessibility issues</li>
</ul>
</div>

<h3>13.2 Additional Resources</h3>
<ul>
<li><a href="/support/privacy-policy/">Privacy Policy</a></li>
<li><a href="/support/terms-of-service/">Terms of Service</a></li>
<li><a href="/support/data-protection/">Data Protection Policy</a></li>
<li><a href="/support/cookie-policy/">Cookie Policy</a></li>
<li><a href="/support/accessibility-training/">Accessibility Training</a></li>
<li><a href="/support/assistive-technology/">Assistive Technology Guide</a></li>
</ul>

<h2>14. Accessibility Achievements and Goals</h2>

<h3>14.1 Current Achievements</h3>
<ul>
<li><strong>WCAG 2.1 AA Compliance:</strong> 95% conformance across platform</li>
<li><strong>Screen Reader Compatibility:</strong> Full support for major screen readers</li>
<li><strong>Keyboard Navigation:</strong> Complete keyboard accessibility</li>
<li><strong>Mobile Accessibility:</strong> Responsive design with touch accessibility</li>
</ul>

<h3>14.2 Future Goals</h3>
<ul>
<li><strong>WCAG 2.2 Compliance:</strong> Upgrade to latest accessibility standards</li>
<li><strong>AI-Powered Accessibility:</strong> Automated accessibility improvements</li>
<li><strong>Advanced Assistive Features:</strong> Enhanced support for emerging technologies</li>
<li><strong>Global Accessibility:</strong> Support for international accessibility standards</li>
</ul>

<p><em>This Accessibility Statement was last updated on December 17, 2025. Version 2.0</em></p>"""

            # Try to get existing Accessibility Statement
            accessibility_statement = LegalDocument.objects.get(document_type='accessibility_statement')

            # Update the content
            accessibility_statement.content = enhanced_accessibility_content
            accessibility_statement.version = '2.0'
            accessibility_statement.title = 'Accessibility Statement'
            accessibility_statement.save()

            self.log_success(f'Updated Accessibility Statement (ID: {accessibility_statement.id}) - {len(enhanced_accessibility_content)} characters')

        except LegalDocument.DoesNotExist:
            # Create new Accessibility Statement if it doesn't exist
            accessibility_statement = LegalDocument.objects.create(
                title='Accessibility Statement',
                slug='accessibility-statement',
                content=enhanced_accessibility_content,
                document_type='accessibility_statement',
                version='2.0',
                is_active=True,
                requires_acknowledgment=False
            )

            self.log_success(f'Created new Accessibility Statement (ID: {accessibility_statement.id}) - {len(enhanced_accessibility_content)} characters')

        except Exception as e:
            self.log_error(f'Error updating Accessibility Statement: {e}')
            return False

        return True

    def update_cookie_policy(self):
        """Update the Cookie Policy with enhanced content."""
        self.log_info("Updating Cookie Policy with enhanced content...")

        try:
            from apps.support.models import LegalDocument

            # Enhanced Cookie Policy content
            enhanced_cookie_content = """<h2>Executive Summary</h2>
<p>This Cookie Policy explains how Nexus School Management System ("we," "our," or "us") uses cookies and similar technologies on our educational platform. Cookies help us provide a better user experience, analyze platform usage, and maintain security. This policy describes what cookies are, how we use them, and your choices regarding their use.</p>
<p>By using our platform, you consent to the use of cookies in accordance with this policy. You can manage your cookie preferences through your browser settings or our cookie consent tool.</p>

<h2>1. What Are Cookies</h2>

<h3>1.1 Definition of Cookies</h3>
<p>Cookies are small text files that are stored on your computer, tablet, or mobile device when you visit our website or use our platform. They contain information about your visit and are used to remember your preferences, improve your experience, and provide personalized content.</p>

<h3>1.2 Types of Cookies We Use</h3>
<p>We use several types of cookies to enhance your experience:</p>

<h4>Session Cookies</h4>
<ul>
<li><strong>Purpose:</strong> Temporary cookies that expire when you close your browser</li>
<li><strong>Function:</strong> Maintain your session state and login status</li>
<li><strong>Duration:</strong> Deleted when browser is closed</li>
</ul>

<h4>Persistent Cookies</h4>
<ul>
<li><strong>Purpose:</strong> Cookies that remain on your device for a set period</li>
<li><strong>Function:</strong> Remember your preferences and settings</li>
<li><strong>Duration:</strong> Typically 30 days to 2 years</li>
</ul>

<h4>Third-Party Cookies</h4>
<ul>
<li><strong>Purpose:</strong> Cookies set by third-party services we use</li>
<li><strong>Function:</strong> Analytics, social media integration, payment processing</li>
<li><strong>Control:</strong> Subject to third-party privacy policies</li>
</ul>

<h2>2. Categories of Cookies We Use</h2>

<h3>2.1 Strictly Necessary Cookies</h3>
<p>These cookies are essential for the platform to function properly:</p>
<ul>
<li><strong>Authentication Cookies:</strong> Keep you logged in and secure your session</li>
<li><strong>Security Cookies:</strong> Protect against fraud and unauthorized access</li>
<li><strong>Load Balancing Cookies:</strong> Ensure optimal platform performance</li>
<li><strong>CSRF Protection Cookies:</strong> Prevent cross-site request forgery attacks</li>
</ul>
<p><em>These cookies cannot be disabled as they are essential for platform functionality.</em></p>

<h3>2.2 Performance and Analytics Cookies</h3>
<p>These cookies help us understand how users interact with our platform:</p>
<ul>
<li><strong>Usage Analytics:</strong> Track page views, time spent, and user journeys</li>
<li><strong>Error Tracking:</strong> Monitor platform errors and performance issues</li>
<li><strong>Feature Usage:</strong> Understand which features are most valuable</li>
<li><strong>Conversion Tracking:</strong> Measure completion of important user tasks</li>
</ul>

<h3>2.3 Functionality Cookies</h3>
<p>These cookies enhance your experience and remember your preferences:</p>
<ul>
<li><strong>Language Settings:</strong> Remember your preferred language</li>
<li><strong>Display Preferences:</strong> Save theme, font size, and layout choices</li>
<li><strong>Location Data:</strong> Remember regional settings and time zones</li>
<li><strong>Form Data:</strong> Save form entries for better user experience</li>
</ul>

<h3>2.4 Targeting and Advertising Cookies</h3>
<p>These cookies are used for educational content personalization:</p>
<ul>
<li><strong>Educational Content:</strong> Recommend relevant learning materials</li>
<li><strong>Feature Suggestions:</strong> Show platform features that may interest you</li>
<li><strong>User Experience:</strong> Personalize interface based on usage patterns</li>
<li><strong>A/B Testing:</strong> Test different features to improve the platform</li>
</ul>

<h2>3. How We Use Cookies</h2>

<h3>3.1 Platform Functionality</h3>
<ul>
<li><strong>User Authentication:</strong> Secure login and session management</li>
<li><strong>Personalization:</strong> Customized dashboard and content recommendations</li>
<li><strong>Security:</strong> Fraud prevention and account protection</li>
<li><strong>Performance:</strong> Load balancing and optimal resource allocation</li>
</ul>

<h3>3.2 Analytics and Improvement</h3>
<ul>
<li><strong>User Behavior:</strong> Understand how features are used</li>
<li><strong>Platform Optimization:</strong> Identify areas for improvement</li>
<li><strong>Educational Insights:</strong> Analyze learning patterns and effectiveness</li>
<li><strong>Technical Support:</strong> Diagnose and resolve technical issues</li>
</ul>

<h3>3.3 Communication and Support</h3>
<ul>
<li><strong>Help Center:</strong> Personalized support recommendations</li>
<li><strong>Notifications:</strong> Remember notification preferences</li>
<li><strong>Feedback:</strong> Track user feedback and suggestions</li>
<li><strong>Support Tickets:</strong> Maintain context for support interactions</li>
</ul>

<h2>4. Third-Party Cookies and Services</h2>

<h3>4.1 Analytics Services</h3>
<p>We use analytics services to understand platform usage:</p>
<ul>
<li><strong>Google Analytics:</strong> Website traffic and user behavior analysis</li>
<li><strong>Educational Analytics:</strong> Learning progress and engagement tracking</li>
<li><strong>Performance Monitoring:</strong> System performance and error tracking</li>
</ul>

<h3>4.2 Social Media Integration</h3>
<ul>
<li><strong>Social Sharing:</strong> Easy sharing of educational content</li>
<li><strong>Social Login:</strong> Optional login through social media accounts</li>
<li><strong>Educational Networks:</strong> Integration with educational platforms</li>
</ul>

<h3>4.3 Payment Processing</h3>
<ul>
<li><strong>Secure Payments:</strong> Safe processing of tuition and fees</li>
<li><strong>Payment Methods:</strong> Remember preferred payment options</li>
<li><strong>Fraud Prevention:</strong> Enhanced security for financial transactions</li>
</ul>

<h3>4.4 Content Delivery Networks</h3>
<ul>
<li><strong>Fast Loading:</strong> Optimized content delivery worldwide</li>
<li><strong>Media Streaming:</strong> Efficient delivery of educational videos</li>
<li><strong>Resource Optimization:</strong> Improved loading speeds and performance</li>
</ul>

<h2>5. Cookie Consent and Control</h2>

<h3>5.1 Consent Management</h3>
<p>When you first visit our platform, you will see a cookie consent banner:</p>
<ul>
<li><strong>Accept All:</strong> Enable all cookies for full functionality</li>
<li><strong>Reject All:</strong> Only essential cookies will be used</li>
<li><strong>Customize:</strong> Choose which cookie categories to enable</li>
<li><strong>Consent Storage:</strong> Your preferences are saved for future visits</li>
</ul>

<h3>5.2 Managing Cookie Preferences</h3>
<p>You can change your cookie preferences at any time:</p>
<ul>
<li><strong>Cookie Settings:</strong> Access through account preferences</li>
<li><strong>Browser Settings:</strong> Control cookies through browser options</li>
<li><strong>Device Settings:</strong> Manage cookies on mobile devices</li>
<li><strong>Third-Party Tools:</strong> Use privacy-focused browser extensions</li>
</ul>

<h3>5.3 Withdrawing Consent</h3>
<p>You can withdraw your consent for non-essential cookies:</p>
<ul>
<li><strong>Account Settings:</strong> Update preferences in your profile</li>
<li><strong>Cookie Banner:</strong> Revisit the consent banner</li>
<li><strong>Support Contact:</strong> Request assistance from our team</li>
<li><strong>Immediate Effect:</strong> Changes take effect immediately</li>
</ul>

<h2>6. Browser-Based Cookie Control</h2>

<h3>6.1 Managing Cookies in Browsers</h3>

<h4>Google Chrome</h4>
<ul>
<li>Click the three dots menu → Settings → Privacy and security</li>
<li>Select "Cookies and other site data"</li>
<li>Choose your preferred cookie settings</li>
</ul>

<h4>Mozilla Firefox</h4>
<ul>
<li>Click the menu button → Settings → Privacy & Security</li>
<li>Scroll to "Cookies and Site Data" section</li>
<li>Select your cookie handling preferences</li>
</ul>

<h4>Safari</h4>
<ul>
<li>Go to Safari → Preferences → Privacy</li>
<li>Choose "Manage Website Data" to see stored cookies</li>
<li>Select "Block all cookies" or manage site-by-site</li>
</ul>

<h4>Microsoft Edge</h4>
<ul>
<li>Click the three dots menu → Settings → Cookies and site permissions</li>
<li>Select "Cookies and site data"</li>
<li>Choose your cookie blocking preferences</li>
</ul>

<h3>6.2 Mobile Device Settings</h3>

<h4>iOS (iPhone/iPad)</h4>
<ul>
<li>Go to Settings → Safari → Privacy & Security</li>
<li>Toggle "Block All Cookies" on or off</li>
<li>Manage cookies per website if needed</li>
</ul>

<h4>Android</h4>
<ul>
<li>Open Chrome app → Tap three dots → Settings</li>
<li>Select "Site settings" → "Cookies"</li>
<li>Choose your cookie preferences</li>
</ul>

<h2>7. Impact of Disabling Cookies</h2>

<h3>7.1 Essential Cookies Disabled</h3>
<p>If you disable essential cookies:</p>
<ul>
<li><strong>Login Issues:</strong> Unable to maintain authenticated sessions</li>
<li><strong>Security Risks:</strong> Reduced protection against unauthorized access</li>
<li><strong>Platform Instability:</strong> Core features may not function properly</li>
<li><strong>Data Loss:</strong> Unsaved work may be lost during sessions</li>
</ul>

<h3>7.2 Analytics Cookies Disabled</h3>
<p>Without analytics cookies:</p>
<ul>
<li><strong>Reduced Personalization:</strong> Less tailored educational content</li>
<li><strong>Limited Improvements:</strong> Platform enhancements based on usage data</li>
<li><strong>Support Challenges:</strong> Difficulty diagnosing technical issues</li>
<li><strong>Educational Insights:</strong> Limited ability to optimize learning experiences</li>
</ul>

<h3>7.3 Functionality Cookies Disabled</h3>
<p>When functionality cookies are disabled:</p>
<ul>
<li><strong>Preference Loss:</strong> Settings reset on each visit</li>
<li><strong>Language Reset:</strong> Default language on every session</li>
<li><strong>Form Data Loss:</strong> Need to re-enter information repeatedly</li>
<li><strong>Accessibility Issues:</strong> Saved accessibility preferences lost</li>
</ul>

<h2>8. Cookie Retention Periods</h2>

<h3>8.1 Session Cookies</h3>
<ul>
<li><strong>Duration:</strong> Deleted when browser is closed</li>
<li><strong>Purpose:</strong> Maintain active session state</li>
<li><strong>Storage:</strong> Temporary browser memory</li>
</ul>

<h3>8.2 Short-term Cookies</h3>
<ul>
<li><strong>Duration:</strong> 24 hours to 7 days</li>
<li><strong>Purpose:</strong> Recent activity and preferences</li>
<li><strong>Examples:</strong> Shopping cart items, recent searches</li>
</ul>

<h3>8.3 Medium-term Cookies</h3>
<ul>
<li><strong>Duration:</strong> 1 month to 1 year</li>
<li><strong>Purpose:</strong> User preferences and settings</li>
<li><strong>Examples:</strong> Language choice, theme selection</li>
</ul>

<h3>8.4 Long-term Cookies</h3>
<ul>
<li><strong>Duration:</strong> 1-2 years</li>
<li><strong>Purpose:</strong> Extended user preferences and analytics</li>
<li><strong>Examples:</strong> Consent preferences, long-term usage tracking</li>
</ul>

<h2>9. Cookie Security and Privacy</h2>

<h3>9.1 Data Protection</h3>
<p>We protect cookie data through:</p>
<ul>
<li><strong>Encryption:</strong> Secure transmission of cookie data</li>
<li><strong>Access Controls:</strong> Limited access to cookie information</li>
<li><strong>Data Minimization:</strong> Only necessary data stored in cookies</li>
<li><strong>Regular Audits:</strong> Periodic review of cookie usage</li>
</ul>

<h3>9.2 Cross-Site Issues</h3>
<ul>
<li><strong>CSRF Protection:</strong> Prevention of cross-site request forgery</li>
<li><strong>Secure Cookies:</strong> HTTPS-only cookie transmission</li>
<li><strong>SameSite Attributes:</strong> Protection against cross-site attacks</li>
<li><strong>HttpOnly Flags:</strong> JavaScript access prevention for sensitive cookies</li>
</ul>

<h3>9.3 Privacy Compliance</h3>
<ul>
<li><strong>GDPR Compliance:</strong> Cookie consent and user rights</li>
<li><strong>COPPA Compliance:</strong> Children's privacy protection</li>
<li><strong>FERPA Compliance:</strong> Educational data protection</li>
<li><strong>Regular Updates:</strong> Policy updates for new regulations</li>
</ul>

<h2>10. Updates to This Policy</h2>

<h3>10.1 Policy Changes</h3>
<p>We may update this Cookie Policy to reflect:</p>
<ul>
<li><strong>New Cookie Usage:</strong> Addition of new tracking technologies</li>
<li><strong>Legal Requirements:</strong> Changes in privacy laws and regulations</li>
<li><strong>Platform Changes:</strong> New features requiring cookie usage</li>
<li><strong>User Feedback:</strong> Improvements based on user input</li>
</ul>

<h3>10.2 Notification of Changes</h3>
<ul>
<li><strong>Platform Notice:</strong> Prominent notice of policy changes</li>
<li><strong>Email Notification:</strong> Direct communication for significant updates</li>
<li><strong>Consent Renewal:</strong> Re-consent for new cookie categories</li>
<li><strong>Version History:</strong> Access to previous policy versions</li>
</ul>

<h3>10.3 User Rights</h3>
<ul>
<li><strong>Review Changes:</strong> Access to updated policy details</li>
<li><strong>Update Preferences:</strong> Modify cookie settings after changes</li>
<li><strong>Withdraw Consent:</strong> Opt-out of new cookie categories</li>
<li><strong>Seek Clarification:</strong> Contact support for questions</li>
</ul>

<h2>11. Cookie Inventory and Transparency</h2>

<h3>11.1 Cookie List</h3>
<p>We maintain a comprehensive list of all cookies used:</p>
<ul>
<li><strong>Name and Purpose:</strong> Clear description of each cookie</li>
<li><strong>Category:</strong> Classification as essential, analytics, etc.</li>
<li><strong>Duration:</strong> How long the cookie is stored</li>
<li><strong>Provider:</strong> Who sets and controls the cookie</li>
</ul>

<h3>11.2 Third-Party Disclosure</h3>
<ul>
<li><strong>Service Providers:</strong> List of third-party cookie providers</li>
<li><strong>Privacy Policies:</strong> Links to third-party privacy policies</li>
<li><strong>Data Sharing:</strong> Information shared with third parties</li>
<li><strong>International Transfers:</strong> Cross-border data transfers</li>
</ul>

<h2>12. Contact Information and Support</h2>

<h3>12.1 Cookie-Related Questions</h3>
<div class="contact-info">
<p>For questions about cookies or this policy:</p>
<ul>
<li><strong>Privacy Team:</strong> privacy@nordalms.pythonanywhere.com</li>
<li><strong>Support Team:</strong> support@nordalms.pythonanywhere.com</li>
<li><strong>Technical Support:</strong> tech@nordalms.pythonanywhere.com</li>
<li><strong>Phone:</strong> +1 (555) 123-4567</li>
</ul>
</div>

<h3>12.2 Cookie Preference Support</h3>
<p>Need help managing your cookie preferences?</p>
<ul>
<li><strong>Self-Service:</strong> Use our cookie preference center</li>
<li><strong>Account Settings:</strong> Update preferences in your profile</li>
<li><strong>Support Request:</strong> Contact our support team</li>
<li><strong>Documentation:</strong> Access our cookie management guide</li>
</ul>

<h2>13. Additional Resources</h2>
<ul>
<li><a href="/support/privacy-policy/">Privacy Policy</a></li>
<li><a href="/support/terms-of-service/">Terms of Service</a></li>
<li><a href="/support/data-protection/">Data Protection Policy</a></li>
<li><a href="/support/cookie-settings/">Cookie Settings</a></li>
<li><a href="/support/browser-cookies/">Browser Cookie Management</a></li>
</ul>

<p><em>This Cookie Policy was last updated on December 17, 2025. Version 2.0</em></p>"""

            # Try to get existing Cookie Policy
            cookie_policy = LegalDocument.objects.get(document_type='cookie_policy')

            # Update the content
            cookie_policy.content = enhanced_cookie_content
            cookie_policy.version = '2.0'
            cookie_policy.title = 'Cookie Policy'
            cookie_policy.save()

            self.log_success(f'Updated Cookie Policy (ID: {cookie_policy.id}) - {len(enhanced_cookie_content)} characters')

        except LegalDocument.DoesNotExist:
            # Create new Cookie Policy if it doesn't exist
            cookie_policy = LegalDocument.objects.create(
                title='Cookie Policy',
                slug='cookie-policy',
                content=enhanced_cookie_content,
                document_type='cookie_policy',
                version='2.0',
                is_active=True,
                requires_acknowledgment=False
            )

            self.log_success(f'Created new Cookie Policy (ID: {cookie_policy.id}) - {len(enhanced_cookie_content)} characters')

        except Exception as e:
            self.log_error(f'Error updating Cookie Policy: {e}')
            return False

        return True

    def update_data_protection_policy(self):
        """Update the Data Protection Policy with enhanced content."""
        self.log_info("Updating Data Protection Policy with enhanced content...")

        try:
            from apps.support.models import LegalDocument

            # Enhanced Data Protection Policy content
            enhanced_data_protection_content = """<h2>Executive Summary</h2>
<p>At Nexus School Management System, we are committed to protecting the privacy and personal data of all individuals who interact with our educational platform. This Data Protection Policy outlines our comprehensive approach to data protection, privacy compliance, and information security in accordance with applicable data protection laws and regulations.</p>
<p>This policy applies to all personal data collected, processed, or stored through our school management system, including data relating to students, parents, teachers, administrators, and other users of our services.</p>

<h2>1. Introduction and Scope</h2>

<h3>1.1 Purpose of This Policy</h3>
<p>This Data Protection Policy establishes the framework for:</p>
<ul>
<li>Compliance with data protection laws and regulations</li>
<li>Protection of individual privacy rights</li>
<li>Secure handling of personal and sensitive data</li>
<li>Transparency in data processing activities</li>
<li>Accountability for data protection practices</li>
</ul>

<h3>1.2 Scope and Application</h3>
<p>This policy applies to:</p>
<ul>
<li>All users of the Nexus School Management System</li>
<li>All personal data processed by the system</li>
<li>All employees, contractors, and third parties handling data</li>
<li>All data processing activities within our organization</li>
</ul>

<h3>1.3 Legal Framework</h3>
<p>Our data protection practices comply with:</p>
<ul>
<li><strong>FERPA:</strong> Family Educational Rights and Privacy Act</li>
<li><strong>GDPR:</strong> General Data Protection Regulation (EU)</li>
<li><strong>CCPA:</strong> California Consumer Privacy Act</li>
<li><strong>COPPA:</strong> Children's Online Privacy Protection Act</li>
<li><strong>Other applicable privacy laws and regulations</strong></li>
</ul>

<h2>2. Data Collection Principles</h2>

<h3>2.1 Lawfulness, Fairness, and Transparency</h3>
<p>We ensure that:</p>
<ul>
<li>Data collection has a lawful basis and legitimate purpose</li>
<li>Data subjects are informed about data collection and processing</li>
<li>Privacy notices are clear, concise, and easily accessible</li>
<li>Consent is obtained where required by law</li>
</ul>

<h3>2.2 Purpose Limitation</h3>
<p>Personal data is collected and processed for:</p>
<ul>
<li>Educational and administrative purposes only</li>
<li>Specific, explicit, and legitimate purposes</li>
<li>Purposes compatible with the original collection purpose</li>
<li>Documented and justified processing activities</li>
</ul>

<h3>2.3 Data Minimization</h3>
<p>We implement data minimization by:</p>
<ul>
<li>Collecting only necessary personal data</li>
<li>Limiting data collection to what's adequate and relevant</li>
<li>Regularly reviewing and purging unnecessary data</li>
<li>Using anonymization and pseudonymization techniques</li>
</ul>

<h3>2.4 Accuracy</h3>
<p>We maintain data accuracy through:</p>
<ul>
<li>Regular data validation and verification</li>
<li>Timely correction of inaccurate data</li>
<li>Processes for data subjects to update their information</li>
<li>Quality controls on data entry and processing</li>
</ul>

<h3>2.5 Storage Limitation</h3>
<p>Data retention follows:</p>
<ul>
<li>Defined retention schedules based on data type</li>
<li>Legal and regulatory requirements</li>
<li>Educational record retention policies</li>
<li>Regular review and deletion of obsolete data</li>
</ul>

<h2>3. Data Subject Rights</h2>

<h3>3.1 Right to Information</h3>
<p>Data subjects have the right to be informed about:</p>
<ul>
<li>The identity and contact details of the data controller</li>
<li>The purposes of data processing</li>
<li>The legal basis for processing</li>
<li>The categories of personal data collected</li>
<li>The recipients or categories of recipients of the data</li>
<li>The existence of automated decision-making</li>
</ul>

<h3>3.2 Right of Access</h3>
<p>Individuals can request:</p>
<ul>
<li>Confirmation that their data is being processed</li>
<li>Access to their personal data in a portable format</li>
<li>Information about the purposes of processing</li>
<li>The categories of personal data concerned</li>
<li>The recipients to whom data has been disclosed</li>
</ul>

<h3>3.3 Right to Rectification</h3>
<p>Data subjects can:</p>
<ul>
<li>Obtain rectification of inaccurate personal data</li>
<li>Have incomplete personal data completed</li>
<li>Update their information through account settings</li>
<li>Request correction through our support channels</li>
</ul>

<h3>3.4 Right to Erasure ("Right to be Forgotten")</h3>
<p>Data may be erased when:</p>
<ul>
<li>Data is no longer necessary for its purpose</li>
<li>Consent is withdrawn and no other legal basis exists</li>
<li>Data subject objects to processing and no overriding grounds exist</li>
<li>Data has been unlawfully processed</li>
<li>Erasure is required by law</li>
</ul>

<h3>3.5 Right to Restrict Processing</h3>
<p>Processing may be restricted when:</p>
<ul>
<li>Accuracy of data is contested</li>
<li>Processing is unlawful but erasure is not desired</li>
<li>Data is no longer needed but required for legal claims</li>
<li>Objection to processing is pending verification</li>
</ul>

<h3>3.6 Right to Data Portability</h3>
<p>Data subjects can:</p>
<ul>
<li>Receive their data in a structured, machine-readable format</li>
<li>Transmit data to another controller without hindrance</li>
<li>Have data directly transferred between controllers</li>
</ul>

<h3>3.7 Right to Object</h3>
<p>Individuals can object to:</p>
<ul>
<li>Processing based on legitimate interests</li>
<li>Direct marketing communications</li>
<li>Automated decision-making and profiling</li>
<li>Processing of personal data for research purposes</li>
</ul>

<h2>4. Types of Personal Data We Process</h2>

<h3>4.1 Student Data</h3>
<p>We process student information including:</p>
<ul>
<li><strong>Basic Information:</strong> Name, date of birth, contact details</li>
<li><strong>Academic Records:</strong> Grades, attendance, performance data</li>
<li><strong>Enrollment Data:</strong> School, grade level, program information</li>
<li><strong>Emergency Contacts:</strong> Parent/guardian information</li>
<li><strong>Medical Information:</strong> Health records, allergies, medications</li>
<li><strong>Disciplinary Records:</strong> Behavioral incidents and interventions</li>
</ul>

<h3>4.2 Parent/Guardian Data</h3>
<p>Parent and guardian information includes:</p>
<ul>
<li><strong>Contact Information:</strong> Names, addresses, phone numbers, emails</li>
<li><strong>Relationship Data:</strong> Relationship to student, custody arrangements</li>
<li><strong>Communication Preferences:</strong> Preferred contact methods and times</li>
<li><strong>Consent Records:</strong> Permissions and authorizations granted</li>
</ul>

<h3>4.3 Staff Data</h3>
<p>Employee and staff information encompasses:</p>
<ul>
<li><strong>Employment Details:</strong> Position, department, employment dates</li>
<li><strong>Qualifications:</strong> Certifications, degrees, professional development</li>
<li><strong>Performance Data:</strong> Evaluations, disciplinary records</li>
<li><strong>Training Records:</strong> Professional development and compliance training</li>
</ul>

<h3>4.4 User Account Data</h3>
<p>Technical and account data includes:</p>
<ul>
<li><strong>Login Credentials:</strong> Usernames, password hashes, authentication tokens</li>
<li><strong>Access Logs:</strong> Login times, IP addresses, device information</li>
<li><strong>Usage Data:</strong> Feature usage, session data, preferences</li>
<li><strong>Communication Logs:</strong> Messages, notifications, support interactions</li>
</ul>

<h2>5. Data Processing Activities</h2>

<h3>5.1 Lawful Bases for Processing</h3>
<p>We process personal data based on:</p>
<ul>
<li><strong>Consent:</strong> Explicit consent from data subjects</li>
<li><strong>Contract:</strong> Necessary for performance of contracts</li>
<li><strong>Legal Obligation:</strong> Required by law or regulation</li>
<li><strong>Vital Interests:</strong> Protection of vital interests</li>
<li><strong>Public Task:</strong> Performance of public tasks</li>
<li><strong>Legitimate Interests:</strong> Pursued by controller or third party</li>
</ul>

<h3>5.2 Data Processing Purposes</h3>
<p>Personal data is processed for:</p>
<ul>
<li><strong>Educational Services:</strong> Delivery of educational programs and services</li>
<li><strong>Administrative Functions:</strong> School operations and management</li>
<li><strong>Communication:</strong> Parent-teacher-student communications</li>
<li><strong>Compliance:</strong> Legal and regulatory compliance</li>
<li><strong>Security:</strong> Platform security and fraud prevention</li>
<li><strong>Improvement:</strong> Service enhancement and quality assurance</li>
</ul>

<h2>6. Data Sharing and Disclosure</h2>

<h3>6.1 Internal Sharing</h3>
<p>Data is shared internally between:</p>
<ul>
<li>Authorized school personnel with legitimate educational interest</li>
<li>Department heads and administrators for operational needs</li>
<li>IT and technical staff for system maintenance and support</li>
<li>Compliance and legal teams for regulatory requirements</li>
</ul>

<h3>6.2 External Sharing</h3>
<p>Data may be shared with external parties when:</p>
<ul>
<li>Required by law or court order</li>
<li>Necessary for student safety or welfare</li>
<li>Authorized by parent/guardian consent</li>
<li>Required for educational partnerships or collaborations</li>
</ul>

<h3>6.3 Third-Party Service Providers</h3>
<p>We engage third-party providers for:</p>
<ul>
<li><strong>Cloud Hosting:</strong> Secure data storage and processing</li>
<li><strong>Payment Processing:</strong> Tuition and fee collection</li>
<li><strong>Communication Services:</strong> Email and messaging platforms</li>
<li><strong>Analytics:</strong> Usage analysis and reporting</li>
</ul>

<h3>6.4 International Data Transfers</h3>
<p>Cross-border data transfers include:</p>
<ul>
<li>Adequacy decisions for approved countries</li>
<li>Standard contractual clauses for protection</li>
<li>Binding corporate rules for multinational organizations</li>
<li>Consent and explicit authorization where required</li>
</ul>

<h2>7. Data Security Measures</h2>

<h3>7.1 Technical Security</h3>
<p>We implement technical safeguards including:</p>
<ul>
<li><strong>Encryption:</strong> Data encrypted at rest and in transit</li>
<li><strong>Access Controls:</strong> Role-based access and multi-factor authentication</li>
<li><strong>Network Security:</strong> Firewalls, intrusion detection, and monitoring</li>
<li><strong>Data Backup:</strong> Regular encrypted backups and disaster recovery</li>
</ul>

<h3>7.2 Organizational Security</h3>
<p>Organizational measures include:</p>
<ul>
<li><strong>Staff Training:</strong> Regular data protection awareness training</li>
<li><strong>Access Management:</strong> Least-privilege access and regular reviews</li>
<li><strong>Incident Response:</strong> Established procedures for security incidents</li>
<li><strong>Vendor Assessment:</strong> Security evaluations of third-party providers</li>
</ul>

<h3>7.3 Physical Security</h3>
<p>Physical protection measures:</p>
<ul>
<li><strong>Secure Facilities:</strong> Controlled access to data centers</li>
<li><strong>Device Security:</strong> Endpoint protection and mobile device management</li>
<li><strong>Document Security:</strong> Secure storage and disposal of physical records</li>
</ul>

<h2>8. Data Breach Procedures</h2>

<h3>8.1 Breach Detection and Assessment</h3>
<p>Upon discovery of a potential breach:</p>
<ul>
<li>Immediate activation of incident response team</li>
<li>Rapid assessment of breach scope and impact</li>
<li>Determination of notification requirements</li>
<li>Implementation of containment measures</li>
</ul>

<h3>8.2 Breach Notification</h3>
<p>Notifications are sent to:</p>
<ul>
<li><strong>Regulatory Authorities:</strong> Within 72 hours of discovery</li>
<li><strong>Affected Individuals:</strong> Without undue delay</li>
<li><strong>Internal Stakeholders:</strong> Immediate notification</li>
<li><strong>Third Parties:</strong> As required by contracts</li>
</ul>

<h3>8.3 Breach Response</h3>
<ul>
<li><strong>Containment:</strong> Immediate steps to contain the breach</li>
<li><strong>Recovery:</strong> Restoration of affected systems and data</li>
<li><strong>Investigation:</strong> Root cause analysis and lessons learned</li>
<li><strong>Prevention:</strong> Implementation of preventive measures</li>
</ul>

<h2>9. Data Retention and Deletion</h2>

<h3>9.1 Retention Schedules</h3>
<p>Data retention periods vary by data type:</p>
<ul>
<li><strong>Student Records:</strong> Retained according to educational regulations</li>
<li><strong>Financial Records:</strong> 7 years for tax and audit purposes</li>
<li><strong>Communication Logs:</strong> 2 years for support and compliance</li>
<li><strong>System Logs:</strong> 1 year for security and troubleshooting</li>
</ul>

<h3>9.2 Data Deletion Procedures</h3>
<ul>
<li><strong>Automated Deletion:</strong> Scheduled deletion of expired data</li>
<li><strong>Manual Review:</strong> Periodic review of retention requirements</li>
<li><strong>Secure Deletion:</strong> Cryptographic erasure and physical destruction</li>
<li><strong>Verification:</strong> Confirmation of complete data removal</li>
</ul>

<h2>10. Cookies and Tracking Technologies</h2>

<h3>10.1 Cookie Usage</h3>
<p>We use cookies and similar technologies for:</p>
<ul>
<li><strong>Essential Functions:</strong> Authentication and security</li>
<li><strong>Analytics:</strong> Usage analysis and performance monitoring</li>
<li><strong>Preferences:</strong> User settings and customization</li>
<li><strong>Marketing:</strong> Targeted communications and advertising</li>
</ul>

<h3>10.2 Cookie Management</h3>
<ul>
<li><strong>Consent:</strong> User consent for non-essential cookies</li>
<li><strong>Control:</strong> Browser settings and preference centers</li>
<li><strong>Transparency:</strong> Clear cookie policies and notices</li>
<li><strong>Minimization:</strong> Limited use of tracking technologies</li>
</ul>

<h2>11. Children's Privacy</h2>

<h3>11.1 Age Restrictions</h3>
<p>Special protections for children under 13:</p>
<ul>
<li><strong>Parental Consent:</strong> Required for data collection from children</li>
<li><strong>Limited Processing:</strong> Only necessary educational data collected</li>
<li><strong>Privacy Notices:</strong> Age-appropriate privacy information</li>
<li><strong>Access Controls:</strong> Additional protections for children's data</li>
</ul>

<h3>11.2 COPPA Compliance</h3>
<ul>
<li><strong>Verifiable Consent:</strong> Parental consent for online data collection</li>
<li><strong>Data Limitations:</strong> Collection limited to educational purposes</li>
<li><strong>Security Measures:</strong> Enhanced security for children's data</li>
<li><strong>Parental Rights:</strong> Parents can review and delete children's data</li>
</ul>

<h2>12. Data Protection Officer</h2>

<h3>12.1 Role and Responsibilities</h3>
<p>Our Data Protection Officer is responsible for:</p>
<ul>
<li><strong>Compliance Oversight:</strong> Ensuring regulatory compliance</li>
<li><strong>Policy Development:</strong> Creating and updating data protection policies</li>
<li><strong>Training:</strong> Conducting privacy awareness training</li>
<li><strong>Audits:</strong> Performing regular compliance assessments</li>
</ul>

<h3>12.2 Contact Information</h3>
<div class="contact-info">
<p>For data protection inquiries, please contact our Data Protection Officer:</p>
<ul>
<li><strong>Email:</strong> dpo@nordalms.pythonanywhere.com</li>
<li><strong>Response Time:</strong> Within 30 days for data requests</li>
<li><strong>Office Hours:</strong> Monday - Friday, 9 AM - 5 PM EST</li>
</ul>
</div>

<h2>13. Data Protection Impact Assessment</h2>

<h3>13.1 DPIA Requirements</h3>
<p>Data Protection Impact Assessments are conducted for:</p>
<ul>
<li>High-risk processing activities</li>
<li>New technology implementations</li>
<li>Large-scale data processing operations</li>
<li>Processing involving sensitive personal data</li>
</ul>

<h3>13.2 DPIA Process</h3>
<ul>
<li><strong>Screening:</strong> Initial assessment of DPIA requirements</li>
<li><strong>Assessment:</strong> Detailed analysis of risks and safeguards</li>
<li><strong>Consultation:</strong> Stakeholder input and expert consultation</li>
<li><strong>Approval:</strong> Senior management review and approval</li>
</ul>

<h2>14. Training and Awareness</h2>

<h3>14.1 Staff Training</h3>
<p>All personnel receive training on:</p>
<ul>
<li><strong>Data Protection Laws:</strong> Legal requirements and obligations</li>
<li><strong>Privacy Practices:</strong> Handling personal data appropriately</li>
<li><strong>Security Procedures:</strong> Protecting data from unauthorized access</li>
<li><strong>Incident Response:</strong> Proper handling of data breaches</li>
</ul>

<h3>14.2 User Education</h3>
<ul>
<li><strong>Privacy Notices:</strong> Clear information about data practices</li>
<li><strong>Consent Processes:</strong> Transparent consent mechanisms</li>
<li><strong>Rights Information:</strong> Education about data subject rights</li>
<li><strong>Best Practices:</strong> Guidance on privacy protection</li>
</ul>

<h2>15. Policy Review and Updates</h2>

<h3>15.1 Regular Review</h3>
<p>This policy is reviewed and updated:</p>
<ul>
<li><strong>Annually:</strong> Comprehensive annual review</li>
<li><strong>Legal Changes:</strong> When laws or regulations change</li>
<li><strong>Process Changes:</strong> When data processing activities change</li>
<li><strong>Incident Response:</strong> Following significant incidents</li>
</ul>

<h3>15.2 Change Notification</h3>
<ul>
<li><strong>Internal Communication:</strong> Staff notification of policy changes</li>
<li><strong>User Notification:</strong> Updates posted on the platform</li>
<li><strong>Version Control:</strong> Clear versioning and change tracking</li>
<li><strong>Training Updates:</strong> Updated training materials as needed</li>
</ul>

<h2>16. Contact Information and Support</h2>

<h3>16.1 Data Protection Support</h3>
<div class="contact-info">
<p>For data protection questions or concerns:</p>
<ul>
<li><strong>General Support:</strong> support@nordalms.pythonanywhere.com</li>
<li><strong>Data Protection:</strong> privacy@nordalms.pythonanywhere.com</li>
<li><strong>Legal Department:</strong> legal@nordalms.pythonanywhere.com</li>
<li><strong>Phone:</strong> +1 (555) 123-4567</li>
</ul>
</div>

<h3>16.2 Data Subject Rights Requests</h3>
<p>To exercise your data protection rights:</p>
<ul>
<li>Visit your account settings</li>
<li>Contact our support team</li>
<li>Use the data request form</li>
<li>Send written requests to our Data Protection Officer</li>
</ul>

<h2>17. Additional Resources</h2>
<ul>
<li><a href="/support/privacy-policy/">Privacy Policy</a></li>
<li><a href="/support/terms-of-service/">Terms of Service</a></li>
<li><a href="/support/cookie-policy/">Cookie Policy</a></li>
<li><a href="/support/accessibility/">Accessibility Statement</a></li>
<li><a href="/support/data-subject-rights/">Data Subject Rights Guide</a></li>
</ul>

<p><em>This Data Protection Policy was last updated on December 17, 2025. Version 2.0</em></p>"""

            # Try to get existing Data Protection Policy
            data_protection_policy = LegalDocument.objects.get(document_type='data_protection')

            # Update the content
            data_protection_policy.content = enhanced_data_protection_content
            data_protection_policy.version = '2.0'
            data_protection_policy.title = 'Data Protection Policy'
            data_protection_policy.save()

            self.log_success(f'Updated Data Protection Policy (ID: {data_protection_policy.id}) - {len(enhanced_data_protection_content)} characters')

        except LegalDocument.DoesNotExist:
            # Create new Data Protection Policy if it doesn't exist
            data_protection_policy = LegalDocument.objects.create(
                title='Data Protection Policy',
                slug='data-protection',
                content=enhanced_data_protection_content,
                document_type='data_protection',
                version='2.0',
                is_active=True,
                requires_acknowledgment=False
            )

            self.log_success(f'Created new Data Protection Policy (ID: {data_protection_policy.id}) - {len(enhanced_data_protection_content)} characters')

        except Exception as e:
            self.log_error(f'Error updating Data Protection Policy: {e}')
            return False

        return True

    def update_terms_of_service(self):
        """Update the Terms of Service with enhanced content."""
        self.log_info("Updating Terms of Service with enhanced content...")

        try:
            from apps.support.models import LegalDocument

            # Enhanced Terms of Service content
            enhanced_terms_content = """<h2>Executive Summary</h2>
<p>Welcome to the Nexus School Management System ("the System"). These Terms of Service ("Terms") govern your access to and use of our comprehensive educational platform. By accessing or using our services, you agree to be bound by these Terms and our Privacy Policy.</p>
<p>Our platform provides a complete solution for educational institutions, including student management, academic tracking, communication tools, and administrative functions. These Terms ensure fair and responsible use of our services.</p>

<h2>1. Acceptance of Terms</h2>

<h3>1.1 Agreement to Terms</h3>
<p>By accessing and using the Nexus School Management System, you accept and agree to be bound by the terms and provision of this agreement. This agreement constitutes a legally binding contract between you and Nexus School Management System.</p>

<h3>1.2 Eligibility Requirements</h3>
<p>To use our services, you must:</p>
<ul>
<li>Be at least 13 years old or have parental consent</li>
<li>Have authority to enter into this agreement</li>
<li>Provide accurate and complete information</li>
<li>Maintain the security of your account credentials</li>
</ul>

<h3>1.3 Institutional Use</h3>
<p>Educational institutions may use our services subject to:</p>
<ul>
<li>Proper licensing and subscription agreements</li>
<li>Compliance with applicable educational regulations</li>
<li>Acceptance of these Terms by authorized representatives</li>
<li>Implementation of appropriate data protection measures</li>
</ul>

<h2>2. Description of Services</h2>

<h3>2.1 Platform Features</h3>
<p>The Nexus School Management System provides comprehensive educational management tools:</p>

<h4>Academic Management</h4>
<ul>
<li><strong>Student Records:</strong> Complete academic profiles and performance tracking</li>
<li><strong>Grade Management:</strong> Automated grading and progress reporting</li>
<li><strong>Curriculum Planning:</strong> Course scheduling and academic planning tools</li>
<li><strong>Assessment Tools:</strong> Quiz creation and evaluation systems</li>
</ul>

<h4>Administrative Functions</h4>
<ul>
<li><strong>User Management:</strong> Role-based access control and user administration</li>
<li><strong>Communication:</strong> Announcements, messaging, and notification systems</li>
<li><strong>Reporting:</strong> Comprehensive analytics and reporting dashboards</li>
<li><strong>Resource Management:</strong> Library, transportation, and facility management</li>
</ul>

<h4>Support Services</h4>
<ul>
<li><strong>Help Center:</strong> Knowledge base and self-service support</li>
<li><strong>Technical Support:</strong> Assistance with platform usage and troubleshooting</li>
<li><strong>Training Resources:</strong> Documentation and training materials</li>
<li><strong>Community Forums:</strong> User-to-user support and knowledge sharing</li>
</ul>

<h3>2.2 Service Availability</h3>
<ul>
<li><strong>Uptime Commitment:</strong> 99.5% uptime excluding scheduled maintenance</li>
<li><strong>Maintenance Windows:</strong> Scheduled maintenance during off-peak hours</li>
<li><strong>Emergency Maintenance:</strong> Unscheduled maintenance with advance notice when possible</li>
<li><strong>Service Updates:</strong> Regular feature updates and security patches</li>
</ul>

<h2>3. User Accounts and Responsibilities</h2>

<h3>3.1 Account Creation and Management</h3>
<p>Users are responsible for:</p>
<ul>
<li>Providing accurate registration information</li>
<li>Maintaining current contact and profile information</li>
<li>Protecting account credentials and access</li>
<li>Notifying us of unauthorized account access</li>
<li>Ensuring proper use by authorized personnel only</li>
</ul>

<h3>3.2 User Conduct and Acceptable Use</h3>

<h4>Permitted Use</h4>
<ul>
<li>Educational and administrative purposes only</li>
<li>Authorized access by licensed users</li>
<li>Compliance with institutional policies</li>
<li>Respect for intellectual property rights</li>
</ul>

<h4>Prohibited Activities</h4>
<ul>
<li>Unauthorized access or use of other accounts</li>
<li>Sharing login credentials with unauthorized users</li>
<li>Attempting to circumvent security measures</li>
<li>Uploading malicious content or code</li>
<li>Violating applicable laws or regulations</li>
<li>Harassing or abusing other users</li>
<li>Impersonating other individuals or institutions</li>
</ul>

<h3>3.3 Data Protection and Privacy</h3>
<p>Users must:</p>
<ul>
<li>Comply with data protection laws (FERPA, GDPR, etc.)</li>
<li>Obtain necessary consents for data collection</li>
<li>Implement appropriate security measures</li>
<li>Report data breaches promptly</li>
<li>Respect student and user privacy rights</li>
</ul>

<h2>4. Intellectual Property Rights</h2>

<h3>4.1 Our Intellectual Property</h3>
<p>The Nexus School Management System and its content are protected by intellectual property laws:</p>
<ul>
<li><strong>Software and Code:</strong> Proprietary software protected by copyright</li>
<li><strong>Trademarks:</strong> Nexus and related marks are our trademarks</li>
<li><strong>Documentation:</strong> User guides and help content are copyrighted</li>
<li><strong>Database Rights:</strong> Data structures and organization are protected</li>
</ul>

<h3>4.2 User Content</h3>
<ul>
<li><strong>Ownership:</strong> Users retain ownership of their content</li>
<li><strong>License Grant:</strong> Users grant us license to use content for service provision</li>
<li><strong>Content Standards:</strong> Content must not violate laws or our policies</li>
<li><strong>Removal Rights:</strong> We may remove inappropriate content</li>
</ul>

<h3>4.3 Educational Content</h3>
<ul>
<li><strong>Fair Use:</strong> Educational use of copyrighted materials under fair use doctrine</li>
<li><strong>Licensing:</strong> Open educational resources and licensed content</li>
<li><strong>Attribution:</strong> Proper attribution of source materials</li>
<li><strong>Copyright Compliance:</strong> Respect for intellectual property in educational materials</li>
</ul>

<h2>5. Fees and Payment Terms</h2>

<h3>5.1 Subscription Fees</h3>
<p>Service fees are based on:</p>
<ul>
<li>Number of users and institutions</li>
<li>Selected feature modules</li>
<li>Service level agreements</li>
<li>Contract duration and terms</li>
</ul>

<h3>5.2 Payment Methods</h3>
<ul>
<li><strong>Accepted Methods:</strong> Credit cards, bank transfers, and approved payment processors</li>
<li><strong>Billing Cycle:</strong> Monthly or annual billing based on subscription plan</li>
<li><strong>Auto-Renewal:</strong> Subscriptions renew automatically unless cancelled</li>
<li><strong>Late Payments:</strong> Service suspension for overdue accounts</li>
</ul>

<h3>5.3 Refunds and Credits</h3>
<ul>
<li><strong>Refund Policy:</strong> Refunds for unused prepaid services within 30 days</li>
<li><strong>Service Credits:</strong> Credits for service outages exceeding agreed levels</li>
<li><strong>Disputes:</strong> Payment disputes handled through our support channels</li>
<li><strong>Tax Compliance:</strong> All fees subject to applicable taxes</li>
</ul>

<h2>6. Service Level Agreements</h2>

<h3>6.1 Performance Standards</h3>
<p>We commit to:</p>
<ul>
<li><strong>System Availability:</strong> 99.5% uptime during business hours</li>
<li><strong>Response Times:</strong> Support response within 24 hours</li>
<li><strong>Data Backup:</strong> Daily backups with disaster recovery</li>
<li><strong>Security:</strong> Industry-standard security measures</li>
</ul>

<h3>6.2 Support Services</h3>
<ul>
<li><strong>Technical Support:</strong> 24/7 monitoring and support</li>
<li><strong>Help Desk:</strong> Multiple support channels and resources</li>
<li><strong>Training:</strong> User training and onboarding support</li>
<li><strong>Updates:</strong> Regular software updates and improvements</li>
</ul>

<h3>6.3 Maintenance and Updates</h3>
<ul>
<li><strong>Scheduled Maintenance:</strong> Announced maintenance windows</li>
<li><strong>Emergency Updates:</strong> Critical security and bug fixes</li>
<li><strong>Feature Releases:</strong> Regular feature updates and enhancements</li>
<li><strong>Compatibility:</strong> Support for current browser and device versions</li>
</ul>

<h2>7. Data Security and Privacy</h2>

<h3>7.1 Security Measures</h3>
<p>We implement comprehensive security:</p>
<ul>
<li><strong>Encryption:</strong> Data encrypted in transit and at rest</li>
<li><strong>Access Controls:</strong> Role-based permissions and authentication</li>
<li><strong>Monitoring:</strong> Continuous security monitoring and alerts</li>
<li><strong>Incident Response:</strong> Established procedures for security incidents</li>
</ul>

<h3>7.2 Data Protection</h3>
<ul>
<li><strong>Compliance:</strong> Adherence to FERPA, GDPR, and other regulations</li>
<li><strong>Data Minimization:</strong> Collection of only necessary data</li>
<li><strong>Retention Policies:</strong> Defined data retention and deletion procedures</li>
<li><strong>Privacy Rights:</strong> Support for user data rights and requests</li>
</ul>

<h3>7.3 Breach Notification</h3>
<ul>
<li><strong>Notification Timeline:</strong> Notification within 72 hours of discovery</li>
<li><strong>Regulatory Compliance:</strong> Compliance with breach notification laws</li>
<li><strong>User Communication:</strong> Clear communication about breach impacts</li>
<li><strong>Remediation:</strong> Steps to mitigate breach effects</li>
</ul>

<h2>8. Termination and Suspension</h2>

<h3>8.1 Termination by User</h3>
<p>Users may terminate their accounts:</p>
<ul>
<li>Through account settings or contacting support</li>
<li>With appropriate notice periods</li>
<li>Following data export procedures</li>
<li>Subject to outstanding payment obligations</li>
</ul>

<h3>8.2 Termination by Us</h3>
<p>We may terminate or suspend services for:</p>
<ul>
<li>Violation of these Terms</li>
<li>Non-payment of fees</li>
<li>Illegal or harmful activities</li>
<li>At the end of subscription periods</li>
</ul>

<h3>8.3 Effect of Termination</h3>
<ul>
<li><strong>Data Export:</strong> Opportunity to export data before termination</li>
<li><strong>Access Removal:</strong> Immediate cessation of service access</li>
<li><strong>Data Retention:</strong> Retention according to legal requirements</li>
<li><strong>Continued Obligations:</strong> Survival of certain provisions</li>
</ul>

<h2>9. Disclaimers and Limitations</h2>

<h3>9.1 Service Disclaimers</h3>
<p>The services are provided "as is" and "as available":</p>
<ul>
<li>No warranties of merchantability or fitness for purpose</li>
<li>No guarantee of uninterrupted or error-free service</li>
<li>No liability for data loss or service interruptions</li>
<li>No warranty of compatibility with all systems</li>
</ul>

<h3>9.2 Limitation of Liability</h3>
<ul>
<li><strong>Direct Damages:</strong> Limited to fees paid in the preceding 12 months</li>
<li><strong>Indirect Damages:</strong> No liability for indirect or consequential damages</li>
<li><strong>Data Loss:</strong> No liability for data loss or corruption</li>
<li><strong>Third-Party Claims:</strong> No liability for third-party actions or claims</li>
</ul>

<h3>9.3 Force Majeure</h3>
<p>We are not liable for failures due to:</p>
<ul>
<li>Natural disasters or acts of God</li>
<li>War, terrorism, or civil unrest</li>
<li>Government actions or regulations</li>
<li>Internet or telecommunications failures</li>
</ul>

<h2>10. Indemnification</h2>

<h3>10.1 User Indemnification</h3>
<p>You agree to indemnify and hold us harmless from:</p>
<ul>
<li>Claims arising from your use of the services</li>
<li>Violation of these Terms or applicable laws</li>
<li>Infringement of third-party intellectual property</li>
<li>Unauthorized access or misuse of your account</li>
</ul>

<h3>10.2 Our Indemnification</h3>
<p>We agree to indemnify you for:</p>
<ul>
<li>Claims of intellectual property infringement by our services</li>
<li>Third-party claims related to our negligence</li>
<li>Breach of data security warranties</li>
</ul>

<h2>11. Dispute Resolution</h2>

<h3>11.1 Informal Resolution</h3>
<p>Disputes should first be resolved through:</p>
<ul>
<li>Contacting our support team</li>
<li>Escalating to account management</li>
<li>Mediation or alternative dispute resolution</li>
</ul>

<h3>11.2 Governing Law</h3>
<ul>
<li><strong>Jurisdiction:</strong> Disputes governed by laws of [Jurisdiction]</li>
<li><strong>Venue:</strong> Exclusive venue in competent courts of [Jurisdiction]</li>
<li><strong>Class Actions:</strong> No class action lawsuits permitted</li>
<li><strong>Arbitration:</strong> Binding arbitration for certain disputes</li>
</ul>

<h3>11.3 Legal Compliance</h3>
<ul>
<li><strong>Export Controls:</strong> Compliance with applicable export laws</li>
<li><strong>Sanctions:</strong> No services to sanctioned individuals or entities</li>
<li><strong>Local Laws:</strong> Compliance with local laws and regulations</li>
</ul>

<h2>12. Changes to Terms</h2>

<h3>12.1 Modifications</h3>
<p>We may modify these Terms:</p>
<ul>
<li>With reasonable notice to users</li>
<li>For legal, regulatory, or operational reasons</li>
<li>To reflect new features or services</li>
<li>To improve clarity or user experience</li>
</ul>

<h3>12.2 User Notification</h3>
<ul>
<li><strong>Email Notification:</strong> Direct email notification of changes</li>
<li><strong>Platform Notice:</strong> Prominent notice on the platform</li>
<li><strong>Review Period:</strong> Reasonable time to review changes</li>
<li><strong>Objection Rights:</strong> Right to terminate if changes unacceptable</li>
</ul>

<h3>12.3 Acceptance of Changes</h3>
<ul>
<li><strong>Continued Use:</strong> Continued use constitutes acceptance</li>
<li><strong>Express Acceptance:</strong> Explicit acceptance through account actions</li>
<li><strong>Version History:</strong> Access to previous versions of Terms</li>
</ul>

<h2>13. Miscellaneous Provisions</h2>

<h3>13.1 Severability</h3>
<p>If any provision is found invalid, the remaining provisions remain in effect.</p>

<h3>13.2 Entire Agreement</h3>
<p>These Terms constitute the entire agreement between parties.</p>

<h3>13.3 Waiver</h3>
<p>Failure to enforce provisions does not constitute waiver of rights.</p>

<h3>13.4 Assignment</h3>
<p>Rights may not be assigned without written consent.</p>

<h3>13.5 Third-Party Beneficiaries</h3>
<p>These Terms do not create rights for third parties.</p>

<h2>14. Contact Information</h2>

<h3>14.1 General Support</h3>
<div class="contact-info">
<p>For questions about these Terms, please contact:</p>
<ul>
<li><strong>Email:</strong> legal@nordalms.pythonanywhere.com</li>
<li><strong>Support:</strong> support@nordalms.pythonanywhere.com</li>
<li><strong>Phone:</strong> +1 (555) 123-4567</li>
<li><strong>Hours:</strong> Monday - Friday, 9 AM - 6 PM EST</li>
</ul>
</div>

<h3>14.2 Legal Department</h3>
<address>
Nexus School Management System<br>
Legal Department<br>
Attn: Terms of Service<br>
[Your Business Address]<br>
[City, State, ZIP Code]<br>
[Country]
</address>

<h2>15. Additional Resources</h2>
<ul>
<li><a href="/support/privacy-policy/">Privacy Policy</a></li>
<li><a href="/support/cookie-policy/">Cookie Policy</a></li>
<li><a href="/support/data-protection/">Data Protection Policy</a></li>
<li><a href="/support/acceptable-use/">Acceptable Use Policy</a></li>
</ul>

<p><em>These Terms of Service were last updated on December 17, 2025. Version 2.0</em></p>"""

            # Try to get existing Terms of Service
            terms_of_service = LegalDocument.objects.get(document_type='terms_of_service')

            # Update the content
            terms_of_service.content = enhanced_terms_content
            terms_of_service.version = '2.0'
            terms_of_service.title = 'Terms of Service'
            terms_of_service.save()

            self.log_success(f'Updated Terms of Service (ID: {terms_of_service.id}) - {len(enhanced_terms_content)} characters')

        except LegalDocument.DoesNotExist:
            # Create new Terms of Service if it doesn't exist
            terms_of_service = LegalDocument.objects.create(
                title='Terms of Service',
                slug='terms-of-service',
                content=enhanced_terms_content,
                document_type='terms_of_service',
                version='2.0',
                is_active=True,
                requires_acknowledgment=True
            )

            self.log_success(f'Created new Terms of Service (ID: {terms_of_service.id}) - {len(enhanced_terms_content)} characters')

        except Exception as e:
            self.log_error(f'Error updating Terms of Service: {e}')
            return False

        return True

    def run_update(self):
        """Run the legal document updates."""
        print("=" * 60)
        print(" LEGAL DOCUMENTS UPDATE ")
        print("=" * 60)
        print()

        try:
            # Update all documents
            terms_success = self.update_terms_of_service()
            privacy_success = self.update_privacy_policy()
            data_success = self.update_data_protection_policy()
            cookie_success = self.update_cookie_policy()
            accessibility_success = self.update_accessibility_statement()

            if terms_success and privacy_success and data_success and cookie_success and accessibility_success:
                print()
                print("=" * 70)
                self.log_success("ALL LEGAL DOCUMENTS UPDATE COMPLETE!")
                print("=" * 70)
                print("\nAll legal documents have been enhanced with:")
                print("✓ Professional HTML formatting")
                print("✓ Comprehensive legal coverage")
                print("✓ Educational institution focus")
                print("✓ Updated to version 2.0")
                print("\nView all enhanced documents at:")
                print("• Terms of Service: http://127.0.0.1:8000/support/terms-of-service/")
                print("• Privacy Policy: http://127.0.0.1:8000/support/privacy-policy/")
                print("• Data Protection: http://127.0.0.1:8000/support/data-protection/")
                print("• Cookie Policy: http://127.0.0.1:8000/support/cookie-policy/")
                print("• Accessibility: http://127.0.0.1:8000/support/accessibility/")
                print("\nOr view all at: http://127.0.0.1:8000/support/legal-documents/")
                return True
            else:
                print()
                self.log_error("UPDATE FAILED!")
                print("Terms of Service:", "✓ Success" if terms_success else "✗ Failed")
                print("Privacy Policy:", "✓ Success" if privacy_success else "✗ Failed")
                print("Data Protection:", "✓ Success" if data_success else "✗ Failed")
                print("Cookie Policy:", "✓ Success" if cookie_success else "✗ Failed")
                print("Accessibility:", "✓ Success" if accessibility_success else "✗ Failed")
                return False

        except Exception as e:
            self.log_error(f'Update failed with error: {e}')
            return False


def main():
    """Main execution function."""
    try:
        updater = LegalDocumentUpdater()

        # Confirm user wants to proceed
        print("This script will update ALL legal documents with enhanced content.")
        print()
        print("Documents to update:")
        print("- Terms of Service")
        print("- Privacy Policy")
        print("- Data Protection Policy")
        print("- Cookie Policy")
        print("- Accessibility Statement")
        print()
        print("Changes:")
        print("- Enhanced HTML formatting")
        print("- Comprehensive legal coverage")
        print("- Educational institution focus")
        print("- Updated to version 2.0")
        print()
        print("WARNING: This will modify all legal documents.")
        print()

        response = input("Do you want to proceed? (y/n): ").strip().lower()
        if response not in ['y', 'yes']:
            print("Update cancelled.")
            return 0

        # Run update
        success = updater.run_update()

        if success:
            print("\n🎉 Terms of Service update completed successfully!")
            return 0
        else:
            print("\n❌ Update failed.")
            return 1

    except KeyboardInterrupt:
        print("\n\nUpdate interrupted by user.")
        return 1
    except Exception as e:
        print(f'\n✗ Update failed with unexpected error: {e}')
        return 1


if __name__ == "__main__":
    sys.exit(main())
