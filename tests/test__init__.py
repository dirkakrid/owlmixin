# coding: utf-8

from __future__ import division, absolute_import, unicode_literals

from typing import List, Optional

import pytest

from dictmixin import DictMixin, replace_keys, to_snake

# For python 3.5.0-3.5.1
try:
    from typing import Text
except ImportError:
    pass


class Human(DictMixin):
    def __init__(self, id, name, favorite_spots):
        # type: (int, Text, List[dict]) -> Human
        self.id = id
        self.name = name
        self.favorite_spots = Spot.from_dict2list(favorite_spots)  # type: List[Spot]


class Spot(DictMixin):
    def __init__(self, names, address=None):
        # type: (List[Text], Text) -> Spot
        self.names = names  # type: Text
        self.address = address  # type: Optional[Text]


class TestReplaceKeys:
    def test_need_not_snake(self):
        keymap = {
            "self": "_self",
            "before": "after"
        }
        d = {
            "before": 1,
            "before2": 2,
            "self": 3,
            "self2": 4,
            "UpperCamelCase": True,
            "lowerCamelCase": True,
            "snake_case": True,
            "chain-case": True,
        }

        expected = {
            "after": 1,
            "before2": 2,
            "_self": 3,
            "self2": 4,
            "UpperCamelCase": True,
            "lowerCamelCase": True,
            "snake_case": True,
            "chain-case": True
        }

        assert replace_keys(d, keymap, False) == expected

    def test_need_must_snake(self):
        keymap = {
            "self": "_self",
            "before": "after"
        }
        d = {
            "before": 1,
            "before2": 2,
            "self": 3,
            "self2": 4,
            "UpperCamelCase": True,
            "lowerCamelCase": True,
            "snake_case": True,
            "chain-case": True
        }

        expected = {
            "after": 1,
            "before2": 2,
            "_self": 3,
            "self2": 4,
            "upper_camel_case": True,
            "lower_camel_case": True,
            "snake_case": True,
            "chain_case": True
        }

        assert replace_keys(d, keymap, True) == expected


class TestToSnake:
    def test_lower_camel(self):
        assert to_snake("lowerCamelCase") == "lower_camel_case"

    def test_upper_camel(self):
        assert to_snake("UpperCamelCase") == "upper_camel_case"

    def test_chain(self):
        assert to_snake("chain-case-example") == "chain_case_example"

    def test_snake(self):
        assert to_snake("snake_case_is_same") == "snake_case_is_same"


class TestFromDict:
    def test_normal(self):
        r = Human.from_dict({
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"]}
            ]
        })

        assert r.id == 1
        assert r.name == "メンバ1"
        assert len(r.favorite_spots) == 2

        assert len(r.favorite_spots[0].names) == 1
        assert r.favorite_spots[0].names[0] == "spot1"
        assert r.favorite_spots[0].address == "address1"

        assert len(r.favorite_spots[1].names) == 2
        assert r.favorite_spots[1].names[0] == "spot21"
        assert r.favorite_spots[1].names[1] == "spot22"
        assert r.favorite_spots[1].address is None

    def test_none(self):
        with pytest.raises(AttributeError):
            Human.from_dict(None)


class TestFromOptionalDict:
    def test_normal(self):
        r = Human.from_optional_dict({
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"]}
            ]
        })

        assert r.id == 1
        assert r.name == "メンバ1"
        assert len(r.favorite_spots) == 2

        assert len(r.favorite_spots[0].names) == 1
        assert r.favorite_spots[0].names[0] == "spot1"
        assert r.favorite_spots[0].address == "address1"

        assert len(r.favorite_spots[1].names) == 2
        assert r.favorite_spots[1].names[0] == "spot21"
        assert r.favorite_spots[1].names[1] == "spot22"
        assert r.favorite_spots[1].address is None

    def test_none(self):
        assert Human.from_optional_dict(None) is None


