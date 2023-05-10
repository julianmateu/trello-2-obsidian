# Trello to Obsidian

Simple script to query the [Trello REST API](https://developer.atlassian.com/cloud/trello/)
to get all lists and cards from a board and replicate it as an [Obsidian](https://obsidian.md)
note to be used with the [Obsidian Kanban plugin](https://github.com/mgmeyers/obsidian-kanban).

## Getting started
1. You'll need an API key and token, follow the steps in the
[official guide](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/).
2. Store them in environment variables `APIKey` and `APIToken`. If you place those in a `.env`
file, it will be loaded automatically by the script.
3. Customize the [`trello_board_to_obsidian.py` script](./trello_board_to_obsidian.py)
to define the `BOARD_ID` (you can get it from the url), and any mappings of labels to
tags in `LABELS_TO_TAGS` (keys should be in lowercase).
4. Create a virtual environment, source it, and install the dependencies:
    ```bash
   python -m venv env
   . env/bin/activate
   pip install -r requirements.txt
    ```
   
5. Run the script:
    ```bash
   python trello_board_to_obsidian.py
    ```
