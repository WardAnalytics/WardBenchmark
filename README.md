# How to use the project

### Setup

1. Clone the repository
2. Cd into the project directory
3. Run `pip install -r requirements.txt`

### How to run

1. Run `main.py`
2. Should take around an hour for 500k addresses. Go grab a coffee! ☕ Or some boba tea ♨️, that's pretty good too.

### Important Notes

- There is a dataclass class in `api_wrapper.py` named `EntityParsedResults`. This **class represents the result of a single API call to the address analysis** endpoint. You can use this object to easily access the results of the API call without having to go through the documentation!
- in `main.py`, each batch of API calls generates a list of `EntityParsedResults`. An empty function `handle_results(results: list[EntityParsedResults])` is provided so that you can handle actions like saving the results to a dataframe, JSON, or SQL database. The implementation of this function is on you!
- The `test_addresses.csv` is used for our benchmarking. Simply provide a CSV with a single row called `addresses` as input and the script will handle the rest. The `test_addresses.csv` is provided as an example. (ignore the ID row)
- The main function automatically prints progress for you, with a basic ETA. No need to panic!

### Notes about results on a random dataset

- **Label hit rate on random addresses is very low, around 0.04%**. This isnt't great, but the part that matters the most is the coverage on the funds they transact, as well as the quality of the labels we do have (a Binance Deposit Address or a MEV Bot is not as valuable as a Silk Road address, for example.)
- The low address coverage can actually be bad luck with the randomly chosen dataset. We have 63M addresses in the Ethereum network, and only 500k were used for this test.
- **The average coverage for incoming and outgoing funds is over 50**%, so that means that for 50% of the money transacted in Ethereum, we know at least one of the parties involved. This is pretty good! This test isn't covering indirect exposure (multiple hops), but for our internal tests, that can go up to 95% average coverage of all the funds transacted by an address. That's more than enough to inform a risk score!
