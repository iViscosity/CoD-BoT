import json
import os
from pathlib import Path


async def save_setting(guild_id, key, value):
    '''Saves a value to a specified key in the current guild.'''

    with open(os.path.join(Path().absolute(), f'settings/guilds/{guild_id}.json')) as f:
        settings = json.load(f)

    with open(os.path.join(Path().absolute(), f'settings/guilds/{guild_id}.json'), 'w+') as f:
        settings[key] = value

        f.seek(0)
        f.truncate()

        json.dump(settings, f)


async def load_setting(guild_id, key):
    '''Finds the value of the key in the guild's settings file.'''

    with open(os.path.join(Path().absolute(), f'settings/guilds/{guild_id}.json'), 'r') as f:
        settings = json.load(f)

        if key in settings:
            return settings[key]
        else:
            print(f'Could not find {key} in {guild_id}.json')
            return None
