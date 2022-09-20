"""Guy Class."""


from random import randint

ERROR_TRAIN = "Invalid match-up...\n"


class Guy:
    """Represent a Guy object."""

    def __init__(self, adj="", nickname="Guy", is_alive=True, rarity=1, level=1,
                 xp=0, max_xp=0, attack=0, hp=0, max_hp=0):
        """Initialise a Guy instance."""

        # info
        self.adj = adj
        self.nickname = nickname
        self.name = self.adj + " " + nickname
        self.is_alive = is_alive
        self.level = int(level)
        self.rarity = int(rarity)

        # stats
        self.xp = int(xp)
        self.max_xp = int(max_xp)
        self.attack = int(attack)
        self.hp = int(hp)
        self.max_hp = int(max_hp)

        # modifiers
        self.modifier_lower = 10 ** self.rarity
        self.modifier_upper = 10 ** (self.rarity + 1)

    def __str__(self):
        """Return a formatted string of the Guy instance."""
        return self.enter()

    def enter(self):
        """Return a formatted entry of the Guy instance."""
        return f"{self.adj}, {self.nickname}, {self.is_alive}, {self.level}, {self.rarity}, {self.xp}, {self.max_xp},"\
               f" {self.attack}, {self.hp}, {self.max_hp}"

    def update_xp(self, xp_amount):
        """Update the xp value of the Guy instance; positive or 0 values only."""
        if xp_amount < 0:
            xp_amount = 0
        self.xp += xp_amount
        print(f"{self.name} got {xp_amount} xp!")
        if self.xp >= self.max_xp:
            self.update_level()
            self.xp = 0

    def update_hp(self, hp_amount):
        """Update the hp value of the Guy instance; positive heals while negative damages."""
        self.hp += hp_amount
        if hp_amount <= 0:
            print(f"{self.name}'s hp went down by {hp_amount}!")
        if self.hp <= 0:
            self.is_alive = False
        elif self.hp > self.max_hp:
            self.hp = self.max_hp

    def update_level(self):
        """Update the level of the Guy instance including attack, max hp and max xp."""
        self.level += 1
        print(f"{self.name} levelled up!")
        self.update_attack()
        self.update_max_hp()
        self.update_max_xp()
        self.hp = self.max_hp

    def update_attack(self):
        """Update the attack value of the Guy instance."""
        modifier = self.randomise_modifier()
        self.attack += modifier
        print(f"{self.name}'s attack went up by {modifier}!")

    def update_max_hp(self):
        """Update the max hp value of the Guy instance."""
        modifier = self.randomise_modifier()
        self.max_hp += modifier
        print(f"{self.name}'s max hp went up by {modifier}!")

    def update_max_xp(self):
        """Update the max xp value of the Guy instance."""
        modifier = self.randomise_modifier()
        self.max_xp += modifier

    def update_rarity(self):
        """Update the rarity value of the GachaGuy instance."""
        self.rarity += 1
        self.update_modifier()
        print(f"{self.name}'s guy-ness went up!")

    def update_modifier(self):
        """Update the modifier based on the GachaGuy instance's rarity."""
        self.modifier_lower = 10 ** self.rarity
        self.modifier_upper = 10 ** (self.rarity + 1)

    def randomise_modifier(self):
        """Randomise the modifier based on the Guy instance's rarity."""
        return randint(self.modifier_lower, self.modifier_upper)
