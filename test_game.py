#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from game import Game, Player, Map, OutsideRoom, Item, Guard, HallwayRoom, Room

class TestGame(unittest.TestCase):
    def setUp(self):
        super(TestGame, self).setUp()
        self.player = Player(gender='male', age='10', hair_color='blue')

    def tearDown(self):
        super(TestGame, self).tearDown()

    def test_instantiate_game(self):
        a_map = Map(rooms=[])
        game = Game(self.player, a_map)
        self.assertEqual(game.player, self.player)
        self.assertEqual(game.a_map, a_map)

    def test_room_traversal(self):
        start_room = OutsideRoom()
        end_room = HallwayRoom()
        a_map = Map(rooms=[start_room, end_room])
        self.assertEqual(a_map.describe_room(), start_room.about)

        possible_exits = a_map.possible_exits()
        new_room = a_map.move_to(possible_exits[0])
        self.assertIsInstance(new_room, Room)
        self.assertEqual(new_room.about, end_room.about)
        self.assertEqual(a_map.describe_room(), end_room.about)

        possible_exits = a_map.possible_exits()
        self.assertEqual(possible_exits, [])

class TestPlayer(unittest.TestCase):
    def test_player(self):
        player = Player(gender='male', age='10', hair_color='blue')
        self.assertEqual(player.gender, 'male')
        self.assertEqual(player.age, '10')
        self.assertEqual(player.hair_color, 'blue')

class TestMap(unittest.TestCase):
    def test_map(self):
        a_map = Map(rooms=[])
        self.assertIsInstance(a_map.rooms, list)
        self.assertEqual(a_map.start, 0)
        self.assertEqual(a_map.location, a_map.start)

class TestRooms(unittest.TestCase):
    def test_outside(self):
        outside = OutsideRoom()
        self.assertGreater(outside.about, 0)
        self.assertIsInstance(outside.items, list)

    def test_add_item(self):
        rock = Item('rock')
        room = Room()
        before = len(room.items)
        self.assertNotIn(rock, room.items)
        room.add_item(rock)
        self.assertEqual(len(room.items), before+1)
        self.assertIn(rock, room.items)

    def test_show_items(self):
        room = Room()
        room.items = [Item('rock'), Item('egg'), Item('gun')]
        self.assertIn('rock', room.show_items())
        self.assertIn('egg', room.show_items())
        self.assertIn('gun', room.show_items())

    def test_show_no_items(self):
        room = Room()
        room.items = []
        self.assertEqual(room.show_items(), '')

    def test_hallway(self):
        hallway = HallwayRoom()
        self.assertGreater(hallway.about, 0)
        self.assertIsInstance(hallway.items, list)

class TestItems(unittest.TestCase):
    def test_item_default_desc(self):
        item = Item('rock')
        self.assertEqual(item.name, 'rock')
        self.assertEqual(item.desc, "It's just a rock...")
        
    def test_item_custom_desc(self):
        item = Item('', 'xyzzy')
        self.assertEqual(item.desc, 'xyzzy')

    def test_item_default_desc_leading_vowel(self):
        item = Item('egg')
        self.assertEqual(item.name, 'egg')
        self.assertEqual(item.desc, "It's just an egg...")

    def test_npc_item(self):
        guard = Guard('Guard')
        self.assertGreater(len(guard.commands), 0)
        self.assertEqual(guard.say(), 'Stop')
        self.assertEqual(guard.name, 'Guard')

    def test_item_say(self):
        item = Item('rock')
        self.assertEqual(item.say(), '...')
