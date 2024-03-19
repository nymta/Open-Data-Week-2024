import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# Local configuration imports for NYS API
try:
    from local_config import (
        am_i_local,
        https,
        http,
        apikey_id,
        apikey_secret,
        apptoken,
        apptoken_secret,
    )
    
    # Apply proxy settings if running locally
    if am_i_local:
        os.environ["https_proxy"] = https
        os.environ["http_proxy"] = http
        os.environ["apikey_id"] = apikey_id
        os.environ["apikey_secret"] = apikey_secret
        os.environ["APPTOKEN"] = apptoken
        os.environ["apptoken_secret"] = apptoken_secret

except ImportError as e:
    print(f"Local configuration not found or error in importing: {e}")



def establish_nys_session(retries: Retry | None | str = 'default', proxy_obj: dict = None) -> requests.Session:
    """
    Establishes a session for the NYS Open Data Portal with optional retries and proxy settings.
    
    Args:
        retries (Retry, None, str): Configuration for request retries. Can be a `Retry` object for detailed config,
                                    'default' for a preconfigured retry strategy, or None to disable retries.
        proxy_obj (dict, optional): Dictionary specifying proxy settings. Keys should be 'http' and 'https'.
    
    Returns:
        requests.Session: A `requests.Session` object configured for API communication.
    
    Example:
        >>> session = establish_nys_session(retries='default', proxy_obj={'http': 'http://proxy.com', 'https': 'https://proxy.com'})
        >>> print(session)
        <requests.sessions.Session object at 0x...>
    """
    session = requests.Session()
    # Ensure the AppToken is used for authentication
    session.headers.update({"X-App-Token": os.environ.get("APPTOKEN", "")})

    # Set retries if specified
    if retries is not None:
        if retries == 'default':
            retries = Retry(total=5, backoff_factor=0.2, status_forcelist=[500, 502, 503, 504])
        session.mount('https://', HTTPAdapter(max_retries=retries))

    # Apply proxy settings if provided
    if proxy_obj:
        session.proxies.update(proxy_obj)

    return session
