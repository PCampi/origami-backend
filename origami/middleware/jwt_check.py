"""Module for autentication JWT."""

from falcon_jwt_checker import JwtChecker


def get_aut_middleware(secret, exempt_routes=["/login"], exempt_methods=["HEAD"],
                       audience="origami.it", expiration_time=30):
    """Create a JWT checker middleware."""

    jwt_checker = JwtChecker(
        secret=secret,  # May be a public key
        algorithm='HS256',
        exempt_routes=exempt_routes,  # Routes listed here will not require a jwt
        exempt_methods=exempt_methods,
        audience=audience,
        leeway=expiration_time
    )

    return jwt_checker
