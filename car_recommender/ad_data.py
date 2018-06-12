import collections

"""This module defines AdData data type

AdData objects spawning:

AdData(<description string>,
       <a hyperlink to the ad>,
       <a list of tuples: (tag, value)>)

Examples:
desc = 'Best VW Passat in SF Bay!''
link = "https://sfbay.craigslist.org/eby/cto/d/00-vw-sports-wagon-1-owner/6607249314.html"
tags = [('odometer', 123000), ('year', 1999)]

ad1 = AdData(desc, link, tags)
# or:
ad2 = AdData(description=desc, hyperlink=link, tags=tags)
"""

AdData = collections.namedtuple('AdData', ['description', 'hyperlink', 'tags'])
