**NAME**


``rssbot`` - feeding rss into your irc channel.


**SYNOPSIS**


``rssctl cfg server=<server> channel=<channel>``
``rssctl rss <url>``


**INSTALL**


``sudo pip3 install rssbot --upgrade --force-reinstall``


**DESCRIPTION**


``rssbot`` is a rss feed fetching bot, that runs under systemd as a 24/7
background service and starts the bot after reboot. It is written in a
static, only code, no popen, no imports and no reading
modules from a directory, way to have it as secure as possible.

``rssbot`` stores it's data on disk where objects are time versioned and the
last version saved on disk is served to the user layer. Paths carry the type
in the path name what makes reconstruction from filename easier then reading
type from the object.

``rssbot`` is a "only messenger bot" which means it only feeds rss into your
irc channel and does not have commands that can be used in the channel. A
seperate program is provided to do the actual configuration of the bot and
other management function (like adding feed urls).


github: <http://github.com/bthate/rssbot> pypi: <http://pypi.org/project/operbot>


**CONFIGURATION**


``sudo cp /usr/local/share/rssbot/rssbot.service /etc/systemd/system``
``sudo systemctl enable rssbot --now``

``* default channel/server is #rssbot on localhost``

``sudo rssctl cfg server=<server> channel=<channel>``
``sudo rssctl pwd <nickservnick> <nickservpass>``
``sudo rssctl cfg password=<outputfrompwd>``
``sudo rssctl rss <url>``


**AUTHOR**


Bart Thate


**NOTICE**


``rssbot`` is placed in the Public Domain, no Copyright, no LICENSE.
