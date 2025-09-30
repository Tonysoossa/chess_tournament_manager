import os
import json
from pathlib import Path
from controllers.player_controller import PlayerController


def main(base_dir="../data"):
    os.makedirs(base_dir, exist_ok=True)

    files = ["players.json", "tournaments.json"]

    for filename in files:
        filepath = Path(base_dir) / filename

        if not filepath.exists():
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
    controller = PlayerController()
    controller.run()