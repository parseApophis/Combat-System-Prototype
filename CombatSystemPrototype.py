import random
import CSSP_Spells

value = int(5)
if value > 0:
    print(str(value) + " is greater than 0.")

# The StatBlock defines individual characters and what meters they have.
class StatBlock:
    def __init__(self, name, stamina, maxstam, lust, maxlust, mana, armor, stance, spells):
        self.name       = name
        self.stamina    = stamina
        self.maxstam    = maxstam
        self.lust       = lust
        self.maxlust    = maxlust
        self.mana       = mana
        self.armor      = armor
        self.stance     = stance
        self.spells     = spells

def checkForTag(spells, tag):
    s = None
    for z in spells:
        if z.tag == tag:
            s = z
    return s

# This is the default list of spells. It can be changed and customized per character.
# NOTE: Each spell has a class that defines what it does. Check "CSSP_Spells.py" to see the specific functions.
# NOTE: Each spell can be customized with a different name and cost. The Spell class is just a base for them.
list = [CSSP_Spells.S1("Infirmia", 20), 
        CSSP_Spells.L1("Delusia", 10),
        CSSP_Spells.A1("Delamina", 30),
        CSSP_Spells.E1("Endometria", 25)]

# Set the characters.
# STAM: 100 / 100   | The "health points" of a character
# LUST: 0   / 100   | More lust = less passive mana gain / more passive mana loss with stances.
    # (Possibly add alternative win condition if both parties max out lust?)
# MANA: 200 / INF   | There is no cap to mana as mana can drain quickly.
# ARMOR:    0.05% DMG REDUCTION (ONLY ACTIVE IN "FEND" STANCE)
# STARTING STANCE: FREE (no effect)
# SPELLS: Default list from the above variable.

pc = StatBlock("Player", 100, 100, 0, 100, 200, .05, "FREE", list)
ec = StatBlock("Enemy", 100, 100, 0, 100, 200, .05, "FREE", list)

