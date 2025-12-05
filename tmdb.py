import requests
import time

TMDB_BASE_URL = "https://api.themoviedb.org/3"

count=[0]

def sanitize_input(input_str):
    if not input_str:
        return ""
    return str(input_str).strip()[:100]


def get_trending():
    x=0
    while x<4:
        try:
            return requests.get("https://api.themoviedb.org/3/trending/all/day?api_key="+get_tmdb_api_key()).json()['results']
        except:
            print('.')
            time.sleep(0.5)
            x+=1
    return []

def get_tmdb_api_key(c=count):
    c[0]+=1
    api_key=""

    if c[0]==2:
        c[0]=0
        api_key= "ece985488c982715535011849742081f"
        print('B')
    else:
        api_key = "d3fd780d8f1fa37ae5559e1847055805"
        print('A')

    return api_key

def tmdb_search_movies(query, page=1):
    api_key = get_tmdb_api_key()
    if isinstance(api_key, tuple):
        return api_key[0]

    base_url = "https://api.themoviedb.org/3"
    endpoint = "/search/movie"

    params = {
        "api_key": api_key,
        "query": sanitize_input(query),
        "page": page
    }

    retries=5
    e=""
    for attempt in range(retries):
        try:
            response = requests.get(
                base_url + endpoint,
                params=params,
                headers={"User-Agent": "MovieSearchApp/1.0"}
            )
            response.raise_for_status()

            data = response.json()
            return {
                "results": data.get("results", []),
                "total_pages": data.get("total_pages", 1)
            }
        except Exception as E:
            print(f"[TMDB] Connection error on attempt {attempt+1}/{retries}")
            e=E
            time.sleep(1)  # wait before retry
    
    return {"error": f"Network Error: {str(e)}"}


def tmdb_get(endpoint, params=None, retries=4, delay=0.5, timeout=7):
    """
    Makes a GET request to TMDB with retries and delay.
    """
    api_key = get_tmdb_api_key()

    if params is None:
        params = {}
    params["api_key"] = api_key

    last_exception = None
    for attempt in range(retries):
        try:
            resp = requests.get(f"{TMDB_BASE_URL}{endpoint}", params=params, timeout=timeout,
                                headers={"User-Agent": "MovieSearchApp/1.0"})
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.ConnectionError as e:
            print(f"[TMDB] Connection error on attempt {attempt+1}/{retries}: {e}")
            last_exception = e
            time.sleep(delay)  # wait before retry
        except requests.exceptions.RequestException as e:
            print(f"[TMDB] Request failed: {e}")
            last_exception = e
            break  # do not retry for non-connection errors

    # If all retries fail, raise last exception
    raise last_exception