import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
import glob

class EmailReporter:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                      "config", "email_config.json")
        
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
    
    def _format_date(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _get_latest_report(self):
        html_reports = glob.glob(os.path.join(self.reports_dir, "html", "*.html"))
        if html_reports:
            return max(html_reports, key=os.path.getctime)
        return None
    
    def _get_failure_screenshots(self):
        if not self.config.get("attach_screenshots", False):
            return []
        
        screenshots_dir = os.path.join(self.reports_dir, "screenshots")
        if not os.path.exists(screenshots_dir):
            return []
        
        # Get screenshots from the last 24 hours
        recent_screenshots = []
        for screenshot in glob.glob(os.path.join(screenshots_dir, "*.png")):
            if (datetime.now() - datetime.fromtimestamp(os.path.getctime(screenshot))).days < 1:
                recent_screenshots.append(screenshot)
        
        return recent_screenshots
    
    def send_report(self, test_results):
        """
        Send email report with test results
        :param test_results: Dictionary containing test results (passed, failed, skipped)
        """
        if not self.config.get("enabled", False):
            return
        
        if self.config.get("send_on_failure_only", False) and test_results["failed"] == 0:
            return
        
        # Create message
        msg = MIMEMultipart()
        msg["From"] = self.config["sender_email"]
        msg["To"] = ", ".join(self.config["recipients"])
        if self.config.get("cc"):
            msg["Cc"] = ", ".join(self.config["cc"])
        
        # Set subject
        subject = self.config["subject_template"].format(date=self._format_date())
        msg["Subject"] = subject
        
        # Set body
        body = self.config["body_template"].format(**test_results)
        msg.attach(MIMEText(body, "plain"))
        
        # Attach HTML report
        if self.config.get("attach_html_report", False):
            latest_report = self._get_latest_report()
            if latest_report:
                with open(latest_report, "rb") as f:
                    report_attachment = MIMEApplication(f.read(), _subtype="html")
                    report_attachment.add_header("Content-Disposition", "attachment", 
                                               filename=os.path.basename(latest_report))
                    msg.attach(report_attachment)
        
        # Attach screenshots
        for screenshot in self._get_failure_screenshots():
            with open(screenshot, "rb") as f:
                screenshot_attachment = MIMEApplication(f.read(), _subtype="png")
                screenshot_attachment.add_header("Content-Disposition", "attachment", 
                                               filename=os.path.basename(screenshot))
                msg.attach(screenshot_attachment)
        
        # Send email
        try:
            with smtplib.SMTP(self.config["smtp_server"], self.config["smtp_port"]) as server:
                server.starttls()
                server.login(self.config["sender_email"], self.config["sender_password"])
                
                recipients = self.config["recipients"]
                if self.config.get("cc"):
                    recipients.extend(self.config["cc"])
                
                server.sendmail(self.config["sender_email"], recipients, msg.as_string())
                print(f"Email report sent successfully to {', '.join(recipients)}")
        except Exception as e:
            print(f"Failed to send email report: {e}") 