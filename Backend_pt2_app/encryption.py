from django.contrib.auth.hashers import (
    PBKDF2PasswordHasher, SHA1PasswordHasher,
)
from django.http import HttpResponse


class PBKDF2WrappedSHA1PasswordHasher(PBKDF2PasswordHasher):
    algorithm = 'pbkdf2_wrapped_sha1'

    def encode_sha1_hash(self, sha1_hash, salt, iterations=None):
        return super().encode(sha1_hash, salt, iterations)

    def encode(self, password, salt, iterations=None):
        _, _, sha1_hash = SHA1PasswordHasher().encode(password, salt).split('$', 2)
        return ((self.encode_sha1_hash(sha1_hash, salt, iterations).split('$'))[-1])[:128:]  # remove the string slicing after fixing pswrd


def secure_html_view(page):
    s = ''
    with open(page, "r") as file:
        x = file.readlines()
        for i in x:
            s += i
    response = HttpResponse(s)
    response['strict-transport-security'] = 'max-age=31536000; includeSubDomains'
    return response
