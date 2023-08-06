import discord, random
from importlib import resources

def seal():
	"""
	Returns a `discord.File()` of a seal for py-cord
	"""
	sealrand = f"{random.randrange(1, 82)}"
	if len(sealrand) == 1:
		sussy = sealrand
		sealrand = "0" + f"{sussy}"
	with resources.open_text('randseal', f'00{sealrand}.jpg') as fp:
		file = discord.File(fp=fp.name, filename=f"{sealrand}.png")
		return file