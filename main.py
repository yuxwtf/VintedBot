import discord
import discord.ext
from PyVinted import Vinted

Api = Vinted(0)
Api.InitVintedSession()

intents = discord.Intents.all() 
bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

# sync the slash command to your server
@bot.event
async def on_ready():
    await tree.sync()
    print("ready")

@discord.app_commands.describe(search_text = "What would you like to search?", order_type = "How would you like to order the results?", size = "What size would you like to search for?", max_price = "What is the maximum price you would like to search for?", page = "What page would you like to search for?", max_items_per_page = "How many items would you like to search for?")
@tree.command(name="search", description="Search for items using the Vinted API")
async def slash_command(ctx: discord.Interaction, search_text: str, order_type: str ="", size:str="", max_price: int=999, page: int=1, max_items_per_page:int=24):    
    results = Api.search(search_text, order_type, size, max_price, page, max_items_per_page)
    rsent = False

    if len(results['items']) > 0:
        for result in results['items']:
            embed=discord.Embed(title=f"Result(s) For {search_text}")
            
            embed.set_thumbnail(url=result['photo']['url'])
            embed.add_field(name="🔖 Title", value=result['title'], inline=True)
            embed.add_field(name="💰 Price", value=result['price'] + " " + result['currency'], inline=True)
            embed.add_field(name="📏 Size", value=result['size_title'], inline=True)
            embed.add_field(name="🥼 Brand", value=result['brand_title'], inline=True)
            embed.add_field(name="📉 Discount", value=result['discount'] if result['discount'] != None else "❌" , inline=True)

            embed.add_field(name="🔗 Link", value="[Here]("+result['url']+")", inline=True)

            # set requested by to the user who requested the command
            embed.set_footer(text=f"Requested by @{ctx.user.name}#{ctx.user.discriminator}")

            n2c = True
            channel_ = None
            for c in ctx.guild.channels:
                if c.name.lower().replace(' ', '-').replace('.', '').replace('(', '').replace(')', '') == result['brand_title'].lower().replace(' ', '-').replace('.', '').replace('(', '').replace(')', ''):
                    n2c = False
                    channel_ = c
            

            if n2c:
                channel_ = await ctx.guild.create_text_channel(name=result['brand_title'])
                await channel_.send(embed=embed)
            else:
                await channel_.send(embed=embed)

            if not rsent:
                rsent = True
                await ctx.response.send_message(f"Here are the results for your search! --> {channel_.mention}")
    else:
        await ctx.response.send_message(f"No items found for {search_text}!")


bot.run("TOKEN HERE")
