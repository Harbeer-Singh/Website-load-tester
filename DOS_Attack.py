import asyncio
import aiohttp
import time
import ssl  # <- Import SSL module

# Worker task: each "user" will run this coroutine
# It sends 'n_requests' HTTP GET requests to the target URL
# and records the status code + response time for each request.
async def worker(session, url, n_requests):
    results = []

    # Create SSL context that ignores certificate verification (for testing only)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    for _ in range(n_requests):
        start = time.perf_counter()  # start timing
        try:
            async with session.get(url, ssl=ssl_context) as resp:
                await resp.text()  # read response body
                elapsed = time.perf_counter() - start
                results.append((resp.status, elapsed))
        except Exception as e:
            print(f"Request failed: {e}")
            results.append(("error", 0))
    return results


# Main load testing function
async def load_test(url, users, requests_per_user):
    async with aiohttp.ClientSession() as session:
        tasks = [worker(session, url, requests_per_user) for _ in range(users)]
        all_results = await asyncio.gather(*tasks)

        # Flatten nested results
        flat = [item for sublist in all_results for item in sublist]

        # Calculate stats
        successes = sum(1 for r, _ in flat if r == 200)
        failures = sum(1 for r, _ in flat if r != 200)
        avg_time = sum(t for _, t in flat) / max(1, len(flat))

        print(f"Users: {users}, Requests: {len(flat)}, "
              f"Success: {successes}, Fail: {failures}, "
              f"Avg Response: {avg_time:.3f}s")


# Entry point
if __name__ == "__main__":
    url = input("Enter URL to test (use localhost!): ")
    users = int(input("Enter number of concurrent users: "))
    requests_per_user = int(input("Enter requests per user: "))

    asyncio.run(load_test(url, users, requests_per_user))

