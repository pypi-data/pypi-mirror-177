import discord, json, os
from aiohttp import ClientSession
from discord.ext import commands

description = ""

class cog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		if not os.path.exists("roleplaydata/characters/"):
			os.makedirs("roleplaydata/characters")

	@discord.slash_command(name="create", description="Creates/edits a character")
	async def roleplaycreatechar(self, ctx: discord.ApplicationContext, image: discord.Option(discord.Attachment, description="Attachment to set as profile picture of your character"), name: discord.Option(str, description="Name of your character"), description: discord.Option(str, description="Description of your character")="No description"):
		with open(f"roleplaydata/characters/{ctx.author.id}.json") as fr:
			data = json.load(fr)
			with open(f"roleplaydata/characters/{ctx.author.id}.json", "w") as fw:
				data.update({f"{name}": {
					"name": name, "image": image.url, "description": description
				}})
				json.dump(data, fw, indent=4)
		webhook = await ctx.channel.create_webhook(name=data[f'{name}']['name'])
		await webhook.send("Hello.", avatar_url=data[f'{name}']['image'])
		await ctx.respond("Done", ephemeral=True)
		await webhook.delete()


	@discord.slash_command(name="send", description="Sends a message as your character")
	async def roleplaysendaschar(self, ctx: discord.ApplicationContext, character: discord.Option(str, description="Name of the character"), message: discord.Option(str, description="Message to send as your character")):
		try:
			with open(f"roleplaydata/characters/{ctx.author.id}.json") as f1:
				data = json.load(f1)
				char = await ctx.channel.create_webhook(name=data[f'{character}']['name'])
				await char.send(message, avatar_url=data['image'])
				await ctx.respond("Sent", ephemeral=True)
				await char.delete()
				if os.path.exists(f"roleplaydata/logs.json"):
					with open(f"roleplaydata/logs.json") as f2:
						data2 = json.load(f2)
						async with ClientSession() as session:
							webhook = discord.Webhook.from_url(data2[f'{ctx.guild.id}'], session=session)
							embed = discord.Embed(colour=0x2f3136, title="New roleplay message")
							embed.add_field(name="User", value=str(ctx.author))
							embed.add_field(name="Character", value=character)
							embed.add_field(name="Message", value=message)
							embed.set_thumbnail(url=data['image'])
							await webhook.send(embed=embed)
		except KeyError:
			await ctx.respond("No such character!", ephemeral=True)

	
	@discord.slash_command(name="delete", description="Deletes a character")
	async def roleplaydeletechar(self, ctx: discord.ApplicationContext, character: discord.Option(str, description="Name of the character")):
		try:
			with open(f"roleplaydata/characters/{ctx.author.id}.json") as fr:
				data = json.load(fr)
				with open(f"roleplaydata/characters/{ctx.author.id}.json", "w") as fw:
					data.update({f"{character}": None})
					await ctx.respond("Done")
					json.dump(data, fw, indent=4)
		except FileNotFoundError:
			await ctx.respond("No such character found")


	@discord.slash_command(name="characters", description="Lists all the characters you have")
	async def roleplaydisplaycharacters(self, ctx: discord.ApplicationContext):
		embed = discord.Embed(colour=0x2f3136)
		with open(f"roleplaydata/characters/{ctx.author.id}.json") as f:
			data = json.load(f)
			for item in list(data.keys()):
				try:
					embed.add_field(name=data[f'{item}']['name'], value=data[f'{item}']['description'])
				except:
					continue
		await ctx.respond(embed=embed)


	@discord.slash_command(name="show", description="Shows a character")
	async def roleplayshowcharacter(self, ctx: discord.ApplicationContext, character: discord.Option(str, description="Name of character")):
		with open(f"roleplaydata/characters/{ctx.author.id}.json") as f:
			data = json.load(f)
			embed = discord.Embed(title=data[f'{character}']['name'], colour=0x2f3136, description=data[f'{character}']['description'])
			embed.set_thumbnail(url=data['image'])
		await ctx.respond(embed=embed)


	@discord.slash_command(name="setlogs", description="Set the logging channel for roleplaying")
	@commands.has_guild_permissions(administrator=True)
	async def roleplaysetlogs(self, ctx: discord.ApplicationContext, channel: discord.Option(discord.TextChannel, description="Channel to set logs to")):
		with open(f"roleplaydata/logs.json") as fr:
			data = json.load(fr)
			with open(f"roleplaydata/logs.json", "w") as fw:
				webhook = await channel.create_webhook(name=f"{self.bot.user.name} roleplay logs")
				data.update({
					f"{ctx.guild.id}": webhook.url
				})
				json.dump(data, fw)
		await ctx.respond("Set")


# py -3 -m twine upload --repository pypi dist/* 