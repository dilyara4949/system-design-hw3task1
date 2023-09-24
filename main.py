import time
import requests

class APIClient:
    def __init__(self):
        self.RATE_LIMIT = 6  
        self.last_request_time = 0
        self.cache = {}

    def rate_limit(self):
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.RATE_LIMIT:
            time.sleep(self.RATE_LIMIT - time_since_last_request)

    def make_api_request(self, bin, lang):
        self.rate_limit()
        response = requests.get(f"https://old.stat.gov.kz/api/juridical/counter/api/?bin={bin}&lang={lang}")
        self.last_request_time = time.time()
        return response

    def make_cached_api_request(self, bin, lang):
        if bin in self.cache:
            return self.cache[bin]
        else:
            response = self.make_api_request(bin, lang)
            self.cache[bin] = response
            return response

if __name__ == "__main__":
    api_client = APIClient()




    # Example usage: Make multiple requests with a 6-second interval
    num_requests = 5  # Change this to the number of requests you want to make
    bin = "012345678910"
    lang = "ru"

    for _ in range(num_requests):
        response = api_client.make_cached_api_request(bin, lang)
        print(response.text)
        time.sleep(api_client.RATE_LIMIT)  # Wait for the rate limit period
