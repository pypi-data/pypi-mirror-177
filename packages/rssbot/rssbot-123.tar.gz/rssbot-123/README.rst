**NAME**


 ``rssbot`` - feeding rss into your irc channel.

**SYNOPSIS**


 | ``rssctl cfg server=<server> channel=<channel>``
 | ``rssctl rss <url>``
 |

**INSTALL**

 as root:

 | ``pip3 install rssbot --upgrade --force-reinstall``
 |
 | ``cp /usr/local/share/rssbot/rssbot.service /etc/systemd/system``
 | ``systemctl enable rssbot --now``

 | ``* default channel/server is #rssbot on localhost``

**DESCRIPTION**

 ``rssbot`` is a python3 IRC bot that runs as a background daemon for 24/7 a day presence on IRC, where it is feeding rss into your channel.

 | github: <http://github.com/bthate/rssbot> pypi: <http://pypi.org/project/operbot>

**CONFIGURATION**

 as root:

 | ``rssctl cfg server=<server> channel=<channel>``
 | ``rssctl pwd <nickservnick> <nickservpass>``
 | ``rssctl cfg password=<outputfrompwd>``
 | ``rssctl rss <url>``

**AUTHOR**


 | Bart Thate
 |


**NOTICE**


 | ``rssbot`` is placed in the Public Domain, no Copyright, no LICENSE.

