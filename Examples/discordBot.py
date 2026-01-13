import discord
from discord import app_commands
import requests


intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

JINXXY_TOKEN = "your_secret_token" #Replace this with your specific Jinxxy API token
PRODUCT_ID_EXPECTED = 1234567890 #Replace this with your specific Product ID
VERIFIED_ROLE_ID = 1234567890 #Replace this with the role ID you want to be applied when verification is successful

@tree.command(name="verify_jinxxy_short_key", description="Verifies your jinxxy SHORT KEY")
async def verifyJinxxySK(interaction: discord.Interaction, short_license_key: str):
    await interaction.response.defer(ephemeral=True)

    # Checks if they already have the verification role.
    if (interaction.guild.get_role(VERIFIED_ROLE_ID)) in (interaction.user.roles):
        await interaction.followup.send("You are already verified.")
        return

    # Get the unique ID of the license connected to the license key.
    data = requests.get(
        "https://api.creators.jinxxy.com/v1/licenses",
        headers={
        "x-api-key": f"{JINXXY_TOKEN}"
        },
        params={
        "short_key": f"{short_license_key}",
        }
        
    )
    print(data)
  # Checks codes and then returns appropriate courses of action to users the recieve them.
    try:
        if data.status_code == 401:
            await interaction.followup.send(f"{interaction.user.mention}, please contact an admin stating that there was an error ccode 401:1, Thanks!", ephemeral=True)
        elif data.status_code == 403:
            await interaction.followup.send(f"{interaction.user.mention}, please contact an admin stating that there was an error ccode 403:1, Thanks!", ephemeral=True)
        elif data.status_code == 429:
            await interaction.followup.send(f"{interaction.user.mention}, please contact an admin stating that there was an error ccode 429:1, Thanks!", ephemeral=True)
        elif data.status_code == 200:
            #Successful location of license ID
            responseJsonDat = data.json()
            licenseID = responseJsonDat['results'][0]['id']
          # Retrieve data about the license, including which product it is linked to.
            lisenceCheck = requests.get(
                f"https://api.creators.jinxxy.com/v1/licenses/{licenseID}",
                headers={
                "x-api-key": f"{JINXXY_TOKEN}"
                }
            )
            licenseJSON = lisenceCheck.json()
            retreivedProdId = int(licenseJSON['inventory_item']['item']['id'])
            print(retreivedProdId)
          # Admittedly not written in the best way, but it checks error codes and returns how to fix them to the user.
            if lisenceCheck.status_code == 401:
                await interaction.followup.send(f"{interaction.user.mention}, please contact an admin stating that there was an error ccode 401, Thanks!", ephemeral=True)
            elif lisenceCheck.status_code == 403:
                await interaction.followup.send(f"{interaction.user.mention}, please contact an admin stating that there was an error ccode 403, Thanks!", ephemeral=True)
            elif lisenceCheck.status_code == 404:
                await interaction.followup.send(f"{interaction.user.mention}, License key does not exist. Please make sure you are using the correct key", ephemeral=True)
            elif lisenceCheck.status_code == 429:
                await interaction.followup.send(f"{interaction.user.mention}, please contact an admin stating that there was an error ccode 429, Thanks!", ephemeral=True)
            elif lisenceCheck.status_code == 200:
                if retreivedProdId == PRODUCT_ID_EXPECTED:
                    #Successful Verification
                    await interaction.user.add_roles(interaction.guild.get_role(VERIFIED_ROLE_ID), reason="Jinxxy Verification Successful")
                    await interaction.followup.send(f"{interaction.user.mention} You have been successfully verified! You have been given the verified role.", ephemeral=True)
                else:
                    #unsuccessful
                    await interaction.followup.send(f"This license is not for the required product. Please make sure you have the right key.", ephemeral=True)
        else:
            print("Uh oh, something is a-not a-right (spoken in italian accent)")
            await interaction.followup.send(f"Sorry, but an error (Code: 1) has occured, please contact an admin to report this issue.", ephemeral=True) #This specific error code is just to identidy which part of the code is throwing the error. Purely internal.
    except IndexError:
        print("Invalid Key")
        await interaction.followup.send("Invalid Key")
@client.event
async def on_ready():
    await tree.sync()
    print(f'We have logged in as {client.user}')

client.run('Discord Bot Token goes here') 
