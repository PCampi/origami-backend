"""Authentication module."""

import logging

import falcon
from falcon_auth import JWTAuthBackend, FalconAuthMiddleware

LOGGER = logging.getLogger("auth-mw")


class SessionedJWTMiddleware(FalconAuthMiddleware):
    """A JWT authentication middleware with a database session."""

    def _get_auth_settings(self, req, resource):
        auth_settings = getattr(resource, 'auth', {})
        auth_settings['exempt_routes'] = self.exempt_routes
        if auth_settings.get('auth_disabled'):
            auth_settings['exempt_routes'].append(req.path)

        try:
            session = getattr(resource, "session")
            LOGGER.debug(
                "Successfully got session %(session)s from resource", {"session": session})
        except AttributeError:
            LOGGER.error("Resource %(resource)s does not have a session", {
                         "resource": resource})
            raise AttributeError("Resource does not have a session")

        for key in ('exempt_methods', 'backend'):
            auth_settings[key] = auth_settings.get(key) or getattr(self, key)

        return auth_settings

    def process_resource(self, req, resp, resource, *args, **kwargs):
        """Override the default method to use the resource-local
        session for database access."""
        auth_setting = self._get_auth_settings(req, resource)
        if (req.path in auth_setting['exempt_routes'] or
                req.method in auth_setting['exempt_methods']):
            return

        backend = auth_setting['backend']
        req.context['user'] = backend.authenticate(
            req, resp, resource, **kwargs)


class SessionedJWTBackend(JWTAuthBackend):
    """A JWT authentication backend using a database session."""

    def authenticate(self, req, resp, resource):
        """Authenticate a request using the database session."""
        payload = self._decode_jwt_token(req)
        account = self.user_loader(payload, req.session)

        if not account:
            raise falcon.HTTPUnauthorized(
                title="401 Unauthorized",
                description="Invalid JWT token",
                challenges=None
            )

        return account
