from api_wrapper import EntityParsedResults, get_address_analysis
from asyncio import gather, run
from time import time

# TODO: If you want to change this address list by importing from something like a CSV or a database, you can do so here!
ADDRESS_LIST = []

# TODO: Implement the handle_results function to store in something like a CSV, database, print the results, etc...
# NOTE: This function accepts a list of size BATCH_SIZE of EntityParsedResults objects
async def handle_results(results: list[EntityParsedResults]):
    ...

# We'll be using asyncio to make gather requests conurrently, doing batches of size BATCH_SIZE at a time.
BATCH_SIZE = 100

async def main():
    # This will store the results of the analysis
    total_gathered = 0
    start = time()

    # We'll be making requests in batches of BATCH_SIZE
    for i in range(0, len(ADDRESS_LIST), BATCH_SIZE):
        batch = ADDRESS_LIST[i:i+BATCH_SIZE]
        
        # Fetch and parse API
        newResults = await gather(*[get_address_analysis(address) for address in batch])
        
        # Handle the results (TODO - Implement this function!)
        await handle_results(newResults)    
        
        # Print progress and ETA
        total_gathered += len(newResults)
        currentTime = time()
        print(f"Progress: {total_gathered}/{len(ADDRESS_LIST)} ({round(total_gathered/len(ADDRESS_LIST) * 100, 2)}%)   |   ETA: {round((currentTime - start) / total_gathered * (len(ADDRESS_LIST) - total_gathered), 2)}s")


if __name__ == "__main__":
    run(main())