import os
import requests


os.environ["NEWS_API_KEY"] = "fe0db6edadd74961920820f98a2347ed"  # Add this line temporarily for testing
API_key = os.getenv("NEWS_API_KEY")

print("API Key:", API_key)  # This should now print the key
r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey=fe0db6edadd74961920820f98a2347ed")
print("Response Code:", r.status_code)
print("Response JSON:", r.json())  # Print full response
