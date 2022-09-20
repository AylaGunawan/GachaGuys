"""GachaGuy Class."""


from random import randrange

from Guy import Guy

ERROR_TRAIN = "Invalid match-up... :("


class GachaGuy(Guy):
    """Represent a Guy object."""
    head_symbols = ['   ( )   ', "    @    ", "   [ ]   ", "   / \   ", "   | |   ", "    o    ", "   { }   "]
    body_symbols = ["   -|-   ", "  --|--  ", "   ~|~   ", "   /|\   ", "   -V-   ", "   _|_   ", "   <|>   "]
    feet_symbols = ["   / \   ", "   ( )   ", "   L L   ", "  _/ \_  ", "   | |   ", "    ^    ", "   < >   "]

    def __init__(self, adj="", nickname="Guy", is_alive=True, rarity=1, level=1,
                 xp=0, max_xp=0, attack=0, hp=0, max_hp=0):
        """Initialise a GachaGuy instance."""
        super().__init__(adj, nickname, is_alive, level, rarity, xp, max_xp, attack, hp, max_hp)

        for i in range(self.level):  # TODO resets guy when it loads from file
            self.attack += self.randomise_modifier()
            self.max_hp += self.randomise_modifier()
            self.max_xp += self.randomise_modifier()

        self.hp = self.max_hp

        # stick figure gen
        self.head = self.head_symbols[randrange(0, len(self.head_symbols))]  # TODO resets guy when it loads from file
        self.body = self.body_symbols[randrange(0, len(self.body_symbols))]  # TODO what about bad guy symbols? files?
        self.feet = self.feet_symbols[randrange(0, len(self.feet_symbols))]

    def __str__(self):
        """Return a formatted info card of the GachaGuy instance."""
        return f"{self.head} {self.name} {'★' * self.rarity}\n" \
               f"{self.body} lvl{self.level} xp{self.xp}/{self.max_xp}\n" \
               f"{self.feet} atk{self.attack} hp{self.hp}/{self.max_hp}\n"

    def handle_nickname(self, nickname):
        """Handle nicknaming the GachaGuy instance, passing if the nickname input is blank."""
        if nickname != "":
            self.name = self.adj + " " + nickname
            print(f"You nicknamed him {nickname}!\n")
        else:
            print(f"You kept the true name!\n")  # pass

    def handle_train(self, other):
        """Handle training where the GachaGuy instance gains another Guy instance's max xp but deals damage."""
        if self is other:
            print(ERROR_TRAIN)
            pass
        else:
            print(f"{self.name} trained with {other.name}!")
            other.update_hp(self.attack * -1)
            if other.is_alive:
                self.update_xp(other.max_xp)
            elif self.head == other.head and self.body == other.body and self.feet == other.feet:
                self.update_rarity()
