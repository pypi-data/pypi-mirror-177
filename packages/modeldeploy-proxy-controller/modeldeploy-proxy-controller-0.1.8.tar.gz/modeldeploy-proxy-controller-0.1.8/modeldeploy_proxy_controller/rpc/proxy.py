import os
import requests
from modeldeploy_proxy_controller.rpc.nb import parse_notebook

API_HOST_URL = os.environ.get("API_HOST_URL", "")
API_VERSION = os.environ.get("API_VERSION", "v1")
PROXY_API_PREFIX = "{}/api/{}/".format(API_HOST_URL, API_VERSION)
TRANSFORMER_UPLOAD_URL = "{}/transformer/upload".format(PROXY_API_PREFIX)
REQUIREMENTS_UPLOAD_URL = "{}/requirements/upload".format(PROXY_API_PREFIX)
STATUS_URL = "{}/proxy/health/status".format(PROXY_API_PREFIX)

PROXY_URL_FILE_NAME = ".proxy"

def revise_proxy_api_url(request, proxy_url):
    request.log.debug("revise_proxy_api_url")

    if not proxy_url:
        raise RuntimeError("Proxy URL should not be empty!")

    global PROXY_API_PREFIX
    global TRANSFORMER_UPLOAD_URL
    global REQUIREMENTS_UPLOAD_URL
    global STATUS_URL

    PROXY_API_PREFIX = "{}/api/{}/".format(proxy_url, API_VERSION)
    TRANSFORMER_UPLOAD_URL = "{}/transformer/upload".format(PROXY_API_PREFIX)
    REQUIREMENTS_UPLOAD_URL = "{}/requirements/upload".format(PROXY_API_PREFIX)
    STATUS_URL = "{}/proxy/health/status".format(PROXY_API_PREFIX)

def apply(request, proxy_url, source_notebook_path):
    request.log.debug("apply nb({}) content to proxy({})...".format(source_notebook_path, proxy_url))

    if proxy_url:
        revise_proxy_api_url(request, proxy_url)

    paths = parse_notebook(request, source_notebook_path)

    if paths.get('requirements_path', None):
        files = {'file': open(paths.get('requirements_path'), 'rb')}
        request.log.debug("POST {} with files...".format(REQUIREMENTS_UPLOAD_URL))
        response = requests.post(REQUIREMENTS_UPLOAD_URL, files = files)
        request.log.debug(response.json())

    if paths.get('transformer_path', None):
        files = {'file': open(paths.get('transformer_path'), 'rb')}
        request.log.debug("POST {} with files...".format(TRANSFORMER_UPLOAD_URL))
        response = requests.post(TRANSFORMER_UPLOAD_URL, files = files)
        request.log.debug(response.json())

def probe(request, proxy_url):
    request.log.debug("probe_proxy")

    if proxy_url:
        revise_proxy_api_url(request, proxy_url)

    response = requests.get(STATUS_URL)
    request.log.debug(str(response))
