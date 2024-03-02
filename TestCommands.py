@client.command()
async def hello(ctx):
    await ctx.send("Hello! I am ATLAS DUO. I am a bot used for DIDOSDD systems.")
    

@client.command()
async def TestMessage1(ctx):
    await ctx.send("This is a test, only a test. breaking everything begins now.")
    await ctx.send("seeing if this sends multiple messages or if I am misunderstanding this.")
    await ctx.send("Purple and pink.")
    
@client.command()
async def Marco(ctx):
    await ctx.send("POLO!")

@client.command()
async def Random(ctx,arg):
    MyRandom = randrange(10)
    await ctx.send("here is a random number: " + str(MyRandom))
    await ctx.send("You also sent me "+ str(arg))
    if (MyRandom <5):
        await ctx.send("I got less than 5")
    else:
        await ctx.send("greater or equal to 5")

@client.command()
async def Game(ctx):
    MyRandom = randrange(10)
    await ctx.send("I was called by " + str(ctx.author) + ". Test your luck much?")
    if (MyRandom <5):
        await ctx.send("no such luck")
    else:
        await ctx.send("Alright, guess I can do something. maybe.")