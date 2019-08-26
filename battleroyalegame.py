# Code written by Alexander Holmstock
from map import Map
from player import Player
import random
from player import Items


class BattleRoyaleGame(object):

    def __init__(self, map_size):
        self.players = []
        self.players_to_include = []
        self.living_players = []
        self.map = Map(map_size)
        self.map_size = map_size
        self.started = False

    # creates a player object and adds them to the game
    def add_player(self, name):
        # determine player's location on map
        x = random.randint(0, self.map_size-1)
        y = random.randint(0, self.map_size-1)

        # create player
        new_player = Player(x, y, name, self.map_size)

        # add player to players
        self.players.append(new_player)
        self.living_players.append(new_player)

    # sets started to true
    def start_game(self):
        self.started = False

    def get_winner(self):
        if len(self.living_players) == 1:
            return self.living_players[0].name

    # called by main when all players have declared their turns
    # generates all events in the round
    # modifies player lists as necessary
    # returns an array of strings describing each event
    def do_round(self):
        # make return array
        results = []

        # copy living_players to players_to_include
        self.players_to_include = self.living_players.copy()
        for x in self.players_to_include:
            x.reset_actions()

        while True:
            # choose random player from players_to_include
            player_index = random.randint(0, len(self.players_to_include)-1)
            the_player = self.players_to_include[player_index]
            self.players_to_include.pop(player_index)

            # determine if event is solo or multiplayer
            is_multiplayer = False
            if len(self.players_to_include) > 2:
                single_or_multi = random.randint(0, 2)  # 0 is single 1 is multi
                if single_or_multi > 0:
                    is_multiplayer = True

            # generate event and add it to array to be returned
            # there's a lot that can be filled out here. single player events demonstrate the variety that can come from
            # different items, this could be expanded into multiplayer events
            # specifically single player out of river bow_and_array shows that randomness can be introduced even within
            # individual outcomes
            # the multiplayer events show how randomness that isn't a straight up 50 50 coin flip can be introduced
            # further. in a multiplayer event there's a 25 percent chance of each outcome happening( p1 dies, p2 dies,
            # neither die, or both die), but if the attacking player has a weapon, those chances morph to 12.5%, 50%,
            # 25%, and 12.5% respectively, indicative of the fact that attacking with an item equipped gives an
            # advantage
            killed_player = Player(100,100,'DEFAULT',100)
            if is_multiplayer:  # multiplayer event generation
                death_int = random.randint(0, 7)  # the meaning of this roll is decided by player1 location and item
                player_index = random.randint(0, len(self.players_to_include) - 1)
                second_player = self.players_to_include[player_index]
                self.players_to_include.pop(player_index)
                if self.map.map_list[the_player.x][the_player.y] == 4:  # the player is in a river
                    if death_int < 2:  # the player kills second player 25%
                        event = the_player.get_name() + " drowns " + second_player.get_name() + " in the river"
                        killed_player = second_player
                    elif death_int < 4:  # second player reverses the murder attempt 25%
                        event = the_player.get_name() + " is drowned by " + second_player.get_name()
                        killed_player = the_player
                    elif death_int < 6:  # both players die 25%
                        event = the_player.get_name() + " attempts to drown " + second_player.get_name() + " but gets" \
                                                                                                           " pulled i" \
                                                                                                           "n and als" \
                                                                                                           "o drowns"
                        killed_player = the_player
                        self.living_players.remove(second_player)
                        second_player.kill()
                    else:  # neither player dies 25%
                        event = the_player.get_name() + " tries to drown" + second_player.get_name() + " but is unsu" \
                                                                                                       "ccessful"
                        pass
                else:  # the player is not in a river
                    if the_player.equipped != Items.NONE:  # the player is attacking with an item equipped
                        if death_int < 4:  # the first player kills the second player 50%
                            event = the_player.get_name() + " kills " + second_player.get_name() + " with their " \
                                    + the_player.equipped.name
                            killed_player = second_player
                        elif death_int < 6:  # neither player dies 25%
                            event = the_player.get_name() + " shows " + second_player.get_name() + " their " \
                                    + the_player.equipped.name
                            pass
                        elif death_int < 7:  # both players die 12.5%
                            event = the_player.get_name() + " attacks " + second_player.get_name() + " with their " \
                                    + the_player.equipped.name + " but they both end up dying"
                            killed_player = the_player
                            self.living_players.remove(second_player)
                            second_player.kill()
                        else:  # second player reverses the murder attempt 12.5%
                            event = the_player.get_name() + " attacks " + second_player.get_name() + " with their " \
                                    + the_player.equipped.name + " but fails and is killed instead"
                            killed_player = the_player
                    else:
                        if death_int < 2:  # the player kills second player 25%
                            event = the_player.get_name() + " kills " + second_player.get_name()
                            killed_player = second_player
                        elif death_int < 4:  # second player reverses the murder attempt 25%
                            event = the_player.get_name() + " is killed by " + second_player.get_name()
                            killed_player = the_player
                        elif death_int < 6:  # both players die 25%
                            event = the_player.get_name() + " and " + second_player.get_name() + " both die"
                            killed_player = the_player
                            self.living_players.remove(second_player)
                            second_player.kill()
                        else:  # neither player dies 25%
                            event = the_player.get_name() + " tries to kill " + second_player.get_name() + " but fails"
                            pass
            else:  # single player event generation
                death_int = random.randint(0, 1)  # 0 if the player dies, 1 if they live
                if death_int == 0:
                    if self.map.map_list[the_player.x][the_player.y] == 4:  # the player is in a river
                        if the_player.equipped == Items.NONE:  # the player is in a river without an item
                            event = the_player.get_name() + " got eaten by alligators in the river. Wait. Were" \
                                                            "they alligators or crocodiles? Can crocodiles live in " \
                                                            "rivers? Probably not. Who cares. " + the_player.get_name() \
                                                            + " got eaten by SOME semi-aquatic beast in the river"
                            killed_player = the_player
                        else:  # the player is in a river with an item equipped
                            if the_player.equipped == Items.SWORD:
                                event = the_player.get_name() + " had a sword accident and bled out in the river"
                                killed_player = the_player
                            if the_player.equipped == Items.DAGGER:
                                event = the_player.get_name() + " dropped their dagger in the river, went in after it" \
                                                                " and drowned, being surprised by the strength of the" \
                                                                " great river"
                                killed_player = the_player
                            if the_player.equipped == Items.MAGIC_WAND:
                                event = the_player.get_name() + " summoned a bridge to cross the river with their" \
                                                                " magic wand, but the spell failed halfway through, " \
                                                                "causing them to fall in and drown"
                                killed_player = the_player
                            if the_player.equipped == Items.BOW_AND_ARROW:
                                event = the_player.get_name() + " fell in the river and tried to use their bow and " \
                                                                "arrow in an elaborate maneuver to shoot a rope into" \
                                                                " the side of a tree to pull themselves out of the " \
                                                                "river with. They forgot that they didn't have any " \
                                                                "rope. Typical " + the_player.get_name()
                                killed_player = the_player
                            if the_player.equipped == Items.CAT:
                                event = the_player.get_name() + "\'s cat watched them drown in the river with uncaring" \
                                                                " eyes"
                                killed_player = the_player
                            if the_player.equipped == Items.RUNNING_SHOES:
                                event = the_player.get_name() + " was running so fast they didn't see the river, " \
                                                                "fell in it, and drowned"
                                killed_player = the_player
                    else:  # the player is not in the river
                        if the_player.equipped == Items.NONE:  # the player has no item equipped
                            event = the_player.get_name() + " dies of starvation(yell at alex to make more options for" \
                                                            "player death with no items out of the river)"
                            killed_player = the_player
                        else:  # the player has an item equipped
                            if the_player.equipped == Items.SWORD:
                                event = the_player.get_name() + " had a sword accident and cut their head off"
                                killed_player = the_player
                            if the_player.equipped == Items.DAGGER:
                                event = the_player.get_name() + " attacked a squirrel with their dagger, but lost the" \
                                                                " fight. They died...to a squirrel..."
                                killed_player = the_player
                            if the_player.equipped == Items.MAGIC_WAND:
                                event = the_player.get_name() + " accidentally disappears their own heart with their" \
                                                                " magic wand"
                                killed_player = the_player
                            if the_player.equipped == Items.BOW_AND_ARROW:
                                new_rand = random.randint(0, 1)
                                if new_rand == 0:
                                    event = the_player.get_name() + " was practicing with their bow and arrow when a" \
                                                                    " portal opened in the arrow\'s path. The arrow" \
                                                                    " went through the portal, coming out another" \
                                                                    " portal that was perfectly aimed at the player." \
                                                                    " What a cruel fate. I guess Alex wasn't creative" \
                                                                    " enough to come up with a realistic way that so" \
                                                                    "meone could kill themselves with a bow and array" \
                                                                    ". A pity"
                                elif new_rand == 1:
                                    event = the_player.get_name() + " was making sure the bow was lined up properly " \
                                                                    "by looking down the barrel when the bow went off"
                                killed_player = the_player
                            if the_player.equipped == Items.CAT:
                                event = the_player.get_name() + " lost their cat and died of grief"
                                killed_player = the_player
                            if the_player.equipped == Items.RUNNING_SHOES:
                                event = the_player.get_name() + "\'s running accelerated beyond the speed of light. " \
                                                                + the_player.get_name() + " became a find dust."
                                killed_player = the_player
                if death_int == 1:  # the player lives
                    live_rand = random.randint(0, 5)
                    if live_rand == 0:
                        event = the_player.get_name() + " spent all day in a tree doing something dumb"
                    if live_rand == 1:
                        event = the_player.get_name() + " found excalibur but couldn't get it out of the stone"
                    if live_rand == 2:
                        event = the_player.get_name() + " played a game of mahjong with a friendly squirrel"
                    if live_rand == 3:
                        event = the_player.get_name() + " went to the mall in their fever dreams"
                    if live_rand == 4:
                        event = the_player.get_name() + " couldn't remember the lyrics to YMCA"
                    if live_rand == 5:
                        event = the_player.get_name() + " found a fully cooked turkey on a table in the middle of a " \
                                                      "clearing"
                results.append(event)

            # make necessary changes
            if killed_player in self.living_players:
                self.living_players.remove(killed_player)
                killed_player.kill()

            # repeat from second step until players_to_include is empty
            if len(self.players_to_include) == 0:
                break

        return results

    # checks to see if all players have declared all of their turns for the round
    def check_if_ready(self):
        for x in self.living_players:
            if x.get_actions() > 0:
                return False
        return True

    # GETTERS
    def get_started(self):
        return self.started
