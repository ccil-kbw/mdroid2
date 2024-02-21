import os
from typing import Optional

import discord


def _test_guild() -> Optional[discord.Object]:
    test_guild_id = os.getenv("MDROID2_TEST_GUILD_ID", None)
    if test_guild_id:
        print(f"Using test guild: {test_guild_id}")

    return discord.Object(id=test_guild_id) if test_guild_id else None
