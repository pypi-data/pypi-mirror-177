"""
Created on Nov 13
@author: gsnyder@synopsys.com
"""
 
import requests
from requests.auth import AuthBase
import logging
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class NoAuth(AuthBase):
    def __call__(self, r):
        return r


class BearerAuth(AuthBase):
    """Authenticate with Blackduck hub using access license_key"""

    def __init__(self, session, license_key):
        """
        Args:
            session (requests.session): requests session to authenticate
            license_key (string): for the Black Duck KB system
        """
        if any(arg is False for arg in (session, license_key)):
            raise ValueError(
                'session & license_key are required'
            )

        self.session = session
        self.license_key = license_key
        self.bearer_token = None
        # self.csrf_token = None
        self.valid_until = datetime.now()

    def __call__(self, request):
        if not self.bearer_token or datetime.now() > self.valid_until - timedelta(minutes=5):
            # If bearer token not set or nearing expiry
            self.authenticate()

        request.headers.update({ 
            "Authorization": f"Bearer {self.bearer_token}",
        })
        logger.debug(f"request headers: {request.headers}")
        return request

    def authenticate(self):
        if not self.session.verify:
            requests.packages.urllib3.disable_warnings()
            # Announce this on every auth attempt, as a little incentive to properly configure certs
            logger.warning("ssl verification disabled, connection insecure. do NOT use verify=False in production!")

        response = self.session.post(
            url="/api/authenticate",
            auth=NoAuth(),  # temporarily strip authentication to avoid infinite recursion
            headers={"Authorization": f"bdsLicenseKey {self.license_key}"}
        )

        if response.status_code == 200:
            try:
                content = response.json()
                self.bearer_token = content['jsonWebToken']
                # self.csrf_token = response.headers['X-CSRF-TOKEN']
                self.valid_until = datetime.now() + timedelta(milliseconds=int(content['expiresInMillis']))
                logger.info(f"success: auth granted until {self.valid_until.astimezone()}")
                return
            except (json.JSONDecodeError, KeyError):
                logger.exception("HTTP response status code 200 but unable to obtain bearer token")
                # fall through

        if response.status_code == 401:
            logger.error("HTTP response status code = 401 (Unauthorized)")
            try:
                logger.error(response.json()['errorMessage'])
            except (json.JSONDecodeError, KeyError):
                logger.exception("unable to extract error message")
                logger.error("HTTP response headers: %s", response.headers)
                logger.error("HTTP response text: %s", response.text)
            raise RuntimeError("Unauthorized access token", response)

        # all unhandled responses fall through to here
        logger.error("Unhandled HTTP response")
        logger.error("HTTP response status code %i", response.status_code)
        logger.error("HTTP response headers: %s", response.headers)
        logger.error("HTTP response text: %s", response.text)
        raise RuntimeError("Unhandled HTTP response", response)

