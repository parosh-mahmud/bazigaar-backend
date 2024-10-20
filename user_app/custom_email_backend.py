# custom_email_backend.py

from django.core.mail.backends.smtp import EmailBackend
import ssl

class CustomEmailBackend(EmailBackend):
    def open(self):
        """Ensures an open connection to the email server."""
        if self.connection:
            return False
        try:
            self.connection = self.connection_class(self.host, self.port)
            self.connection.ehlo()
            self.connection.starttls(context=ssl.create_default_context())  # Custom SSL context
            self.connection.ehlo()
            self.connection.login(self.username, self.password)
        except Exception:
            if not self.fail_silently:
                raise
        return True
