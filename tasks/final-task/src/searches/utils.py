from typing import Any, Dict, List


class Player:
    def __init__(self, player_dict: Dict[str, Any]):
        self.id = str(player_dict["id"]).strip()
        self.name = player_dict["name"].strip()
        self.position = player_dict["position"].strip()
        self.club = player_dict["club"].strip()
        self.score = float(player_dict["score"])
        self.price = float(player_dict["price"])

    @property
    def price_efficiency(self):
        return self.score / self.price

    def __eq__(self, other):
        if other is None or not isinstance(other, Player):
            return False

        return (
            self.id == other.id
            and self.name == other.name
            and self.position == other.position
            and self.club == other.club
            and self.score == other.score
            and self.price == other.price
        )

    def __str__(self):
        return (
            f"[{self.id}] {self.name} ({self.position}) from {self.club} "
            f"({self.score} for {self.price:g}m)"
        )

    def __repr__(self):
        return str(self)

    def __hash__(self):
        try:
            return int(self.id)
        except Exception:
            return -1


def get_player_data_from_row(row: List) -> Dict[str, Any]:
    return {
        "id": row[0],
        "position": row[1],
        "name": row[2],
        "club": row[3],
        "score": row[4],
        "price": row[5],
    }


def get_players_from_rows(rows: List[List]) -> List[Player]:
    return [Player(get_player_data_from_row(row)) for row in rows]
