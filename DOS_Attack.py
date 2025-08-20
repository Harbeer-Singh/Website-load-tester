import asyncio
import aiohttp
import time

async def worker(session, url, n_requests):
    results = []
    for _ in range(n_requests):
        start = time.perf_counter()
        try:
            async with session.get(url) as resp:
                await resp.text()
                elapsed = time.perf_counter() - start
                results.append((resp.status, elapsed))
        except Exception as e:
            results.append(("error", 0))
    return results

async def load_test(url, users, requests_per_user):
    async with aiohttp.ClientSession() as session:
        tasks = [
            worker(session, url, requests_per_user)
            for _ in range(users)
        ]
        all_results = await asyncio.gather(*tasks)
        flat = [item for sublist in all_results for item in sublist]
        successes = sum(1 for r,_ in flat if r == 200)
        failures = sum(1 for r,_ in flat if r != 200)
        avg_time = sum(t for _,t in flat) / max(1, len(flat))
        print(f"Users: {users}, Requests: {len(flat)}, Success: {successes}, Fail: {failures}, Avg Response: {avg_time:.3f}s")

if __name__ == "__main__":
    url = input("Enter URL to test (use localhost!): ")
    users = int(input("Enter number of concurrent users: "))
    requests_per_user = int(input("Enter requests per user: "))
    asyncio.run(load_test(url, users, requests_per_user))
