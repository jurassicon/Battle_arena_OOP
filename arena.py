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

THINGS = ['Sword', 'Shield', 'Helmet', 'Nike Air', 'Armor', 'Bow', 'Arrow',
          'Spade', 'Axe', 'Mace', 'Blowfish', 'Stick', 'Ring', 'Underpants']


class Thing:
    name: str
    protection: float
    damage: int

    def __init__(self, name: str, protection: float, damage: int):
        self.name = name
        self.protection = protection
        self.damage = damage

    def __repr__(self):
        # repr для отладки: всё, что важно
        return (f"Thing(name={self.name!r}, protection={self.protection:.2f}, "
                f"damage={self.damage}")

    def __str__(self):
        # str для "красивого" вывода
        return (f"{self.name}: +Damage: {self.damage}, +ATK{self.damage}, "
                f"+DEF{self.protection:.2f}")


class Person:
    name: str
    health: int
    things: list
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
        print(f'Attack is 3X -- {self.base_attack}')

    def set_things(self, things: list):
        self.things = things

    def __init__(self, name: str, hp: int, attack: int, protection: float):
        self.name = name
        self.hp = hp
        self.base_attack = attack
        self.base_protection = protection
        self.things = []

    def __repr__(self):
        return (f"{self.__class__.__name__}(name={self.name!r}, hp={self.hp}, "
                f"damage={self.base_attack}, prot={self.base_protection:.2f}, "
                f"things={self.things!r})")

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


def damage(thing, attacker):
    selected_weapon = random.choice(thing)
    weapon_damage = selected_weapon.damage
    print(
        f'Attacker {attacker.name} choose weapon for fight - {selected_weapon}')
    calc_damage = weapon_damage + attacker.base_attack
    return calc_damage


def protection(thing, defender):
    selected_weapon = random.choice(thing)
    print(f'Defender: {defender} choose for protection - {selected_weapon}')
    def_protection = defender.base_protection + selected_weapon.protection
    return def_protection


def generate_things():
    thing_list = []
    for thing in range(20):
        name = random.choice(THINGS)
        protection = random.uniform(0.01, 2.0)
        damage = random.randint(1, 10)
        thing_list.append(Thing(name, round(protection, 1), damage))
    return thing_list


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
    people = generate_person()
    print(f"[dress_up_warrior] Сгенерировано персонажей: {len(people)}")

    for idx, person in enumerate(people, 1):
        count = random.randint(1, 4)
        all_items = generate_things()
        items = random.sample(all_items, count)

        person.set_things(items)

        # print(f"{idx}.{person.name} ({person.__class__.__name__}):")
        # print(f"— должен получить {count} вещей")
        # print(f"— взяты из общей кучи (размер {len(all_items)})")
        # print(f"— полученные вещи: {[thing.name for thing in items]}")
        # print(f"— детали вещей: {items!r}")

    return people


def main():
    fighters = dress_up_warrior()
    print(fighters)
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

            # если вы уже попали элемент по index1, индекс второго может «съехать».
            # Без лишней головы: просто выберем второго из оставшихся.
            defender = fighters.pop(index2 if index2 < index1 else index2 - 1)
            print(f'__NEW fight is begin!__')
            attacker.crit_chance()
            defender.crit_chance()
            hits = 0

            while defender.hp > 0 and attacker.hp > 0:
                hits += 1
                attacker_dem = damage(attacker.things, attacker)
                defender_protection = protection(defender.things, defender)
                hit = max(0, attacker_dem - defender_protection)
                defender.hp -= hit
                if defender.hp <= 0:
                    winners.append(attacker)
                    print(
                        f'Attacker {attacker.name} is win! {defender.name} is dead from {hits} hits.')
                    continue
                else:
                    print(
                        f'Fight is continue {defender.name} is alive! HP - {round(defender.hp, 1)}')

                sleep(0.1)
                print('Now Defender is attacking the attacker!')
                defender_dem = damage(defender.things, defender)
                attacker_protection = protection(attacker.things, attacker)
                attacker.hp -= (defender_dem - attacker_protection)
                hit = max(0, defender_dem - attacker_protection)
                attacker.hp -= hit
                if attacker.hp <= 0:
                    print(
                        f'Defender {defender.name} is win! {attacker.name} is dead from {hits} hits.')
                    winners.append(defender)
                    continue
                else:
                    print(
                        f'Fight is continue {attacker.name} is alive! HP - {round(attacker.hp, 1)}')

    arena(fighters, 0)
    print('🔥 🔥 🔥 Now is a battle of winners! Fight!🔥 🔥 🔥 ')
    for w in winners:
        print(f'Win {w}!')
    arena(winners, 0)


if __name__ == '__main__':
    main()