# A handy method that determines what a character does in their turn.
# If the actor is in FLICK stance, then they gain two actions. isFlick makes sure it's only two times.
# NOTE: If they enter a turn with FLICK stance, they can switch stances on their first action and keep their second action.
def takeAction(actor, target, isFlick):
    # Set variables for use within the whole method.
    x, y, s = None, None, None
    # IF actor is player: Prompt the player on what they can do this turn.
    if actor is pc:
        print("YOUR TURN")
        print("1: CAST")
        print("2: STANCE")
        print("3: WAIT")
        x = str(input())
    
    # IF player chooses CAST: Let a player choose what to CAST
    if (x == "1" or x == "CAST") and actor is pc:
        num = 1
        for z in actor.spells:
            print(str(num) + ": " + z.name + " | " + str(z.cost) + " MANA")
            num +=1
        y = int(input())
        for z in actor.spells:
            if actor.spells[y-1] is z:
                s = z

    # IF player chooses STANCE: Let a player pick their STANCE.
    if (x == "2" or x == "STANCE") and actor is pc:
        print("1: FLOW")    # Increased mana gain. Take more damage.
        print("2: FLICK")   # Act twice. Less efficient magic casting. Huge mana drain per turn.
        print("3: FORCE")   # Increased magic casting. Large mana drain per turn.
        print("4: FEND")    # Reduce incoming damage from Stamina attacks by half. Recover stamina. Slight mana drain per turn.
        print("5: FREE")    # No effect.
        y = str(input())

    # IF actor is enemy npc: Resolve the logic of the AI.
    if actor is ec:
        # If the actor lacks mana,
            # preserve mana with FLOW stance.
        if actor.mana <= 20:
            if actor.stance == "FLOW":
                x = "WAIT"
            else:
                x = "STANCE"
                y = "FLOW"
        # If the target has high ARMOR,
            # target the enemy's ARMOR with ARMOR spells. Otherwise, use FORCE stance if enough mana.
            # Or, use FLOW stance to build up mana.
        if x == None and target.armor > .5:
            s = checkForTag(actor.spells, "armor")
            if s == None and actor.mana > 60:
                x = "STANCE"
                y = "FORCE"
            elif s == None:
                x = "FLOW"
            elif actor.mana > s.cost:
                x = "CAST"
        
        # If the target is in the FEND stance,
            # target the enemy's LUST to break their FEND. Otherwise, use FLOW to gain mana.
        if x == None and target.stance == "FEND":
            s = checkForTag(actor.spells, "lust")
            if s == None:
                if actor.stance == "FLOW":
                    x = "WAIT"
                else:
                    x = "STANCE"
                    y = "FLOW"
            elif actor.mana > s.cost:
                x = "CAST"
        
        # If the target is in the FLOW stance,
            # attack the enemy's STAMINA. Otherwise, use FLOW to gain mana.
            # Also, what the FUCK are you doing without STAMINA spells?
        elif x == None and target.stance == "FLOW":
            s = checkForTag(actor.spells, "stamina")
            if s == None:
                if actor.stance == "FLOW":
                    x = "WAIT"
                else:
                    x = "STANCE"
                    y = "FLOW"
            elif actor.mana > s.cost:
                x = "CAST"

        # If the target is in the FORCE stance,
            # attack the enemy's LUST to end their FORCE earlier and mana-bust them.
            # Or, if their mana is too high, enter FEND stance to reduce incoming damage.
            # Otherwise, go into FREE stance to take less damage compared to FLOW.
        elif x == None and target.stance == "FORCE":
            s = checkForTag(actor.spells, "lust")
            if s == None or (target.mana > 100 and actor.mana > 50):
                if actor.stance == "FEND":
                    x = "WAIT"
                else:
                    x = "STANCE"
                    y = "FEND"
            else:
                if actor.stance == "FREE":
                    x = "WAIT"
                else:
                    x = "STANCE"
                    y = "FREE"
        
        # If the actor has low STAMINA,
            # DO NOT FUCKING DIE.
            # Enter FEND / Increase ARMOR / End FLOW and go to FREE / Mana-bust the enemy with LUST / Enter FLOW if you're mana-busted.
        elif x == None and actor.stamina <= (actor.maxstam / 2):
            s = checkForTag(actor.spells, "effect")
            if actor.stance != "FEND" and actor.mana > 50:
                x = "STANCE"
                y = "FEND"
                s = None
            elif s != None and actor.mana >= s.cost:
                x = "CAST"
            elif actor.stance == "FLOW":
                x = "STANCE"
                y = "FREE"
                s = None
            elif s == None:
                s = checkForTag(actor.spells, "lust")
                if s != None and actor.mana >= s.cost:
                    x = "CAST"
                elif actor.mana <= s.cost and actor.stance != "FLOW":
                    x = "STANCE"
                    y = "FLOW"
        # Perform a basic Stamina spell if no other conditions are met. Otherwise, just go FLOW.
        elif x == None:
            s = checkForTag(actor.spells, "stamina")
            if s != None and actor.mana >= s.cost:
                x = "CAST"
            elif s == None:
                if actor.stance == "FLOW":
                    x = "WAIT"
                else:
                    x = "STANCE"
                    y = "FLOW"

    # Resolve what action was taken by the actor.
    match x:
        # Cast a spell.
        case "1" | "CAST":
            sev = 1
            # Set the SEVERITY of the spell based on the STANCE
            match actor.stance:
                case "FLOW":
                    sev = 0.75
                case "FLICK":
                    sev = 0.40
                case "FORCE":
                    sev = 1.10
                case "FEND":
                    sev = 0.65
                case "FREE":
                    sev = 1
            print(actor.name + " cast " + s.name)
            # If the actor has enough MANA, they CAST. Otherwise, they fail to cast.
            if actor.mana >= s.cost:
                s.cast(actor, target, sev)
                actor.mana -= s.cost
            else:
                print(actor.name + " failed to cast due to lack of mana! [" + s.cost + " > " + actor.mana + "]")
        # Change stance.
        case "2" | "STANCE":
            match y:
                case "1" | "FLOW":
                    actor.stance = "FLOW"
                case "2" | "FLICK":
                    actor.stance = "FLICK"
                case "3" | "FORCE":
                    actor.stance = "FORCE"
                case "4" | "FEND":
                    actor.stance = "FEND"
                case "5" | "FREE":
                    actor.stance = "FREE"
            print(actor.name + " entered " + actor.stance + " stance")
        # Do nothing.
        case "3" | "WAIT":
            print(actor.name + " waited")     

    # Resolve the effects of an actor's STANCE.
    match actor.stance:
        case "FLOW":
            actor.mana += 50 - (0.25 * actor.lust)
        case "FLICK":
            if not isFlick:
                takeAction(actor, target, True)
            actor.mana -= 20 + (0.25 * actor.lust)
        case "FORCE":
            actor.mana -= 10 + (0.25 * actor.lust)
        case "FEND":
            actor.mana -= 15 + (0.25 * actor.lust)
            actor.stamina += 5

    # Cap off meters at their min/max if they overflow.
    if actor.stamina > actor.maxstam:
        actor.stamina = actor.maxstam
    if actor.lust > actor.maxlust:
        actor.lust = actor.maxlust
    if actor.mana <= 0:
        actor.mana = 0
        actor.stance = "FREE"   
    
    return actor, target

# Display all the stats periodically.
def check(): 
    print("============== " + pc.name)
    print("STAM:    " + str(pc.stamina))
    print("LUST:    " + str(pc.lust))
    print("ARMOR:   " + str(pc.armor))
    print("MANA:    " + str(pc.mana))
    print("STANCE:  " + pc.stance)
    print("============== " + ec.name )
    print("STAM:    " + str(ec.stamina))
    print("LUST:    " + str(ec.lust))
    print("ARMOR:   " + str(ec.armor))
    print("MANA:    " + str(ec.mana))
    print("STANCE:  " + ec.stance)

# Turn counter.
turn = 0

# Continue gameplay loop while both parties are alive.
while pc.stamina > 0 and ec.stamina > 0:
    turn += 1   # Increment the Turn counter.
    print("[[=============================== TURN " + str(turn) + " ===============================]]")
    pc, ec = takeAction(pc, ec, False)  # Player's turn.
    ec, pc = takeAction(ec, pc, False)  # Enemy's turn.
    check()                             # Display stats.

# When the gameplay loop is broken, determine the ending message.
if pc.stamina > 0:
    print("YOU WIN")
else:
    print("YOU LOSE")


