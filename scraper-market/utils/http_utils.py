import requests
from requests.exceptions import RequestException
import time

DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
DEFAULT_TIMEOUT = 10  # seconds

def fetch_html(url, headers=None, timeout=DEFAULT_TIMEOUT, retries=3, delay=5):
    """
    Fetches HTML content from a URL with error handling and retries.

    Args:
        url (str): The URL to fetch.
        headers (dict, optional): HTTP headers to send with the request. Defaults to None.
        timeout (int, optional): Request timeout in seconds. Defaults to DEFAULT_TIMEOUT.
        retries (int, optional): Number of retries in case of failure. Defaults to 3.
        delay (int, optional): Delay in seconds between retries. Defaults to 5.

    Returns:
        str: The HTML content of the page, or None if fetching fails after all retries.
    """
    effective_headers = {"User-Agent": DEFAULT_USER_AGENT}
    if headers:
        effective_headers.update(headers)

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=effective_headers, timeout=timeout)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            return response.text
        except RequestException as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                print(f"Failed to fetch {url} after {retries} retries.")
                return None
    return None # Should be unreachable if retries > 0, but as a fallback

if __name__ == '__main__':
    # Example usage:
    test_url_ok = "https://httpstat.us/200"
    test_url_fail = "https://httpstat.us/503" # Service unavailable

    print(f"Fetching {test_url_ok}...")
    html_content_ok = fetch_html(test_url_ok, retries=1)
    if html_content_ok:
        print(f"Successfully fetched {test_url_ok}. Length: {len(html_content_ok)}")
    else:
        print(f"Failed to fetch {test_url_ok}")

    print(f"\nFetching {test_url_fail} (expecting retries and failure)...")
    html_content_fail = fetch_html(test_url_fail, retries=2, delay=2)
    if html_content_fail:
        print(f"Successfully fetched {test_url_fail} (unexpected).")
    else:
        print(f"Failed to fetch {test_url_fail} as expected.")
