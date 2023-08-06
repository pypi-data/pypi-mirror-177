import discord, random
from importlib import resources

def seal(num: int=None):
	"""
	Returns a `discord.File()` of a seal for py-cord
	"""
	if num == None:
		sealrand = f"{random.randrange(1, 82)}"
	else: 
		if not sealrand > 82:
			sealrand = num
		else:
			sealrand = f"{random.randrange(1, 82)}"
	if len(sealrand) == 1:
		sussy = sealrand
		sealrand = "0" + f"{sussy}"
	with resources.open_text('randseal', f'00{sealrand}.jpg') as fp:
		file = discord.File(fp=fp.name, filename=f"{sealrand}.png")
		return file