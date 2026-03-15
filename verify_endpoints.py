import http.client
import json

def check_endpoint(path):
    try:
        conn = http.client.HTTPConnection("127.0.0.1", 8000, timeout=10)
        conn.request("GET", path)
        res = conn.getresponse()
        data = res.read().decode()
        print(f"Endpoint: {path}")
        print(f"Status: {res.status}")
        print(f"Response: {data}")
        conn.close()
    except Exception as e:
        print(f"Endpoint: {path}")
        print(f"Error: {e}")

check_endpoint("/health")
check_endpoint("/ready")
check_endpoint("/")
