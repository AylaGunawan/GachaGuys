"""GuyCollection Class."""


class GuyCollection:
    """Represent a GuyCollection object."""

    def __init__(self):
        """Initialise a GuyCollection instance."""

        # the list of guys
        self.guys = []

    def add_guy(self, guy=None):
        """Add a new Guy instance into the GuyCollection instance."""
        self.guys.append(guy)

    def shift_guy_to_front(self, guy=None):
        """Shift a guy to the front of the list of guys."""
        self.guys.remove(guy)
        self.guys.insert(0, guy)

    def handle_death(self):
        """Handle death if a Guy instance is not alive; share his max hp value with the list of guys."""
        hp_amount_total = 0
        for guy in self.guys:
            if not guy.is_alive:
                hp_amount = guy.max_hp // (len(self.guys) - 1)
                hp_amount_total += hp_amount
                print(f"{guy.name} died! Your guys ate him for {hp_amount} hp each.\n")
                self.guys.remove(guy)

        for guy in self.guys:
            if hp_amount_total <= 0:
                print()  # pass
            else:
                guy.update_hp(hp_amount_total)
