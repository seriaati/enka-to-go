import asyncio
import datetime
import logging
import os

import uvicorn

from src.main import app
from update_data import update_data

logger = logging.getLogger(__name__)


async def update_data_daily() -> None:
    while True:
        try:
            await update_data()
        except Exception:
            logger.exception("Failed to update Enka assets")

        now = datetime.datetime.now()
        midnight = datetime.datetime.combine(
            now.date() + datetime.timedelta(days=1), datetime.time.min
        )
        await asyncio.sleep((midnight - now).total_seconds())


async def main() -> None:
    update_task = asyncio.create_task(update_data_daily())

    config = uvicorn.Config(app, host=os.environ.get("HOST", "127.0.0.1"), port=7091)
    server = uvicorn.Server(config)
    await server.serve()

    update_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
