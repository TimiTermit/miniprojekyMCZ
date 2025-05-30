
import random
import json
import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_print(text, delay=0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()



class Character:
    def __init__(self, name, max_hp, max_mp, attack, defense, level=1, exp=0):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mp = max_mp
        self.mp = max_mp
        self.attack = attack
        self.defense = defense
        self.level = level
        self.exp = exp
        self.inventory = Inventory()
        self.equipment = Equipment()
        self.status_effects = []

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        damage_taken = max(0, amount - self.defense)
        self.hp = max(0, self.hp - damage_taken)
        return damage_taken

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def use_mp(self, amount):
        if self.mp >= amount:
            self.mp -= amount
            return True
        return False

    def restore_mp(self, amount):
        self.mp = min(self.max_mp, self.mp + amount)

    def gain_exp(self, amount):
        self.exp += amount
        while self.exp >= self.exp_to_next_level():
            self.exp -= self.exp_to_next_level()
            self.level_up()

    def exp_to_next_level(self):
        return 50 + self.level * 20

    def level_up(self):
        self.level += 1
        self.max_hp += 10
        self.hp = self.max_hp
        self.max_mp += 5
        self.mp = self.max_mp
        self.attack += 3
        self.defense += 2
        slow_print(f"\n{self.name} leveled up to level {self.level}!")
        slow_print(f"HP increased to {self.max_hp}, MP to {self.max_mp}, ATK to {self.attack}, DEF to {self.defense}.\n")

class Player(Character):
    def __init__(self, name):
        super().__init__(name, max_hp=100, max_mp=30, attack=10, defense=5)
        self.gold = 100
        self.location = "Town"

    def save(self, filename="savegame.json"):
        data = {
            "name": self.name,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "max_mp": self.max_mp,
            "mp": self.mp,
            "attack": self.attack,
            "defense": self.defense,
            "level": self.level,
            "exp": self.exp,
            "gold": self.gold,
            "location": self.location,
            "inventory": self.inventory.to_list(),
            "equipment": self.equipment.to_dict()
        }
        with open(filename, "w") as f:
            json.dump(data, f)
        slow_print("Game saved successfully!\n", delay=0.01)

    def load(self, filename="savegame.json"):
        if not os.path.exists(filename):
            return False
        with open(filename, "r") as f:
            data = json.load(f)
        self.name = data.get("name", self.name)
        self.max_hp = data.get("max_hp", self.max_hp)
        self.hp = data.get("hp", self.hp)
        self.max_mp = data.get("max_mp", self.max_mp)
        self.mp = data.get("mp", self.mp)
        self.attack = data.get("attack", self.attack)
        self.defense = data.get("defense", self.defense)
        self.level = data.get("level", self.level)
        self.exp = data.get("exp", self.exp)
        self.gold = data.get("gold", self.gold)
        self.location = data.get("location", self.location)
        self.inventory.from_list(data.get("inventory", []))
        self.equipment.from_dict(data.get("equipment", {}))
        slow_print("Game loaded successfully!\n", delay=0.01)
        return True

class Enemy(Character):
    def __init__(self, name, max_hp, max_mp, attack, defense, level=1, exp_reward=10, gold_reward=10):
        super().__init__(name, max_hp, max_mp, attack, defense, level)
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward

    def choose_action(self):
        if self.mp >= 5 and random.random() < 0.3:
            return "skill"
        else:
            return "attack"

# ----- Inventory and Items -----

class Item:
    def __init__(self, name, description, price, effect=None, item_type="consumable", power=0):
        self.name = name
        self.description = description
        self.price = price
        self.effect = effect  
        self.item_type = item_type  
        self.power = power  

    def use(self, user, target=None):
        if self.effect == "heal_hp":
            heal_amount = self.power
            user.heal(heal_amount)
            slow_print(f"{user.name} healed {heal_amount} HP!")
        elif self.effect == "heal_mp":
            restore_amount = self.power
            user.restore_mp(restore_amount)
            slow_print(f"{user.name} restored {restore_amount} MP!")
        elif self.effect == "damage":
            if target:
                damage = self.power
                damage_dealt = target.take_damage(damage)
                slow_print(f"{target.name} took {damage_dealt} damage!")
        

class Inventory:
    def __init__(self):
        self.items = {}  

    def add(self, item, quantity=1):
        self.items[item.name] = self.items.get(item.name, 0) + quantity

    def remove(self, item, quantity=1):
        if item.name in self.items:
            self.items[item.name] -= quantity
            if self.items[item.name] <= 0:
                del self.items[item.name]

    def has(self, item_name, quantity=1):
        return self.items.get(item_name, 0) >= quantity

    def to_list(self):
        return list(self.items.items())

    def from_list(self, items_list):
        self.items = dict(items_list)

    def show(self):
        if not self.items:
            print("Inventory is empty.")
            return
        print("Inventory:")
        for item_name, qty in self.items.items():
            print(f"- {item_name}: {qty}")

class Equipment:
    def __init__(self):
        self.weapon = None
        self.armor = None

    def to_dict(self):
        return {
            "weapon": self.weapon.name if self.weapon else None,
            "armor": self.armor.name if self.armor else None
        }

    def from_dict(self, data):
        if data.get("weapon"):
            self.weapon = ITEM_DATABASE.get(data["weapon"])
        else:
            self.weapon = None
        if data.get("armor"):
            self.armor = ITEM_DATABASE.get(data["armor"])
        else:
            self.armor = None

    def equip(self, player, item):
        if item.item_type == "weapon":
            self.weapon = item
            player.attack = player.attack + item.power
            slow_print(f"{player.name} equipped {item.name}!")
        elif item.item_type == "armor":
            self.armor = item
            player.defense = player.defense + item.power
            slow_print(f"{player.name} equipped {item.name}!")

    def unequip(self, player, item_type):
        if item_type == "weapon" and self.weapon:
            player.attack = player.attack - self.weapon.power
            slow_print(f"{player.name} unequipped {self.weapon.name}!")
            self.weapon = None
        elif item_type == "armor" and self.armor:
            player.defense = player.defense - self.armor.power
            slow_print(f"{player.name} unequipped {self.armor.name}!")
            self.armor = None


ITEM_DATABASE = {
    "Health Potion": Item("Health Potion", "Restores 50 HP", price=25, effect="heal_hp", power=50),
    "Mana Potion": Item("Mana Potion", "Restores 30 MP", price=30, effect="heal_mp", power=30),
    "Iron Sword": Item("Iron Sword", "Basic weapon +5 attack", price=100, item_type="weapon", power=5),
    "Steel Armor": Item("Steel Armor", "Basic armor +5 defense", price=120, item_type="armor", power=5),
    "Fire Scroll": Item("Fire Scroll", "Deals 40 damage to enemy", price=80, effect="damage", power=40),
}



LOCATIONS = {
    "Town": {
        "description": "You are in a peaceful town. You can buy items or travel.",
        "connections": ["Forest", "Dungeon Entrance"],
    },
    "Forest": {
        "description": "A dense forest with wild monsters roaming.",
        "connections": ["Town", "Mountain"],
    },
    "Mountain": {
        "description": "A rocky mountain range, home to fierce beasts.",
        "connections": ["Forest", "Dungeon Entrance"],
    },
    "Dungeon Entrance": {
        "description": "The entrance to a dark and dangerous dungeon.",
        "connections": ["Town", "Mountain", "Dungeon"],
    },
    "Dungeon": {
        "description": "A dark dungeon with powerful monsters and treasures.",
        "connections": ["Dungeon Entrance"],
    },
    "Misty Swamp": {
        "description": "A foggy swamp with hidden dangers beneath the murky waters.",
        "connections": ["Forest", "Haunted Grove"],
    },
    "Crystal Lake": {
        "description": "A beautiful lake known for its reflective waters and lurking water spirits.",
        "connections": ["Town", "Misty Swamp"],
    },
    "Haunted Grove": {
        "description": "A cursed grove, where trees whisper forgotten names.",
        "connections": ["Misty Swamp", "Abandoned Castle"],
    },
    "Wizards Tower": {
        "description": "The tower of a powerful wizard. Few are allowed inside.",
        "connections": ["Town"],
    },
    "Ancient Ruins": {
        "description": "Collapsed stones and relics of a forgotten civilization.",
        "connections": ["Mountain", "Cave"],
    },
    "Frozen Tundra": {
        "description": "A cold, desolate place where only the toughest survive.",
        "connections": ["Dungeon", "Ice Cavern"],
    },
    "Ice Cavern": {
        "description": "Crystalline walls echo with the howls of icy monsters.",
        "connections": ["Frozen Tundra"],
    },
    "Sunken Temple": {
        "description": "A temple partially submerged in water, hiding sacred artifacts.",
        "connections": ["Crystal Lake"],
    },
    "Volcano Core": {
        "description": "The heart of a volcano, where fire elementals roam.",
        "connections": ["Mountain"],
    },
    "Sky Bridge": {
        "description": "A floating bridge of light connecting realms.",
        "connections": ["Wizards Tower", "Sky Citadel"],
    },
    "Sky Citadel": {
        "description": "A city in the clouds, home of the Celestial Order.",
        "connections": ["Sky Bridge"],
    }, 
        "Ashen Ridge": {
        "description": "A mountain pass blackened by ancient volcanic fires.",
        "connections": ["Mountain", "Volcano Core"],
    },
    "Windscar Plateau": {
        "description": "An elevated land swept by fierce, unnatural winds.",
        "connections": ["Ashen Ridge", "Sky Bridge"],
    },
    "Silent Marsh": {
        "description": "A lifeless swamp where even frogs fear to croak.",
        "connections": ["Misty Swamp", "Haunted Grove"],
    },
    "Frostfang Peak": {
        "description": "A peak so cold it freezes breath midair.",
        "connections": ["Frozen Tundra", "Ice Cavern"],
    },
    "Twilight Hollow": {
        "description": "A forest shrouded in permanent dusk.",
        "connections": ["Forest", "Haunted Grove"],
    },
    "Bloodmist Vale": {
        "description": "A valley filled with red mist and screams at night.",
        "connections": ["Dungeon", "Ancient Ruins"],
    },
    "Crimson Dunes": {
        "description": "Desert sands tinged with red, stained by forgotten battles.",
        "connections": ["Sunken Temple", "Crystal Lake"],
    },
    "Shimmering Strand": {
        "description": "A beach where the sand sparkles with ancient magic.",
        "connections": ["Crystal Lake", "Sunken Temple"],
    },
    "Echo Caverns": {
        "description": "Caves that echo not just sound, but memory.",
        "connections": ["Cave", "Ancient Ruins"],
    },
    "Gloomspire": {
        "description": "A towering ruin that pierces the clouds like a dagger.",
        "connections": ["Abandoned Castle", "Dungeon Entrance"],
    },
    "Obsidian Flats": {
        "description": "Vast black plains of cooled lava, still warm to the touch.",
        "connections": ["Volcano Core", "Ashen Ridge"],
    },
    "Moonlit Cliffs": {
        "description": "White cliffs that shine under the moonlight.",
        "connections": ["Sky Bridge", "Crystal Lake"],
    },
    "Gravewatch Hill": {
        "description": "A grassy hill covered in forgotten gravestones.",
        "connections": ["Haunted Grove", "Twilight Hollow"],
    },
    "Wailing Coast": {
        "description": "The waves here howl like the lost souls.",
        "connections": ["Shimmering Strand", "Sunken Temple"],
    },
    "Verdant Wilds": {
        "description": "Overgrown jungle teeming with aggressive flora.",
        "connections": ["Forest", "Twilight Hollow"],
    },
    "Ivory Steps": {
        "description": "A staircase carved from bones leads into the mountain.",
        "connections": ["Gloomspire", "Dungeon"],
    },
    "Blightwoods": {
        "description": "Rotting trees and decayed beasts prowl this cursed forest.",
        "connections": ["Forest", "Twilight Hollow"],
    },
    "Thornreach": {
        "description": "A thicket where brambles whisper warnings.",
        "connections": ["Verdant Wilds", "Blightwoods"],
    },
    "Scorchtrail": {
        "description": "A trail of ash and burn marks left by fire beasts.",
        "connections": ["Volcano Core", "Ashen Ridge"],
    },
    "Spectral Glade": {
        "description": "Phantom deer roam this ghostly clearing.",
        "connections": ["Gravewatch Hill", "Twilight Hollow"],
    },
    "Silvergrove": {
        "description": "An enchanted grove with trees of silver bark.",
        "connections": ["Verdant Wilds", "Wizards Tower"],
    },
    "Sunspire Citadel": {
        "description": "A shining fortress above the clouds.",
        "connections": ["Sky Citadel", "Sky Bridge"],
    },
    "Mirror Depths": {
        "description": "Still waters reflect more than just your face.",
        "connections": ["Sunken Temple", "Crystal Lake"],
    },
    "Rift Canyon": {
        "description": "A deep chasm split by an ancient battle of gods.",
        "connections": ["Dungeon Entrance", "Obsidian Flats"],
    },
    "Celestial Garden": {
        "description": "Floating islands with flowers that sing.",
        "connections": ["Sky Citadel", "Sunspire Citadel"],
    },
    "Mirevault": {
        "description": "An ancient vault buried deep beneath the swamp.",
        "connections": ["Silent Marsh", "Echo Caverns"],
    },
    "Ashvale": {
        "description": "Blackened fields where nothing grows anymore.",
        "connections": ["Ashen Ridge", "Scorchtrail"],
    },
    "Driftwood Shoal": {
        "description": "A beach littered with broken ships and forgotten cargo.",
        "connections": ["Wailing Coast", "Mirror Depths"],
    },
    "Cindershade Keep": {
        "description": "Ruins of a keep destroyed by fire magic.",
        "connections": ["Blightwoods", "Ashvale"],
    },
    "Hollowcore": {
        "description": "A hidden city built into the mountain’s heart.",
        "connections": ["Frostfang Peak", "Ivory Steps"],
    },
    "Blackspire Bluff": {
        "description": "A sheer cliff overlooking eternal darkness below.",
        "connections": ["Gloomspire", "Obsidian Flats"],
    },
    "Thundervale": {
        "description": "Storms constantly roar across this jagged valley.",
        "connections": ["Sky Bridge", "Rift Canyon"],
    },
    "Ebonroot": {
        "description": "An ancient tree at the center of a dead forest.",
        "connections": ["Blightwoods", "Thornreach"],
    },
    "Feycross": {
        "description": "A glade where fae spirits dance and meddle.",
        "connections": ["Silvergrove", "Celestial Garden"],
    },
}



ENEMY_DATABASE = {
    "Slime": Enemy("Slime", max_hp=30, max_mp=10, attack=5, defense=2, level=1, exp_reward=15, gold_reward=10),
    "Goblin": Enemy("Goblin", max_hp=50, max_mp=20, attack=10, defense=5, level=3, exp_reward=30, gold_reward=20),
    "Orc": Enemy("Orc", max_hp=80, max_mp=10, attack=15, defense=8, level=5, exp_reward=50, gold_reward=40),
    "Dragon": Enemy("Dragon", max_hp=200, max_mp=50, attack=25, defense=15, level=10, exp_reward=150, gold_reward=200),
    "Dark Elf": Enemy("Dark Elf", 70, 30, 18, 7, 6, 60, 50),
    "Troll": Enemy("Troll", 120, 10, 20, 10, 7, 80, 70),
    "Wraith": Enemy("Wraith", 60, 50, 22, 6, 6, 90, 60),
    "Fire Elemental": Enemy("Fire Elemental", 90, 40, 25, 8, 8, 100, 85),
    "Ice Golem": Enemy("Ice Golem", 130, 15, 20, 12, 9, 110, 90),
    "Necromancer": Enemy("Necromancer", 80, 70, 30, 5, 10, 120, 100),
    "Ghost Knight": Enemy("Ghost Knight", 95, 20, 18, 15, 9, 100, 95),
    "Bandit Leader": Enemy("Bandit Leader", 110, 25, 22, 12, 8, 95, 80),
    "Vampire": Enemy("Vampire", 100, 60, 26, 10, 10, 130, 120),
    "Cursed Dragon": Enemy("Cursed Dragon", 250, 80, 35, 20, 15, 200, 250),
}




class Combat:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def start(self):
        slow_print(f"\nA wild {self.enemy.name} appears!\n")
        while self.player.is_alive() and self.enemy.is_alive():
            self.player_turn()
            if not self.enemy.is_alive():
                break
            self.enemy_turn()

        if self.player.is_alive():
            slow_print(f"\nYou defeated the {self.enemy.name}!")
            self.player.gain_exp(self.enemy.exp_reward)
            self.player.gold += self.enemy.gold_reward
            slow_print(f"You gained {self.enemy.exp_reward} EXP and {self.enemy.gold_reward} Gold.\n")
            time.sleep(1)
            return True
        else:
            slow_print("\nYou were defeated. Game Over.\n")
            return False

    def player_turn(self):
        slow_print(f"\n{self.player.name}'s turn:")
        slow_print(f"HP: {self.player.hp}/{self.player.max_hp}  MP: {self.player.mp}/{self.player.max_mp}")
        slow_print(f"{self.enemy.name} HP: {self.enemy.hp}/{self.enemy.max_hp}")
        slow_print("Choose action:")
        slow_print("1. Attack")
        slow_print("2. Use Item")
        slow_print("3. Use Skill/Spell")
        slow_print("4. Run")

        choice = input("> ")
        if choice == "1":
            damage = self.player.attack
            damage_dealt = self.enemy.take_damage(damage)
            slow_print(f"You attacked {self.enemy.name} for {damage_dealt} damage.")
        elif choice == "2":
            self.use_item()
        elif choice == "3":
            self.use_skill()
        elif choice == "4":
            chance = random.random()
            if chance > 0.5:
                slow_print("You successfully fled!")
                self.enemy.hp = 0  
            else:
                slow_print("Failed to flee!")
        else:
            slow_print("Invalid input, you lose your turn!")

    def use_item(self):
        inv = self.player.inventory
        if not inv.items:
            slow_print("You have no items to use.")
            return
        slow_print("Your Inventory:")
        inventory_list = list(inv.items.items())
        for i, (item_name, qty) in enumerate(inventory_list, start=1):
            slow_print(f"{i}. {item_name} x{qty}")
        slow_print("0. Cancel")
        choice = input("Choose item number to use: ")
        try:
            choice_num = int(choice)
            if choice_num == 0:
                return
            if 1 <= choice_num <= len(inventory_list):
                item_name = inventory_list[choice_num -1][0]
                item = ITEM_DATABASE.get(item_name)
                if item:
                    item.use(self.player, self.enemy)
                    self.player.inventory.remove(item)
                else:
                    slow_print("Invalid item choice.")
            else:
                slow_print("Invalid choice.")
        except ValueError:
            slow_print("Invalid input.")

    def use_skill(self):
       
        if self.player.mp < 10:
            slow_print("Not enough MP!")
            return
        slow_print("Casting Fireball! Costs 10 MP.")
        self.player.use_mp(10)
        damage = 30 + self.player.level * 2
        damage_dealt = self.enemy.take_damage(damage)
        slow_print(f"Fireball hits {self.enemy.name} for {damage_dealt} damage.")

    def enemy_turn(self):
        slow_print(f"\n{self.enemy.name}'s turn.")
        action = self.enemy.choose_action()
        if action == "attack":
            damage = self.enemy.attack
            damage_dealt = self.player.take_damage(damage)
            slow_print(f"{self.enemy.name} attacks {self.player.name} for {damage_dealt} damage.")
        elif action == "skill":
            
            if self.enemy.use_mp(5):
                damage = self.enemy.attack + 10
                damage_dealt = self.player.take_damage(damage)
                slow_print(f"{self.enemy.name} uses a special skill for {damage_dealt} damage!")
            else:
                damage = self.enemy.attack
                damage_dealt = self.player.take_damage(damage)
                slow_print(f"{self.enemy.name} attacks {self.player.name} for {damage_dealt} damage.")


class Shop:
    def __init__(self, items_for_sale):
        self.items_for_sale = items_for_sale

    def visit(self, player):
        slow_print("\nWelcome to the Shop!")
        while True:
            slow_print(f"You have {player.gold} gold.")
            slow_print("Items available:")
            for i, item in enumerate(self.items_for_sale, start=1):
                slow_print(f"{i}. {item.name} - {item.price} gold")
            slow_print("0. Exit Shop")
            choice = input("Choose item number to buy: ")
            try:
                choice_num = int(choice)
                if choice_num == 0:
                    break
                if 1 <= choice_num <= len(self.items_for_sale):
                    item = self.items_for_sale[choice_num-1]
                    if player.gold >= item.price:
                        player.gold -= item.price
                        player.inventory.add(item)
                        slow_print(f"You bought {item.name}!")
                    else:
                        slow_print("You don't have enough gold.")
                else:
                    slow_print("Invalid choice.")
            except ValueError:
                slow_print("Invalid input.")
            time.sleep(0.5)




class RPGGame:
    def __init__(self):
        self.player = None
        self.running = True

    def start(self):
        clear_screen()
        slow_print("Welcome to the Python RPG!\n")
        if os.path.exists("savegame.json"):
            slow_print("Load saved game? (y/n)")
            if input("> ").lower() == 'y':
                self.player = Player("Hero")
                if not self.player.load():
                    slow_print("Failed to load save, starting new game.\n")
                    self.create_character()
            else:
                self.create_character()
        else:
            self.create_character()

        while self.running:
            clear_screen()
            slow_print(f"Location: {self.player.location}")
            slow_print(LOCATIONS[self.player.location]["description"])
            slow_print(f"HP: {self.player.hp}/{self.player.max_hp} MP: {self.player.mp}/{self.player.max_mp} Gold: {self.player.gold}")
            slow_print("\nWhat would you like to do?")
            slow_print("1. Explore")
            slow_print("2. View Inventory")
            slow_print("3. View Equipment")
            slow_print("4. Visit Shop")
            slow_print("5. Save Game")
            slow_print("6. Quit")

            choice = input("> ")
            if choice == "1":
                self.explore()
            elif choice == "2":
                self.manage_inventory()
            elif choice == "3":
                self.manage_equipment()
            elif choice == "4":
                self.visit_shop()
            elif choice == "5":
                self.player.save()
                time.sleep(1)
            elif choice == "6":
                slow_print("Thanks for playing!")
                self.running = False
            else:
                slow_print("Invalid choice.")
                time.sleep(1)

    def create_character(self):
        slow_print("Enter your character's name:")
        name = input("> ")
        self.player = Player(name)
        slow_print(f"Welcome, {self.player.name}! Your adventure begins...\n")
        time.sleep(1)

    def explore(self):
        location = self.player.location
        connections = LOCATIONS[location]["connections"]
        slow_print("\nWhere do you want to travel?")
        for i, loc in enumerate(connections, start=1):
            slow_print(f"{i}. {loc}")
        slow_print("0. Stay here")
        choice = input("> ")
        try:
            choice_num = int(choice)
            if choice_num == 0:
                slow_print("You stay in place.")
                time.sleep(1)
                return
            if 1 <= choice_num <= len(connections):
                new_location = connections[choice_num -1]
                self.player.location = new_location
                slow_print(f"Traveling to {new_location}...")
                time.sleep(1)
                self.random_encounter()
            else:
                slow_print("Invalid choice.")
                time.sleep(1)
        except ValueError:
            slow_print("Invalid input.")
            time.sleep(1)

    def random_encounter(self):
        if self.player.location == "Town":
            slow_print("It's peaceful here. No enemies around.")
            time.sleep(1)
            return

        encounter_chance = 0.6  
        if random.random() < encounter_chance:
            enemy = self.generate_enemy_for_location(self.player.location)
            combat = Combat(self.player, enemy)
            if not combat.start():
                self.running = False
        else:
            slow_print("No enemies found. You explore peacefully.")
            time.sleep(1)

    def generate_enemy_for_location(self, location):
        if location == "Forest":
            return Enemy("Goblin", max_hp=50, max_mp=20, attack=10, defense=5, level=3, exp_reward=30, gold_reward=20)
        elif location == "Mountain":
            return Enemy("Orc", max_hp=80, max_mp=10, attack=15, defense=8, level=5, exp_reward=50, gold_reward=40)
        elif location == "Dungeon Entrance":
            return Enemy("Slime", max_hp=30, max_mp=10, attack=5, defense=2, level=1, exp_reward=15, gold_reward=10)
        elif location == "Dungeon":
            return Enemy("Dragon", max_hp=200, max_mp=50, attack=25, defense=15, level=10, exp_reward=150, gold_reward=200)
        else:
            return Enemy("Rat", max_hp=20, max_mp=5, attack=3, defense=1, level=1, exp_reward=5, gold_reward=3)

    def manage_inventory(self):
        while True:
            clear_screen()
            slow_print("Inventory Management:")
            self.player.inventory.show()
            slow_print("\nOptions:")
            slow_print("1. Use Item")
            slow_print("2. Back")
            choice = input("> ")
            if choice == "1":
                self.use_inventory_item()
            elif choice == "2":
                break
            else:
                slow_print("Invalid choice.")
                time.sleep(1)

    def use_inventory_item(self):
        inv = self.player.inventory
        if not inv.items:
            slow_print("Inventory empty.")
            time.sleep(1)
            return
        slow_print("Choose item to use:")
        inventory_list = list(inv.items.items())
        for i, (item_name, qty) in enumerate(inventory_list, start=1):
            slow_print(f"{i}. {item_name} x{qty}")
        slow_print("0. Cancel")
        choice = input("> ")
        try:
            choice_num = int(choice)
            if choice_num == 0:
                return
            if 1 <= choice_num <= len(inventory_list):
                item_name = inventory_list[choice_num -1][0]
                item = ITEM_DATABASE.get(item_name)
                if item:
                    if item.item_type == "consumable":
                        item.use(self.player)
                        inv.remove(item)
                    else:
                        slow_print("Cannot use that item here. Try equipping it.")
                else:
                    slow_print("Invalid item.")
            else:
                slow_print("Invalid choice.")
            time.sleep(1)
        except ValueError:
            slow_print("Invalid input.")
            time.sleep(1)

    def manage_equipment(self):
        while True:
            clear_screen()
            slow_print(f"Equipment:")
            slow_print(f"Weapon: {self.player.equipment.weapon.name if self.player.equipment.weapon else 'None'}")
            slow_print(f"Armor: {self.player.equipment.armor.name if self.player.equipment.armor else 'None'}")
            slow_print("\nOptions:")
            slow_print("1. Equip Item")
            slow_print("2. Unequip Item")
            slow_print("3. Back")
            choice = input("> ")
            if choice == "1":
                self.equip_item()
            elif choice == "2":
                self.unequip_item()
            elif choice == "3":
                break
            else:
                slow_print("Invalid choice.")
                time.sleep(1)

    def equip_item(self):
        inv = self.player.inventory
        equ = self.player.equipment
        equipable_items = [item for item in ITEM_DATABASE.values() if item.name in inv.items and item.item_type in ["weapon", "armor"]]
        if not equipable_items:
            slow_print("No equipable items in inventory.")
            time.sleep(1)
            return
        slow_print("Choose item to equip:")
        for i, item in enumerate(equipable_items, start=1):
            slow_print(f"{i}. {item.name}")
        slow_print("0. Cancel")
        choice = input("> ")
        try:
            choice_num = int(choice)
            if choice_num == 0:
                return
            if 1 <= choice_num <= len(equipable_items):
                item = equipable_items[choice_num -1]
                if item.item_type == "weapon" and equ.weapon:
                    equ.unequip(self.player, "weapon")
                elif item.item_type == "armor" and equ.armor:
                    equ.unequip(self.player, "armor")
                equ.equip(self.player, item)
                self.player.inventory.remove(item)
                slow_print(f"Equipped {item.name}.")
            else:
                slow_print("Invalid choice.")
            time.sleep(1)
        except ValueError:
            slow_print("Invalid input.")
            time.sleep(1)

    def unequip_item(self):
        equ = self.player.equipment
        slow_print("Unequip:")
        slow_print("1. Weapon")
        slow_print("2. Armor")
        slow_print("0. Cancel")
        choice = input("> ")
        if choice == "1":
            if equ.weapon:
                equ.unequip(self.player, "weapon")
                self.player.inventory.add(equ.weapon)
            else:
                slow_print("No weapon equipped.")
            time.sleep(1)
        elif choice == "2":
            if equ.armor:
                equ.unequip(self.player, "armor")
                self.player.inventory.add(equ.armor)
            else:
                slow_print("No armor equipped.")
            time.sleep(1)
        elif choice == "0":
            return
        else:
            slow_print("Invalid choice.")
            time.sleep(1)

    def visit_shop(self):
        if self.player.location != "Town":
            slow_print("There is no shop here.")
            time.sleep(1)
            return
        shop_items = list(ITEM_DATABASE.values())
        shop = Shop(shop_items)
        shop.visit(self.player)

if __name__ == "__main__":
    game = RPGGame()
    game.start()

