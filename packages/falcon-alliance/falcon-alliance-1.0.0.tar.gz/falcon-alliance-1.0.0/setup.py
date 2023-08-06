# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['falcon_alliance',
 'falcon_alliance.plotting',
 'falcon_alliance.schemas',
 'falcon_alliance.tests',
 'falcon_alliance.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<3.9.0',
 'matplotlib>=3.6.0,<3.7.0',
 'python-dotenv>=0.19,<1.0',
 'scipy>=1.9.2,<1.10.0']

setup_kwargs = {
    'name': 'falcon-alliance',
    'version': '1.0.0',
    'description': 'A Pythonic library that attains FRC-related information from sources like The Blue Alliance and more.',
    'long_description': "# FalconAlliance\n### A Pythonic wrapper around TBA and other FRC data sources at your convenience. You can find the documentation [here](https://falcon-alliance.readthedocs.io/en/latest).\n\n<hr>\n\n## Installation\n\nTo install `falcon-alliance`, run the following in your console:\n```console\n(.venv) $ pip install falcon-alliance\n```\n\nIf the following doesn't work, and you get an error regarding pip not being a command, try one of the following below:\n```console\n(.venv) $ python -m pip install falcon-alliance\n```\n```console\n(.venv) $ python3 -m pip install falcon-alliance\n```\n```console\n(.venv) $ python3.<your_version> -m pip install falcon-alliance\n```\n\n## Setup\n\nOnce you have `falcon-alliance` installed, a basic skeleton of FalconAlliance code is \n```py\nimport falcon_alliance\n\nwith falcon_alliance.ApiClient(api_key=YOUR_API_KEY) as api_client:\n  # Code using the API client here\n```\n<sup> For more information about the building block of FalconAlliance code, check out [this section](https://falcon-alliance.readthedocs.io/en/latest/getting_started/quick_start.html#building-block-of-falconalliance-code) of our documentation. </sup>\n\nDo note that passing in the API key is not required if the API key is already stored in your `.env` file under the name `TBA_API_KEY` or `API_KEY`. \n\nAs for the code within the context manager (the with statement), below is an example of retrieving a list of all the teams that played in 2022 via FalconAlliance:\n```py\nimport falcon_alliance\n\nwith falcon_alliance.ApiClient(api_key=YOUR_API_KEY) as api_client:\n  all_teams = api_client.teams(year=2022)\n```\n<sup> For more examples with the building block, check out the [Common Tasks](https://falcon-alliance.readthedocs.io/en/latest/getting_started/quick_start.html#common-tasks) section and the [Examples](https://falcon-alliance.readthedocs.io/en/latest/getting_started/examples.html) section.\n\n## Structure\nThe structure of FalconAlliance code follows a hierarchy, with `ApiClient` being at the top, containing agnostic methods like getting a list of all teams from a certain year, a list of all events from a certain year, etc. \n\nIn the middle of the hierarchy are schemas with methods in them, containing endpoints depending on a certain team/event/district. `Team`, `Event`, and `District`, which wrap around endpoints that depend on a certain key (team key/event key/district key). An example of a method for each of the following classes are:\n  - `Team.events`, which wraps around the `/team/{team_key}/events` endpoint.\n  - `Event.teams`, which wraps around the `/event/{event_key}/teams` endpoint.\n  - `District.rankings`, which wraps around the `/district/{district_key}/rankings` endpoint.\n\nAt the bottom of the hierarchy are schemas which primarily act as data-classes, and are there as a means of communicating data in a readable format rather than having functionality. The classes at the bottom of the hierarchy are: `Award`, `EventTeamStatus`, `Match`, `Media`, and `Robot`.\n\n## Plotting\nFalconAlliance has a plotting feature that makes on-the-fly visualizations for you based on your data. **You can learn more about the plotting feature [here](https://github.com/team4099/FalconAlliance/blob/main/PLOTTING.md).**\n\n## Examples\n### [Creating a Dictionary Containing how many Teams each State has](https://falcon-alliance.readthedocs.io/en/latest/getting_started/examples.html#creating-a-dictionary-containing-how-many-teams-each-state-has)\n```py\nimport falcon_alliance\n\nstates_to_teams = {}\n\nwith falcon_alliance.ApiClient(api_key=YOUR_API_KEY) as api_client:\n   all_teams = api_client.teams(year=2022)\n\n   for team in all_teams:\n       states_to_teams[team.state_prov] = states_to_teams.get(team.state_prov, 0) + 1\n```\n### [Getting the Average Rookie Year of Teams in a District](https://falcon-alliance.readthedocs.io/en/latest/getting_started/examples.html#getting-the-average-rookie-year-of-teams-in-a-district)\n```py\nimport falcon_alliance\n\nwith falcon_alliance.ApiClient(api_key=YOUR_API_KEY) as api_client:\n    team4099 = falcon_alliance.Team(4099)\n\n    # Suggested way\n    match_with_max_score = team4099.max(2022, metric=falcon_alliance.Metrics.MATCH_SCORE)\n    maximum_score = match_with_max_score.alliance_of(team4099).score\n\n    # Alternative way\n    match_scores = []\n\n    for match in team4099.matches(year=2022):\n        match_scores.append(match.alliance_of(team4099).score)\n\n    maximum_match_score = max(match_scores)\n```\n### [Finding the Maximum Score from all the Matches a Team Played During a Year](https://falcon-alliance.readthedocs.io/en/latest/getting_started/examples.html#finding-the-maximum-score-from-all-the-matches-a-team-played-during-a-year)\n```py\nimport falcon_alliance\n\nwith falcon_alliance.ApiClient(api_key=YOUR_API_KEY) as api_client:\n    team4099 = falcon_alliance.Team(4099)\n\n    # Suggested way\n    match_with_max_score = team4099.max(2022, metric=falcon_alliance.Metrics.MATCH_SCORE)\n    maximum_score = match_with_max_score.alliance_of(team4099).score\n\n    # Alternative way\n    match_scores = []\n\n    for match in team4099.matches(year=2022):\n        match_scores.append(match.alliance_of(team4099).score)\n\n    maximum_match_score = max(match_scores)\n```\n\n**More examples are listed on the documentation [here](https://falcon-alliance.readthedocs.io/en/latest/getting_started/examples.html#examples).**\n",
    'author': 'The Falcons - Team 4099',
    'author_email': 'contact@team4099.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/team4099/FalconAlliance',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
