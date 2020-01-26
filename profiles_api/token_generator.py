from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
import string
import secrets

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.password) + six.text_type(user.is_active)
        )

account_activation_token = TokenGenerator()


def generateSecureRandomString(stringLength=10):
    """Generate a secure random string of letters, digits and special characters """
    password_characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(password_characters) for i in range(stringLength))
