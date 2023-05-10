import os
from dotenv import load_dotenv
import requests

load_dotenv()
OUTPUT_FOLDER = "output"

# CUSTOMIZABLE VARIABLES
BOARD_ID = "BOARD_ID"
OUTPUT_FILE = f"{OUTPUT_FOLDER}/Kanban.md"
LABELS_TO_TAGS = {
    'languages and frameworks': 'programming_languages programming_frameworks',
    'topics': 'software_concepts',
    'techniques': 'software_techniques',
    'platforms': 'software_platforms'
}

API_KEY = os.getenv("APIKey")
API_TOKEN = os.getenv("APIToken")
BASE_URL = "https://api.trello.com/1"
AUTH_QUERY_PARAMS = f"key={API_KEY}&token={API_TOKEN}"

HEAD = """
---
kanban-plugin: basic
---
"""

TAIL = """
%% kanban:settings
```
{"kanban-plugin":"basic"}
```
%%
"""


def labels_to_tags(label: dict[str]) -> str:
    return LABELS_TO_TAGS.get(label['name'].lower(), '') or label['name'].lower().replace(' ', '_')


def get_lists_for_board(board_id: str) -> list[dict]:
    lists = requests.get(f"{BASE_URL}/boards/{board_id}/lists?{AUTH_QUERY_PARAMS}").json()
    for _list in lists:
        list_id = _list['id']
        _list['cards'] = requests.get(f"{BASE_URL}/lists/{list_id}/cards?{AUTH_QUERY_PARAMS}").json()
    return lists


def write_card_as_separate_note_file(card: dict) -> None:
    labels = [labels_to_tags(label) for label in card['labels']]
    with open(f"{OUTPUT_FOLDER}/{card['name']}.md", 'wt') as card_file:
        header = f"---\ndate: {card['dateLastActivity']}\ntags: {labels}\n---\n"
        card_file.write(header)
        card_file.write(card['desc'])


def main() -> None:
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    with open(OUTPUT_FILE, 'wt') as board_file:
        board_file.write(HEAD)
        lists = get_lists_for_board(BOARD_ID)
        for _list in lists:
            board_file.write(f"## {_list['name']}\n")
            for card in _list['cards']:
                if card['desc']:
                    write_card_as_separate_note_file(card)
                    # Link to card in new file
                    board_file.write(f"- [ ] [[{card['name']}]]\n")
                else:
                    board_file.write(f"- [ ] {card['name']}\n")
        board_file.write(TAIL)


if __name__ == "__main__":
    main()
