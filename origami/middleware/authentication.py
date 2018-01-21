"""Authentication module."""

import logging
from typing import List

import falcon
import jwt

LOGGER = logging.getLogger("auth-mw")


class InvalidAuthHeader(Exception):
    """Custom exception raised when the authentication header is invalid."""
    pass


class JwtAuthBackend(object):
    """Class that implements credential verification using JWT tokens."""

    def __init__(self, secret_key, user_loader, auth_header_prefix, issuer, verify_claims):
        """Create a new instance.

        Parameters
        ----------
        secret_key: str
            key to encode and decode JWT tokens

        user_loader: Callable
            function called to verify a user against known credentials stored in
            the database, must return an instance of the user as Dictionary

        auth_header_prefix: str
            prefix of the authentication header

        issuer: str
            str to verify as the issuer of the token

        verify_claims: List[str] or None
            List of jwt claims to verify
        """
        self.secret_key = secret_key
        self.user_loader = user_loader
        self.auth_header_prefix = auth_header_prefix
        self.issuer = issuer
        self.verify_claims = verify_claims
        self.user_key = "email"

    def authenticate(self, token, session):
        """Authenticate a request using the database session inside the resource."""
        try:
            payload = jwt.decode(token, key=self.secret_key,
                                 verify=True, algorithms="HS256")
            user_name = payload[self.user_key]  # type: str

            account_from_db = self.user_loader(user_name, session)
            if not account_from_db:
                raise falcon.HTTPUnauthorized(
                    title="401 Unauthorized",
                    description="User {} does not exist".format(user_name),
                    challenges=None
                )

            account = account_from_db.as_dict
            return account
        except KeyError:
            raise falcon.HTTPBadRequest(
                title="401 Unauthorized",
                description="The JWT token payload\n{}\ndoes not contain the required key {}"
                .format(payload, self.user_key)
            )
        except jwt.exceptions.DecodeError:
            raise falcon.HTTPBadRequest(
                title="401 Unauthorized",
                description="The JWT token is invalid"
            )


class SessionedAuthMiddleware(object):
    """Authentication middleware."""

    def __init__(self, backend, auth_header_prefix: str="Bearer",
                 exempt_routes: List[str]=None, exempt_methods: List[str]=None) -> None:
        """Create a new instance of the middleware.

        Parameters
        ----------
        backend: JwtAuthBackend
            backend used to verify a user against the database

        auth_header_prefix: str
            prefix of the Authorization header

        exempt_routes: List[str]
            list of routes which will not be checked with JWT

        exempt_methods: List[str]
            list of HTTP method names which will not be checked with JWT
        """
        self.backend = backend
        self.auth_header_prefix = auth_header_prefix
        if exempt_routes is not None:
            self.exempt_routes = set(exempt_routes)
        else:
            self.exempt_routes = set([])

        if exempt_methods is not None:
            self.exempt_methods = set(exempt_methods)
        else:
            self.exempt_methods = set(["OPTIONS", "HEAD"])

    def get_auth_token(self, req) -> str:
        """Get the value of the 'Authorization' header from the request."""
        auth_header = req.get_header("Authorization", required=True).split()

        if auth_header[0].lower() != self.auth_header_prefix.lower():
            raise InvalidAuthHeader(("Authentication header starts with {} " +
                                     "but '{}' is required")
                                    .format(auth_header[0], self.auth_header_prefix))

        auth_header_length = len(auth_header)
        if auth_header_length != 2:
            raise InvalidAuthHeader("Header has len={} but 2 is expected"
                                    .format(auth_header_length))
        else:
            return auth_header[1]

    def process_resource(self, req, resp, resource, params):
        """Override the default method to use the resource-local
        session for database access."""
        if (req.path in self.exempt_routes or req.method in self.exempt_methods):
            return

        token = self.get_auth_token(req)
        try:
            session = getattr(resource, "session")
            LOGGER.debug(
                "Successfully got session %(session)s from resource", {"session": session})
            req.context['user'] = self.backend.authenticate(token, session)
        except AttributeError:
            LOGGER.error("Resource %(resource)s does not have a session",
                         {"resource": resource})
            raise AttributeError("Resource does not have a session")
