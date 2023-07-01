class Player:
    def __init__(self, id, name, health, stamina):
        self.id = id
        self.name = name
        self.health = health
        self.stamina = stamina
        self.last_death_date = None
        self.last_shield_date = None