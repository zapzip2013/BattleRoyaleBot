# Code written by Alexander Holmstock

import discord
import asyncio
from battleroyalegame import BattleRoyaleGame
import random


print("Current DiscordPy version: " + discord.__version__)

token = "NTgwODEwNjY4NjM5Mzg3NjU4.XQquxQ.uVKh5YQvDGiSFROAoQTWY7ZA5j0"

client = discord.Client()  # starts the discord client.

channels = []

# when we're logged in, print to console
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.guilds[0].text_channels[0].send('Type \"!help\" for command list and instructions.')

# global variables, all brought in on the initiate option
initiated = False
the_game = BattleRoyaleGame(50)
player_channels = []
main_channel = None

@client.event
async def on_message(message):
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    if message.content.startswith('!'):
        if "help" in message.content.lower():
            await message.channel.send("```Welcome to BattleRoyaleBot! To indicate that your message is to me, start yo"
                                       "ur message with an exclamation point(!)"
                                       "\nEach turn lasts one hour. "
                                       "Last man standing is the winner!\n\nThe following are the bot commands:"
                                       "\n!initiate: initiates search for players"
                                       "\n!addme: lets you join the game once search for players has begun"
                                       "\n!startgame: starts the game"
                                       "\n!players: shows players, their status, and whether they have taken their turn"
                                       "\n!cleanup: tells me to clean up the channels after a game"
                                       "\nWhen a player is added to the game, a private channel only they can access"
                                       " is created. All gameplay commands must be sent to their private channels. The "
                                       "following commands are gameplay commands. An asterisk indicates that this comma"
                                       "nd costs one of your 3 actions per turn. These are actions your character can"
                                       " do, but they do not happen until every player has made their move:"
                                       "\n!equip {item}: equips an item that you own*"
                                       "\n!move {north/east/south/west}: moves your character on the map*"
                                       "\n!search: searches for nearby items and adds them to your inventory*"
                                       "\n!map: shows you the map and your current location on it"
                                       "\n!inventory: shows the items you have in your inventory"
                                       "\n!actions: says how many actions you have left on this turn"
                                       "\n\nMay the odds be ever in your favor!```")
        elif "initiate" in message.content.lower():
            # make sure initiated can't be called twice and it has to be called before all others but help
            global initiated
            if not initiated:
                initiated = True
            global player_channels
            global the_game
            global main_channel
            main_channel = message.channel
            the_game = BattleRoyaleGame(50)
            await message.channel.send("Player search has started. This channel has been set as the main game channel. "
                                       "To join the game type an exclamation point(!)"
                                       " followed by \"addme\"")
        elif "addme" in message.content.lower() and initiated:
            the_game.add_player(message.author.name)
            overwrites = {
                message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                message.author: discord.PermissionOverwrite(read_messages=True)
            }
            player_number_str = str(len(player_channels)+1)
            channel_name = "Player_" + player_number_str
            new_channel = await message.guild.create_text_channel(channel_name, overwrites=overwrites)
            player_channels.append(new_channel)
            await main_channel.send(message.author.name + " has been added to the game as Player " + player_number_str)
        elif "startgame" in message.content.lower() and initiated:
            if not the_game.started:
                await main_channel.send("Let the games begin!")
                the_game.start_game()
                client.loop.create_task(hour_timer())
        elif "players" in message.content.lower() and initiated:
            if len(the_game.players) > 0:
                for x in the_game.players:
                    the_message = x.get_name() + " is "
                    if x.alive:
                        the_message += "alive! They have " + str(x.get_actions()) + " remaining actions this turn"
                    else:
                        the_message += "dead! RIP"
                    await main_channel.send(the_message)
            else:
                await main_channel.send("There are currently no players.")
        elif "done" in message.content.lower() and initiated:
            main_channel.send("Currently considering removing this from the implementation, don't call this for now")
        elif "cleanup" in message.content.lower() and initiated:
            for x in player_channels:
                await x.delete()
        elif "equip" in message.content.lower() and initiated and message.channel != main_channel:
            players_index = player_channels.index(message.channel)
            the_player = the_game.players[players_index]
            if the_player.alive:
                if the_player.actions > 0:
                    for x in message.content.lower().split():
                        if x != '!equip':
                            equipped = the_player.equip(x)
                            if equipped:
                                await message.channel.send(x + " has been equipped.")
                                the_player.actions -= 1
                            else:
                                await message.channel.send("The item " + x + " is not a valid item that you own.")
                            break
                else:
                    await message.channel.send("You have no more remaining actions this turn.")
        elif "move" in message.content.lower() and initiated and message.channel != main_channel:
            players_index = player_channels.index(message.channel)
            the_player = the_game.players[players_index]
            if the_player.alive:
                if the_player.actions > 0:
                    for x in message.content.lower().split():
                        if x != "!move":
                            moved = the_player.move(x)
                            if moved:
                                the_player.actions -= 1
                                await message.channel.send(" Successfully moved to (" + str(the_player.x) + "," + str(the_player.y) + ")")
                            else:
                                await message.channel.send("Either too close to edge of map, or you didn't input a valid direction.")
                else:
                    await message.channel.send("You have no more remaining actions this turn.")
        elif "search" in message.content.lower() and initiated and message.channel != main_channel:
            players_index = player_channels.index(message.channel)
            the_player = the_game.players[players_index]
            if the_player.alive:
                if the_player.actions > 0:
                    rand_int = random.randint(0, 2)
                    if rand_int == 0:  # they find something
                        rand_int = random.randint(0, 5)
                        if rand_int == 0:
                            the_player.find_item('SWORD')
                            await message.channel.send("You found a SWORD!")
                        if rand_int == 1:
                            the_player.find_item('BOW_AND_ARROW')
                            await message.channel.send("You found a BOW_AND_ARROW")
                        if rand_int == 2:
                            the_player.find_item('MAGIC_WAND')
                            await message.channel.send("You found a MAGIC_WAND")
                        if rand_int == 3:
                            the_player.find_item('DAGGER')
                            await message.channel.send("You found a DAGGER")
                        if rand_int == 4:
                            the_player.find_item('CAT')
                            await message.channel.send("You found a CAT")
                        if rand_int == 5:
                            the_player.find_item('RUNNING_SHOES')
                            await message.channel.send("You found RUNNING_SHOES. Equip these to get +1 action per turn")
                    else:  # they find nothing
                        await message.channel.send("You found nothing. :(")
                    the_player.actions -= 1
                else:
                    await message.channel.send("You have no more remaining actions this turn.")
        elif "map" in message.content.lower() and initiated and message.channel != main_channel:
            players_index = player_channels.index(message.channel)
            the_player = the_game.players[players_index]
            if the_player.alive:
                the_game.map.generate_map_image_with_player(the_player.x, the_player.y, the_player.name+".png")
                await message.channel.send(file=discord.File(the_player.name+".png"))
        elif "inventory" in message.content.lower() and initiated and message.channel != main_channel:
            players_index = player_channels.index(message.channel)
            the_player = the_game.players[players_index]
            if the_player.alive:
                if len(the_player.items) == 0:
                    await message.channel.send("You don't currently have any items. Try searching.")
                else:
                    await message.channel.send("You have the following items:")
                    for x in the_player.items:
                        await message.channel.send(x.name)
        elif "actions" in message.content.lower() and initiated and message.channel != main_channel:
            players_index = player_channels.index(message.channel)
            the_player = the_game.players[players_index]
            if the_player.alive:
                await message.channel.send("You have " + str(the_player.actions) + " remaining actions this turn.")
    # if "shogun" in message.content.lower():
    #     if "one" in message.content.lower():
    #         await message.channel.send('Output 1')
    #     elif "two" in message.content.lower():
    #         await message.channel.send('Output 2')
    #     else:
    #         await message.channel.send('First name sho, last name gun.')
    # if "/r" in message.content.lower() or "?roll" in message.content.lower():
    #     global rolls
    #     rolls += 1
    #     roll_message = f"You guys have rolled {rolls} dice today."
    #     await message.channel.send(roll_message)
    # if "picture" in message.content.lower():
    #     await message.channel.send(file=discord.File('test.png'))
    # if "map" in message.content.lower():
    #     map_size = 8
    #     for x in message.content.lower().split():
    #         if x.isdigit():
    #             map_size = int(x)
    #             break
    #     Map(map_size)


async def hour_timer():
    await client.wait_until_ready()
    counter = 0
    while not client.is_closed():
        if counter != 0:
            await main_channel.send("An hour has passed, time for the next round!")
            await tell_game_do_round()
        if len(the_game.living_players) < 2:
            await announce_winner()
            break
        counter += 1
        await asyncio.sleep(3600)


async def tell_game_do_round():
    events = the_game.do_round()
    print(len(events))
    for x in events:
        await main_channel.send(x)


async def announce_winner():
    if len(the_game.living_players) < 1:
        await main_channel.send("Everybody died. There is no winner. Sorry.")
    else:
        await main_channel.send("The triumphant winner of this tournament is " + the_game.get_winner())

client.run(token)
