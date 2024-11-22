import aiohttp
import asyncio
import time
from aiohttp import ClientSession, TCPConnector
from tqdm import tqdm  # Importing tqdm for async progress

# Function to perform a single request
async def request(pbar):
    url = 'https://camo.githubusercontent.com/e39573b8a2742cc0187e58716815a29cfbac12a2ddc8c4d7fe0885c8adff083d/68747470733a2f2f6b6f6d617265762e636f6d2f67687076632f3f757365726e616d653d6a75696e6e6c617532266c6162656c3d50726f66696c65253230766965777326636f6c6f723d306537356236267374796c653d666c6174'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }

    retries = 3
    delay = 5  # Retry delay

    for attempt in range(retries):
        try:
            connector = TCPConnector(limit_per_host=50) 
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 503:
                        print("Service Unavailable (503). Waiting 5 seconds before retrying.")
                        await asyncio.sleep(5)  # Wait before retrying
                    else:
                        #print(f"Response status: {resp.status}")
                        pbar.update(1)  # Update progress bar after successful request
                        return  # Exit on successful response
        except aiohttp.ClientError as e:
            print(f"Request failed: {str(e)}")
            if attempt < retries - 1:
                await asyncio.sleep(delay)  # Sleep before retrying
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            if attempt < retries - 1:
                await asyncio.sleep(delay)  # Sleep before retrying

    print("Max retries reached, moving to next request.")

# Function to run multiple requests concurrently
async def run_requests(num_requests):
    tasks = []
    # Create a progress bar using tqdm
    with tqdm(total=num_requests, desc="Sending requests") as pbar:
        for _ in range(num_requests):
            task = request(pbar)  # Pass progress bar to each request
            tasks.append(task)
        await asyncio.gather(*tasks)  # Run all tasks concurrently

if __name__ == "__main__":
    start_time = time.time()
    num_requests = 1000  # Number of requests to run concurrently
    asyncio.run(run_requests(num_requests))
    print(f"Time taken: {time.time() - start_time} seconds")
