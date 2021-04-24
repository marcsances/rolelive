import asyncio
from asyncio import Future

from domain.watchdog.watchdog import Watchdog


class TwitchWatchdog(Watchdog):
    def __init__(self):
        super().__init__()

    async def main(self):
        print("Twitch Watchdog started")
        while True:
            await asyncio.sleep(1000)

    def start(self) -> Future:
        return asyncio.create_task(self.main())
