import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Set a key-value pair
r.set('mykey', 'Hello, Redis!')

# Retrieve the value
value = r.get('mykey')
print(value.decode('utf-8'))

import redis
import time

# Simulate a slow function
def slow_function():
    time.sleep(2)  # Simulate a 2-second delay
    return "Result from slow function"

# Redis client
r = redis.Redis(host='localhost', port=6379, db=0)

# Check if the result is cached
cached_result = r.get('slow_function_result')
if cached_result:
    print("Retrieved from cache:", cached_result.decode('utf-8'))
else:
    result = slow_function()
    r.set('slow_function_result', result)
    print("Calculated and cached:", result)