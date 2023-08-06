# Roleplay Cog
This package is a cog edition of [my roleplay bot repository](https://github.com/mariohero24/Roleplay-Bot)
## Usage
In your bot's cog directory, make a new file named roleplay and enter:
```py
from roleplaycog.roleplay import cog

def setup(bot):
	bot.add_cog(cog(bot))
```
Or if you want the commands to be in a slash command group named `roleplay`, `from roleplaycog.roleplaygrouped import cog` instead.

In your main bot file (replace `cogs` and `roleplay` with the proper path):
```py
bot.add_extension("cogs.roleplay")
```
From there you are set!