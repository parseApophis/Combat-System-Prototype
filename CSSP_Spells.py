class Spell:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

    def cast(self, target):
        print("This spell does nothing!")
        pass

# S / STAMINA
# L / LUST
# A / ARMOR
# E / EFFECT


class S1(Spell):
    # Infirmia
    # Attack the muscles of the target, causing them to lose STAMINA.
    def __init__(self, name, cost):
        super().__init__(name, cost)
        self.tag = "stamina"
    
    def cast(self, actor, target, severity):
        dmg = 0
        if target.stance == "FEND":
            dmg = ((15 * severity) - (15 * target.armor)) * 0.5
        else:
            dmg = 15 * severity
        if dmg < 0:
            dmg = 0
        target.stamina -= dmg
        actor.mana -= self.cost * severity

class L1(Spell):
    # Delusia
    # Throw a dizzying cloud at the target, arousing them and raising their LUST.
    def __init__(self, name, cost):
        super().__init__(name, cost)
        self.tag = "lust"

    def cast(self, actor, target, severity):
        target.lust += 15 * severity
        actor.mana -= self.cost * severity

class A1(Spell):
    # Delamina
    # Attack the fibers of a target's clothes, lowering the target's ARMOR
    def __init__(self, name, cost):
        super().__init__(name, cost)
        self.tag = "armor"
    
    def cast(self, actor, target, severity):
        target.armor -= .05 * severity
        actor.mana -= self.cost * severity

class E1 (Spell):
    # Endometria
    # Thicken the defenses around your body, increasing your ARMOR rating.
    def __init__(self, name, cost):
        super().__init__(name, cost)
        self.tag = "effect"
    
    def cast(self, actor, target, severity):
        actor.armor += .10 * severity
        actor.mana -= self.cost * severity