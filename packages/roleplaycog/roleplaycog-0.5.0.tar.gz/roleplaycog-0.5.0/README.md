# Roleplay Cog
This package is a cog edition of [my roleplay bot repository](https://github.com/mariohero24/Roleplay-Bot)
## Installation
```cs
pip install roleplaycog
```
## Setup
In your main bot file:
```py
bot.load_extension(".roleplay", package="roleplaycog")
```
Or if you want all the commands to be in a slash command group:
```py
bot.load_extension(".roleplaygrouped", package="roleplaycog")
```