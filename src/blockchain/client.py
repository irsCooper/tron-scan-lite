from typing import Optional
from tronpy import AsyncTron

from src.blockchain.schemas import BandwidthSchema, EnergySchema, ResourcesSchema

class TronClient:
    def __init__(self, network: str = "shasta"):
        self.client = AsyncTron(network=network)


    async def get_account(self, address: str) -> Optional[dict]:
        return await self.client.get_account(address)


    async def get_balance(self, address: str) -> Optional[float]:
        return await self.client.get_account_balance(address)


    async def get_resources(self, address: str) -> Optional[ResourcesSchema]:
        resources = await self.client.get_account_resource(address)
        return ResourcesSchema(
            bandwidth=BandwidthSchema(**resources),
            energy=EnergySchema(**resources)
        )
    

tron_client = TronClient(network="shasta")