from requests import get
from aiohttp import ClientSession
from dataclasses import dataclass
from asyncio import run


# These are the dataclasses for parsing the API results for this specific test

@dataclass
class EntityTotal:
    sent: int
    received: int

@dataclass
class EntityParsedResults:
    entity_totals: dict[str, EntityTotal]
    labels: list[str]
    address: str

    @property
    def incoming_coverage(self) -> float:
        total_received = 0
        total_known_received = 0
        for entity, value in self.entity_totals.items():
            total_received += value.received
            if entity != "Unknown": total_known_received += value.received
        return (total_known_received / total_received) * 100
    
    @property
    def outgoing_coverage(self) -> float:
        total_sent = 0
        total_known_sent = 0
        for entity, value in self.entity_totals.items():
            total_sent += value.sent
            if entity != "Unknown": total_known_sent += value.sent
        return (total_known_sent / total_sent) * 100

    @staticmethod
    def from_api_result(analysis_result: dict) -> "EntityParsedResults":
        """ Receives the result of the address analysis and returns a map of each entity to the total sent and received. """

        address = analysis_result["data"]["address"]
        labels = analysis_result["data"]["labels"]
        incoming_direct = analysis_result["data"]["incomingDirectExposure"]["categories"]
        outgoing_direct = analysis_result["data"]["outgoingDirectExposure"]["categories"]

        entity_totals = {} # Each entry should have total sent and total received in separate keys
        
        for category in incoming_direct:
            for entity in category["entities"]:
                entity_totals.setdefault(entity["name"], {"sent": 0, "received": 0})
                entity_totals[entity["name"]]["received"] = entity["quantity"]
        
        for category in outgoing_direct:
            for entity in category["entities"]:
                entity_totals.setdefault(entity["name"], {"sent": 0, "received": 0})
                entity_totals[entity["name"]]["sent"] = entity["quantity"]

        entity_totals_dataclass = {}
        for entity, value in entity_totals.items():
            entity_totals_dataclass[entity] = EntityTotal(value["sent"], value["received"])
        
        return EntityParsedResults(entity_totals_dataclass, labels, address)

    def __str__(self) -> str:
        labels = ", ".join(self.labels)
        incoming_coverage = f"Incoming Coverage: {round(self.incoming_coverage, 1)}%"
        outgoing_coverage = f"Outgoing Coverage: {round(self.outgoing_coverage, 1)}%"
        
        # Calculate the top 5 entities by sum of sent and received. Add them to the string
        top_entities = sorted(self.entity_totals.items(), key=lambda x: x[1].sent + x[1].received, reverse=True)[:5]
        top_entities_str = ", ".join([f"{entity}: {value.sent + value.received}" for entity, value in top_entities])

        return f"Labels: {labels} | {incoming_coverage} | {outgoing_coverage} | Top Entities: {top_entities_str}"


# Wrapper for fetching API data

async def get_address_analysis(address: str) -> EntityParsedResults:
    url = f"https://wardanalyticsapi.com/addresses/{address}?only_direct=true"
    
    async with ClientSession(timeout=60) as session:
        async with session.get(url) as response:
            if response.status == 200:
                res = await response.json()
                return EntityParsedResults.from_api_result(res)
            else:
                raise Exception(response.text)