class TestFromDict2List:
    def test_normal(self):
        r = Spot.from_dict2list([
            {"names": ["spot1"], "address": "address1"},
            {"names": ["spot21", "spot22"]}
        ])

        assert len(r) == 2
        assert r[0].to_dict() == {"names": ["spot1"], "address": "address1"}
        assert r[1].to_dict() == {"names": ["spot21", "spot22"], "address": None}


class TestFromOptionalDict2List:
    def test_normal(self):
        r = Spot.from_optional_dict2list([
            {"names": ["spot1"], "address": "address1"},
            {"names": ["spot21", "spot22"]}
        ])

        assert len(r) == 2
        assert r[0].to_dict() == {"names": ["spot1"], "address": "address1"}
        assert r[1].to_dict() == {"names": ["spot21", "spot22"], "address": None}

    def test_none(self):
        assert Human.from_optional_dict2list(None) is None


class TestFromDict2Dict:
    def test_normal(self):
        r = Spot.from_dict2dict({
            "spot1": {"names": ["spot1"], "address": "address1"},
            "spot2": {"names": ["spot21", "spot22"]}
        })

        assert len(r) == 2
        assert r["spot1"].to_dict() == {"names": ["spot1"], "address": "address1"}
        assert r["spot2"].to_dict() == {"names": ["spot21", "spot22"], "address": None}


class TestFromOptionalDict2Dict:
    def test_normal(self):
        r = Spot.from_optional_dict2dict({
            "spot1": {"names": ["spot1"], "address": "address1"},
            "spot2": {"names": ["spot21", "spot22"]}
        })

        assert len(r) == 2
        assert r["spot1"].to_dict() == {"names": ["spot1"], "address": "address1"}
        assert r["spot2"].to_dict() == {"names": ["spot21", "spot22"], "address": None}

    def test_none(self):
        assert Human.from_optional_dict2dict(None) is None


class TestToDict:
    def test_normal(self):
        r = Human.from_dict({
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"]}
            ]
        })

        assert r.to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"], "address": None}
            ]
        }

    def test_ignore_none(self):
        r = Human.from_dict({
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"]}
            ]
        })

        assert r.to_dict(ignore_none=True) == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"]}
            ]
        }


class TestFromJson:
    def test_normal(self):
        r = Human.from_json("""{
            "favorite_spots": [
                {"address": "address1", "names": ["spot1"]},
                {"names": ["spot21", "spot22"]}
            ],
            "id": 1,
            "name": "メンバ1"
        }
        """)

        assert r.to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"], "address": None}
            ]
        }


class TestFromYaml:
    def test_normal(self):
        r = Human.from_yaml("""
            id: 1
            name: "メンバ1"
            favorite_spots:
              - address: address1
                names:
                  - spot1
              - names:
                  - spot21
                  - spot22
        """)

        assert r.to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"], "address": None}
            ]
        }


class TestToJson:
    def test_normal(self):
        r = Human.from_dict({
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"]}
            ]
        })

        assert r.to_json() == """{
"favorite_spots": [{"address": "address1","names": ["spot1"]},{"address": null,"names": ["spot21","spot22"]}],
"id": 1,
"name": "メンバ1"
}
""".replace("\n", "")


class TestToPrettyJson:
    def test_normal(self):
        r = Human.from_dict({
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"]}
            ]
        })

        assert r.to_pretty_json() == """
{
    "favorite_spots": [
        {
            "address": "address1",
            "names": [
                "spot1"
            ]
        },
        {
            "address": null,
            "names": [
                "spot21",
                "spot22"
            ]
        }
    ],
    "id": 1,
    "name": "メンバ1"
}
""".strip()


class TestToYaml:
    def test_normal(self):
        r = Human.from_dict({
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"]}
            ]
        })

        assert r.to_yaml() == """
favorite_spots:
  - address: address1
    names:
      - spot1
  - address: null
    names:
      - spot21
      - spot22
id: 1
name: メンバ1
""".lstrip()
