import collections

"""This module defines AdData data type

AdData objects spawning:

AdData(<description string>,
       <a hyperlink to the ad>)

Examples:
desc = 'Best VW Passat in SF Bay!''
link = "https://sfbay.craigslist.org/eby/cto/d/00-vw-sports-wagon-1-owner/6607249314.html"

ad1 = AdData(desc, link)
# or:
ad2 = AdData(description=desc, hyperlink=link)
"""

AdData = collections.namedtuple('AdData', ['description', 'hyperlink'])
