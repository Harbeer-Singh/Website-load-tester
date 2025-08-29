import asyncio
import aiohttp
import time

# Worker task: each "user" will run this coroutine
# It sends 'n_requests' HTTP GET requests to the target URL
# and records the status code + response time for each request.
async def worker(session, url, n_requests):
    results = []
    for _ in range(n_requests):
        start = time.perf_counter()  # start timing
        try:
            async with session.get(url) as resp:
                await resp.text()  # read response body (not stored, just ensures completion)
                elapsed = time.perf_counter() - start  # end timing
                results.append((resp.status, elapsed))
        except Exception as e:
            # If any error occurs (connection error, timeout, etc.), mark as failure
            results.append(("error", 0))
    return results


# Main load testing function
# Simulates 'users' concurrent workers, each sending 'requests_per_user' requests
async def load_test(url, users, requests_per_user):
    # Reuse a single session for efficiency
    async with aiohttp.ClientSession() as session:
        # Create one worker task per simulated user
        tasks = [
            worker(session, url, requests_per_user)
            for _ in range(users)
        ]
        # Run all workers concurrently and collect results
        all_results = await asyncio.gather(*tasks)

        # Flatten nested results list into a single list
        flat = [item for sublist in all_results for item in sublist]

        # Calculate stats
        successes = sum(1 for r,_ in flat if r == 200)  # count HTTP 200 OK
        failures = sum(1 for r,_ in flat if r != 200)   # count errors / non-200
        avg_time = sum(t for _,t in flat) / max(1, len(flat))  # average latency

        # Print summary
        print(f"Users: {users}, Requests: {len(flat)}, "
              f"Success: {successes}, Fail: {failures}, "
              f"Avg Response: {avg_time:.3f}s")


# Entry point when running script directly
if __name__ == "__main__":
    # Prompt user for input parameters
    url = input("Enter URL to test (use localhost!): ")
    users = int(input("Enter number of concurrent users: "))
    requests_per_user = int(input("Enter requests per user: "))

    # Run the load test
    asyncio.run(load_test(url, users, requests_per_user))

