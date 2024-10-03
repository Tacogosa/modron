import pytest
from unittest.mock import patch
from modron import Dice
from modron import spellSearch
import os

def test_calculateBonus_above_10():
    dice = Dice()
    assert dice.calculateBonus(11) == "0"
    assert dice.calculateBonus(12) == "+1"
    assert dice.calculateBonus(15) == "+2"
    assert dice.calculateBonus(18) == "+4"

def test_calculateBonus_at_10():
    dice = Dice()
    assert dice.calculateBonus(10) == "0"

def test_calculateBonus_below_10():
    dice = Dice()
    assert dice.calculateBonus(9) == "-1"
    assert dice.calculateBonus(8) == "-1"
    assert dice.calculateBonus(6) == "-2"
    assert dice.calculateBonus(3) == "-4"


@pytest.mark.parametrize("input_value, expected_output", [
    ("acid arrow", "Name:"),
    ("eldritch blast", "Name:"),
    ("Polymorph", "Name:"),
    ("dog", "Spell not found"),
    (" magic missile ", "Name:")
])
def test_spell_search(input_value, expected_output, capfd):
    with patch('builtins.input', return_value=input_value), \
         patch('requests.get') as mock_get:
        
        if input_value == "dog":
            mock_get.return_value.status_code = 404
        else:
            mock_get.return_value.status_code = 200
        
        spellSearch()
        
        out, _ = capfd.readouterr()
        assert expected_output in out

def test_rollStats():
    dice = Dice()
    results = dice.rollStats()
    assert len(results) == 6
    for result in results:
        assert 3 <= result <= 18

# Required Files
def test_files_exist():
    assert os.path.isfile('DnD_5E_CharacterSheet_FormFillable.pdf')
    assert os.path.isfile('modron.py')