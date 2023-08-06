import discord, json, os
from aiohttp import ClientSession
from discord.ext import commands

description = ""

class cog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	roleplay = discord.SlashCommandGroup("roleplay", "Roleplay cog from roleplaycog.roleplaygrouped")

	@roleplay.command(name="create", description="Creates a character")
	async def roleplaycreatechar(self, ctx: discord.ApplicationContext, image: discord.Option(discord.Attachment, description="Attachment to set as profile picture of your character"), name: discord.Option(str, description="Name of your character"), description: discord.Option(str, description="Description of your character")="No description"):
		if not os.path.exists(f"roleplaydata/characters/{ctx.author.id}"):
			os.makedirs(f"roleplaydata/characters/{ctx.author.id}")
		with open(f"roleplaydata/characters/{ctx.author.id}/{name}.json", "w") as f2:
			data = {
				"name": name, "image": image.url, "description": description
			}
			json.dump(data, f2, indent=4)
		webhook = await ctx.channel.create_webhook(name=data['name'])
		await webhook.send("Hello.", avatar_url=data['image'])
		await ctx.respond("Done", ephemeral=True)
		await webhook.delete()


	@roleplay.command(name="send", description="Sends a message as your character")
	async def roleplaysendaschar(self, ctx: discord.ApplicationContext, character: discord.Option(str, description="Name of the character"), message: discord.Option(str, description="Message to send as your character")):
		if os.path.exists(f"roleplaydata/characters/{ctx.author.id}/{character}.json"):
			with open(f"roleplaydata/characters/{ctx.author.id}/{character}.json") as f:
				data = json.load(f)
				character = await ctx.channel.create_webhook(name=data['name'])
				await character.send(message, avatar_url=data['image'])
				await ctx.respond("Sent", ephemeral=True)
				await character.delete()
		else: await ctx.respond("No such character found")
		if os.path.exists(f"roleplaydata/logs/{ctx.guild.id}.json"):
			with open(f"roleplaydata/logs/{ctx.guild.id}.json") as f:
				data2 = json.load(f)
				async with ClientSession() as session:
					webhook = discord.Webhook.from_url(data2['url'], session=session)
					embed = discord.Embed(colour=0x2f3136, title="New roleplay message")
					embed.add_field(name="User", value=str(ctx.author))
					embed.add_field(name="Character", value=character)
					embed.add_field(name="Message", value=message)
					embed.set_thumbnail(url=data['image'])
					await webhook.send(embed=embed)

	
	@roleplay.command(name="delete", description="Deletes a character")
	async def roleplaydeletechar(self, ctx: discord.ApplicationContext, character: discord.Option(str, description="Name of the character")):
		try:
			os.remove(f"roleplaydata/characters/{ctx.author.id}/{character}.json")
			await ctx.respond("Done")
		except FileNotFoundError:
			await ctx.respond("No such character found")


	@roleplay.command(name="characters", description="Lists all the characters you have")
	async def roleplaydisplaycharacters(self, ctx: discord.ApplicationContext):
		embed = discord.Embed(colour=0x2f3136)
		for dir in os.listdir(f"roleplaydata/characters/{ctx.author.id}"):
			with open(f"roleplaydata/characters/{ctx.author.id}/{dir}") as f:
				data = json.load(f)
				embed.add_field(name=data['name'], value=data['description'])
		await ctx.respond(embed=embed)


	@roleplay.command(name="show", description="Shows a character")
	async def roleplayshowcharacter(self, ctx: discord.ApplicationContext, character: discord.Option(str, description="Name of character")):
		with open(f"roleplaydata/characters/{ctx.author.id}/{character}.json") as f:
			data = json.load(f)
			embed = discord.Embed(title=data['name'], colour=0x2f3136, description=data['description'])
			embed.set_thumbnail(url=data['image'])
		await ctx.respond(embed=embed)


	@roleplay.command(name="setlogs", description="Set the logging channel for roleplaying")
	@commands.has_guild_permissions(administrator=True)
	async def roleplaysetlogs(self, ctx: discord.ApplicationContext, channel: discord.Option(discord.TextChannel, description="Channel to set logs to")):
		if not os.path.exists("roleplaydata/logs/"):
			os.makedirs("roleplaydata/logs/")
		with open(f"roleplaydata/logs/{ctx.guild.id}.json", "w") as f:
			webhook = await channel.create_webhook(name=f"{self.bot.user.name} roleplay logs")
			data = {
				"url": webhook.url
			}
			json.dump(data, f)
		await ctx.respond("Set")