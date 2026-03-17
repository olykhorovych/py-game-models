import sys

import init_django_orm  # noqa: F401
import json
from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json") as json_file:
        data = json.load(json_file)
    if Race.objects.exists():
        Race.objects.all().delete()
    if Skill.objects.exists():
        Skill.objects.all().delete()
    if Guild.objects.exists():
        Guild.objects.all().delete()
    if Player.objects.exists():
        Player.objects.all().delete()

    for player in data:
        current_player = data[player]
        if current_player["guild"] is not None:
            fields = {
                "name": current_player["guild"]["name"],
                "description": current_player["guild"]["description"],
            }
            guild, _ = Guild.objects.get_or_create(
                **{key: value for key, value in fields.items() if value is not None}
            )
        else:
            guild = None

        race, _ = Race.objects.get_or_create(
            name=current_player["race"]["name"],
            description=current_player["race"]["description"],
        )
        for skill in current_player["race"]["skills"]:
            Skill.objects.get_or_create(
                name=skill["name"],
                bonus=skill["bonus"],
                race=race
            )

        kwargs = {
            "nickname": player,
            "email": current_player["email"],
            "bio": current_player["bio"],
            "race": race,
            "guild": guild,
        }
        player = Player(
            **{
                key: value for key, value in kwargs.items() if value is not None
            }
        )
        player.save()


if __name__ == "__main__":
    main()
