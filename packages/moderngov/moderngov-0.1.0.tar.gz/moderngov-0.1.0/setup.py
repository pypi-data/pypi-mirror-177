# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moderngov']

package_data = \
{'': ['*']}

install_requires = \
['diskcache>=5.4.0,<6.0.0',
 'requests>=2.28.1,<3.0.0',
 'validators>=0.20.0,<0.21.0',
 'xmltodict>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['moderngov = moderngov.mgq:run']}

setup_kwargs = {
    'name': 'moderngov',
    'version': '0.1.0',
    'description': '',
    'long_description': "# ModernGov Local Council Data API\nAll local councils seem to use some software from [moderngov](https://moderngov.com/) to store ward, committee, councillor,\nand meeting information. This does have an public API but it doesn't accessible or well documented.\n\nI had a need to lookup some local council data digitally and found it quite difficult.\n\nI wished there was a more easily accessible library available when I needed to query it - so I made one!\n\nI did this for Eastleigh & the whole of Hampshire, but it should work for any council making use of the moderngov software to manage their operation, which seems to be most borough and county councils.\n\n# Install\n\n```shell\npip install moderngov\n```\n\n# Example Usage\n\nFirst find the moderngov website your council uses, its usually called demoracy.(council domain), or meetings.(council domain).  Follow a meetings link\nand you will see it. \n\nMaybe some kind person will compile a list of them and add to this repo. :)\n\n\nYou can use this package in two ways:\n## Use the moderngov module\n```shell\n# Connect\nmoderngov = api.Website('https://meetings.eastleigh.gov.uk')\n\n# get a committee list\nmoderngov.committee.list()\n\n# get a ward list\nmoderngov.wards.list()\n\n# get a councillor list\nmoderngov.members.list()\n\n# get a councillor by member id\nmoderngov.members.by_id()\n```\n\n## Use the CLI command\nThe CLI tool doesn't yet support all the options the backend module provides, but still it can be useful for quick lookup.\n\n```shell\n# List the registered wards\n% moderngov meetings.eastleigh.gov.uk -w\nBishopstoke\nBotley\nBursledon and Hound North\nChandler's Ford\nEastleigh Central\nEastleigh North\nEastleigh South\nFair Oak & Horton Heath\nHamble and Netley\nHedge End North\nHedge End South\nHiltingbury\nWest End North\nWest End South\n\n# List the council members\n% moderngov meetings.eastleigh.gov.uk -m \n1451 Councillor Janice Asman\n50000738 Councillor Maud Attrill\n50000483 Councillor Tim Bearder\n50000737 Councillor Steve Beer\n1446 Councillor Paul Bicknell\n500000103 Councillor Alex Bourne\n174 Councillor Alan Broadhurst\n50000683 Councillor Steven Broomfield\n50000684 Councillor Anne Buckley\n50000203 Councillor Ian Corben\n50000282 Councillor Nicholas Couldrey\n180 Councillor Tonia Craig\n731 Councillor Malcolm Cross\n500000114 Councillor Ray Dean\n50000731 Councillor Bhavin Dedhia\n50000484 Councillor James Duguid\n745 Councillor Cynthia Garton\n500000119 Councillor Richard Gomer\n500000098 Councillor Tim Groves\n50000736 Councillor Leigh Hadaway\n644 Councillor Steve Holes\n197 Councillor Keith House\n204 Councillor Wayne Irish\n50000739 Councillor Liz Jarvis\n50000685 Councillor Dave Kinloch\n208 Councillor Rupert Kyrle\n50000084 Councillor Darshan Mann\n500000092 Councillor Adam Manning\n50000482 Councillor Michelle Marsh\n50000682 Councillor Tanya Park\n500000049 Councillor Louise Parker-Jones\n50000082 Councillor David Pragnell\n192 Councillor Derek Pretty\n50000140 Councillor Jane Rich\n50000740 Councillor Cameron Spencer\n918 Councillor Bruce Tennent\n500000050 Councillor Gin Tidridge\n500000108 Councillor Sara Tyson-Payne\n173 Councillor Jane Welsh\n\n# List a council member details\n% moderngov meetings.eastleigh.gov.uk -M 197\nmemberid             197   \nfullusername         Councillor Keith House\nphotosmallurl        https://meetings.eastleigh.gov.uk/UserData/7/9/1/Info00000197/smallpic.jpg\nphotobigurl          https://meetings.eastleigh.gov.uk/UserData/7/9/1/Info00000197/bigpic.jpg\npoliticalpartytitle  Liberal Democrat\npoliticalgrouptitle  none  \ndistricttitle        Hamble\nrepresenting         none  \nkeyposts             Leader of the Council; Cabinet Member for Planning and Property\n\n# List the known committees\n% moderngov meetings.eastleigh.gov.uk -b\n255 Administration Committee\n267 Airport Consultative Committee\n496 Audit and Resources Committee\n432 Audit and Risk Management Committee\n249 Bishopstoke, Fair Oak and Horton Heath Local Area Committee\n265 Bursledon Windmill Joint Management Committee\n250 Bursledon, Hamble-le-Rice and Hound Local Area Committee\n254 Cabinet\n251 Chandler's Ford and Hiltingbury Local Area Committee\n434 Community Wellbeing Scrutiny Panel\n276 Council\n306 Eastleigh Local Area Committee\n264 Eastleigh Museum Joint Management Committee\n333 Eastleigh Strategic Partnership\n359 Eastleigh Strategic Partnership - Executive\n258 Environment & Transport Scrutiny Panel\n433 Environment Scrutiny Panel\n335 Environmental Health and Control Committee\n253 Hedge End, West End and Botley Local Area Committee\n336 Highways And Planning Committee\n337 Highways And Works Committee\n510 Horton Heath Development Management Committee\n338 Housing And Health Committee\n330 Joint Area Committee\n508 Joint Meeting of Policy and Performance Scrutiny Panel and Audit and Resources Committee\n427 Joint Meeting of the Scrutiny Panels\n339 Leisure Centre Consultative Group\n340 Leisure Services Committee\n425 Licensed Transport Forum\n332 Licensing Committee\n356 Licensing Panel\n358 Performance Review Scrutiny Panel\n262 Places Leisure Eastleigh Consultative Group\n341 Planning And Transportation Committee\n486 Policy and Performance Scrutiny Panel\n342 Policy And Resources Committee\n293 Prosperity Scrutiny Panel\n343 Recreation And Amenities Committee\n259 Resources Scrutiny Panel\n436 Scrutiny Management Group\n260 Social Policy Scrutiny Panel\n257 Special Joint Committee\n256 Standards Committee\n495 Standards Sub Committee (Third stage)\n```\n\n",
    'author': 'Adam Ford',
    'author_email': 'feel.wires_0c@icloud.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/afdy/moderngov',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
