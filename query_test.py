import requests
import time
BASE_URL = "http://localhost:8000"
Session_ID="default"
queries = [
    "What is a PI controller?",
    "Explain proportional, integral, and derivative terms",
    "Why does fuzzy control perform better than PI control?"
]

#To Ensure session is cleared before starting the test
requests.post(f"{BASE_URL}/clear/{Session_ID}")
print(f"Session '{Session_ID}' cleared before starting the test.")
for query in queries: 
    print(f"Query: {query}")
    response = requests.post(f"{BASE_URL}/query", json={"query": query, "session_id": Session_ID})
    print(f"Response Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Answer: {data['answer']}\n")
    else:
        print(f"Error: {response.status_code} - {response.text}\n")
    time.sleep(1)  # Optional: Sleep for a second between queries

weak=requests.get(f"{BASE_URL}/weak-topics/{Session_ID}")
print(f"Weak Topics for session '{Session_ID}': {weak.json()}")