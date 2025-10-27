import random
from time import sleep

WARRIORS_NAMES = [
    'Leonardo DiCaprio',
    'Scarlett Johansson',
    'Dwayne Johnson',
    'Jennifer Lawrence',
    'Tom Hanks',
    'Angelina Jolie',
    'Will Smith',
    'Emma Watson',
    'Robert Downey Jr.',
    'Beyoncé',
    'Chris Hemsworth',
    'Taylor Swift',
    'Brad Pitt',
    'Meryl Streep',
    'Ryan Reynolds',
    'Natalie Portman',
    'Keanu Reeves',
    'Sandra Bullock',
    'Julia Roberts',
    'Samuel L. Jackson',
]
print(f'Имен в списке:{len(WARRIORS_NAMES)}')

WEAPONS = [
    'Sword', 'Shield', 'Helmet', 'Nike Air', 'Armor', 'Bow', 'Arrow',
    'Spade', 'Axe', 'Mace', 'Blowfish', 'Stick', 'Ring', 'Underpants'
]

# Скорость боя
BATTLE_SPEED = 0.2


class Weapon:
    name: str
    protection: float
    damage: int

    def __init__(self, name: str, protection: float, damage: int):
        self.name = name
        self.protection = protection
        self.damage = damage

    def __str__(self):
        return (f"{self.name}: +Damage: {self.damage}, +ATK{self.damage}, "
                f"+DEF{self.protection:.2f}")


class Person:
    name: str
    health: int
    weapons: list
    base_attack: int
    base_protection: float

    def crit_chance(self):
        if self.hp <= 50:
            random_num = random.randint(1, 10)
            if random_num == 1:
                self.critical_hit()

    def critical_hit(self):
        self.base_attack = self.base_attack * 3
        print(f'💥 💥 💥 {self.name} is activate a critical hit!💥 💥 💥 ')
        print(f'Attack is 3X -- {self.base_attack} and HP is - {self.hp}')

    def set_weapons(self, weapons: list):
        self.weapons = weapons

    def __init__(self, name: str, hp: int, attack: int, protection: float):
        self.name = name
        self.hp = hp
        self.base_attack = attack
        self.base_protection = protection
        self.weapons = []

    def __repr__(self):
        return (f"{self.__class__.__name__}(name={self.name!r}, hp={self.hp}, "
                f"damage={self.base_attack}, prot={self.base_protection:.2f}, "
                f"weapons={self.weapons!r})")

    def __str__(self):
        # краткий вывод для print(p)
        return (f"{self.__class__.__name__} {self.name}: "
                f"HP={round(self.hp, 1)}, ATK={self.base_attack}, "
                f"DEF={self.base_protection:.2f}")


class Paladin(Person):

    def __init__(self, name, hp, base_attack, protection):
        super().__init__(name, hp, base_attack, protection)
        self.hp = hp * 2
        self.base_protection = protection * 2


class Warrior(Person):
    def __init__(self, name, hp, base_attack, protection):
        super().__init__(name, hp, base_attack, protection)
        self.base_attack = base_attack * 2


def damage(weapon, attacker):
    """
    Calculate the total damage dealt by an attacker using a selected weapon.

    The function selects a random weapon from the given list, calculates the
    damage by adding the weapon's damage to the base attack of the attacker,
    and returns the computed damage value.
    """
    selected_weapon = random.choice(weapon)
    weapon_damage = selected_weapon.damage
    print(
        f'Attacker {attacker.name} choose weapon for fight - {selected_weapon}'
    )
    calc_damage = weapon_damage + attacker.base_attack
    return calc_damage


def protection(weapon, defender):
    """
    Calculates the total protection value for a defender based on their base
    protection and the protection value of a randomly chosen weapon.
    """
    selected_weapon = random.choice(weapon)
    print(f'Defender: {defender} choose for protection - {selected_weapon}')
    def_protection = defender.base_protection + selected_weapon.protection
    return def_protection


def generate_weapons():
    weapon_list = []
    for weapon in range(20):
        name = random.choice(WEAPONS)
        protection = random.uniform(0.01, 2.0)
        damage = random.randint(1, 10)
        weapon_list.append(Weapon(name, round(protection, 1), damage))
    return weapon_list


def generate_person():
    person_list = []
    for person in WARRIORS_NAMES:
        if person not in person_list:
            name = person
            hp = random.randint(1, 100)
            base_attack = random.randint(1, 10)
            protection = random.uniform(0.01, 1.0)
            cls_warrior = random.choice([Paladin, Warrior])
            person_list.append(
                cls_warrior(name, hp, base_attack, round(protection, 1)))

    return person_list


def dress_up_warrior():
    warriors = generate_person()
    print(f"[dress_up_warrior] Сгенерировано персонажей: {len(warriors)}")

    for idx, person in enumerate(warriors, 1):
        count = random.randint(1, 4)
        all_items = generate_weapons()
        items = random.sample(all_items, count)

        person.set_weapons(items)

        # print(f"{idx}.{person.name} ({person.__class__.__name__}):")
        # print(f"— должен получить {count} вещей")
        # print(f"— взяты из общей кучи (размер {len(all_items)})")
        # print(f"— полученные вещи: {[weapon.name for weapon in items]}")
        # print(f"— детали вещей: {items!r}")

    return warriors


def main():
    fighters = dress_up_warrior()
    winners = []

    def arena(fighters, hits: int):

        while len(fighters) > 0:
            if len(fighters) < 2:
                print(f'В списке недостаточно элементов - {len(fighters)}')
                print(f'Победитель  -- {winners}')
                return

            index1 = random.randrange(len(fighters))
            index2 = random.randrange(len(fighters))

            while index1 == index2:
                index2 = random.randrange(len(fighters))

            attacker = fighters.pop(index1)

            defender = fighters.pop(index2 if index2 < index1 else index2 - 1)
            print('__NEW fight is begin!__')
            print(f'Attacker: {attacker} \nDefender: {defender}')
            attacker.crit_chance()
            defender.crit_chance()
            hits = 0

            while defender.hp > 0 and attacker.hp > 0:
                hits += 1
                attacker_dem = damage(attacker.weapons, attacker)
                defender_protection = protection(defender.weapons, defender)
                hit = max(0, attacker_dem - defender_protection)
                defender.hp -= hit
                if defender.hp <= 0:
                    winners.append(attacker)
                    print(
                        f'Attacker {attacker.name} is win! {defender.name} '
                        f'is dead from {hits} hits.'
                    )
                    continue
                else:
                    print(
                        f'Fight is continue {defender.name} is alive! '
                        f'HP - {round(defender.hp, 1)}'
                    )

                sleep(BATTLE_SPEED)
                defender_dem = damage(defender.weapons, defender)
                attacker_protection = protection(attacker.weapons, attacker)
                hit = max(0, defender_dem - attacker_protection)
                print('Now Defender is attacking the attacker! \n')
                attacker.hp -= hit
                if attacker.hp <= 0:
                    print(
                        f'Defender {defender.name} is win! {attacker.name} \n'
                        f'is dead from {hits} hits.'
                    )
                    winners.append(defender)
                    continue
                else:
                    print(
                        f'Fight is continue {attacker.name} is alive! '
                        f'HP - {round(attacker.hp, 1)}'
                    )

    arena(fighters, 0)
    print('🔥 🔥 🔥 Now is a battle of winners! Fight!🔥 🔥 🔥 ')
    for w in winners:
        print(f'Win {w}!')
    arena(winners, 0)


if __name__ == '__main__':
    main()
