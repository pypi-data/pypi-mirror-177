import discord, json, os
from discord.ext import commands

description = ""

class cog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	roleplay = discord.SlashCommandGroup("roleplay", "Roleplay cog from roleplaycog.roleplaygrouped")

	@roleplay.command(description="Creates a character")
	async def create(self, ctx: discord.ApplicationContext, image: discord.Option(discord.Attachment, description="Attachment to set as profile picture of your character"), name: discord.Option(str, description="Name of your character"), description: discord.Option(str, description="Description of your character")="No description"):
		if not os.path.exists(f"roleplaydata/characters/{ctx.author.id}"):
			os.makedirs(f"roleplaydata/characters/{ctx.author.id}")
		with open(f"roleplaydata/characters/{ctx.author.id}/{name}.json", "w") as f2:
			data = {
				"name": name, "image": image.url, "description": description
			}
			json.dump(data, f2, indent=4)
		webhook = await ctx.channel.create_webhook(name="CHARACTERHOOK")
		await webhook.send("Hello.", username=name, avatar_url=data['image'])
		await ctx.respond("Done", ephemeral=True)
		await webhook.delete()


	@roleplay.command(description="Sends a message as your character")
	async def send(self, ctx: discord.ApplicationContext, character: discord.Option(str, description="Name of the character"), message: discord.Option(str, description="Message to send as your character")):
		if os.path.exists(f"roleplaydata/characters/{ctx.author.id}/{character}.json"):
			with open(f"roleplaydata/characters/{ctx.author.id}/{character}.json") as f:
				data = json.load(f)
				character = await ctx.channel.create_webhook(name="CHARACTERHOOK")
				await character.send(message, username=data['name'], avatar_url=data['image'])
				await ctx.respond("Sent", ephemeral=True)
				await character.delete()
		else: await ctx.respond("No such character found")

	
	@roleplay.command(description="Deletes a character")
	async def delete(self, ctx: discord.ApplicationContext, character: discord.Option(str, description="Name of the character")):
		try:
			os.remove(f"roleplaydata/characters/{ctx.author.id}/{character}.json")
			await ctx.respond("Done", ephemeral=True)
		except FileNotFoundError:
			await ctx.respond("No such character found")


	@roleplay.command(description="Lists all the characters you have")
	async def characters(self, ctx: discord.ApplicationContext):
		embed = discord.Embed(colour=0x2f3136)
		for dir in os.listdir(f"roleplaydata/characters/{ctx.author.id}"):
			with open(f"roleplaydata/characters/{ctx.author.id}/{dir}") as f:
				data = json.load(f)
				embed.add_field(name=data['name'], value=data['description'])
		await ctx.respond(embed=embed)


	@roleplay.command(description="Shows a character")
	async def show(self, ctx: discord.ApplicationContext, character: discord.Option(str, description="Name of character")):
		with open(f"roleplaydata/characters/{ctx.author.id}/{character}.json") as f:
			data = json.load(f)
			embed = discord.Embed(title=data['name'], colour=0x2f3136, description=data['description'])
			embed.set_thumbnail(url=data['image'])
		await ctx.respond(embed=embed)


	@roleplay.command(description="Edit a character")
	async def edit(self, ctx: discord.ApplicationContext, oldname: discord.Option(str, description="Name of character you want to edit"), newname: discord.Option(str, description="New name for your character")=None, image: discord.Option(discord.Attachment, description="New attachment to set as profile picture of your character")=None, description: discord.Option(str, description="New description for your character")=None):
		with open(f"roleplaydata/characters/{ctx.author.id}/{oldname}.json") as f1:
			data = json.load(f1)
			if newname == None:
				newname = oldname
			if image == None:
				img = data['image']
			else:
				img = image.url
			if description == None:
				desc = data['description']
			else:
				desc = description
			embed = discord.Embed(title=newname, colour=0x2f3136, description=data)
			embed.set_thumbnail(url=image.url)
			data2 = {"name": newname, "description": desc, "image": img}
			os.remove(f"roleplaydata/characters/{ctx.author.id}/{oldname}.json")
			with open(f"roleplaydata/characters/{ctx.author.id}/{newname}.json", "w") as f2:
				json.dump(data2, f2, indent=4)
		await ctx.respond(embed=embed)


def setup(bot):
	bot.add_cog(cog(bot))