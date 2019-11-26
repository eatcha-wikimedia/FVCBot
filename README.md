# FVCBot : Featured video candidates bot
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f6844b0fbc5146b7a44413795aada49b)](https://www.codacy.com/manual/eatcha-wikimedia/FVCBot?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=eatcha-wikimedia/FVCBot&amp;utm_campaign=Badge_Grade)[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/eatcha-wikimedia/FVCBot/graphs/commit-activity)[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)[![GPL 3 license](https://img.shields.io/badge/GPL-3-green.svg)](https://github.com/eatcha-wikimedia/FVCBot/blob/master/LICENSE)[![Open Source Love png1](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)


[![FVCBot - Wikimedia Commons](https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Mini-Robot.png/211px-Mini-Robot.png)](https://commons.wikimedia.org/wiki/User:FVCBot)

Hi, I’m [Featured video](https://commons.wikimedia.org/wiki/Commons:Featured_videos) [candidates](https://commons.wikimedia.org/wiki/Commons:Featured_video_candidates) [bot](https://commons.wikimedia.org/wiki/User:FVCBot). My job includes counting of votes, closing nomination, notifying the nominator if the nomination gets featured and marking the featured nominations with featured video tag. I work in 3 shifts a day (5:00, 13:00, 21:00 UTC). I live in the servers of Toollabs (Eqiad cluster), Virginia, Ashburn, United States of America. 

From Eatcha: This script is derived from the source code of [fpcBot](https://github.com/Zitrax/fpcBot) which was originally written by Daniel78 at commons.wikimedia.org / Zitrax on GitHub. Bot's recent edits can be found at [Special:Contributions/FVCBot](https://commons.wikimedia.org/wiki/Special:Contributions/FVCBot)

This bot runs in 3 shifts 5:00, 13:00, 21:00 UTC  , the cronjob looks like the following. 
0 5,13,21 * * * jsub -once python3 fvc.py -park -close -auto

## Usage
There are 11 Command-line arguments supported by this python script.
* test Perform a testrun against an old log
* close Close and add result to the nominations
* info Just print the vote count info about the current nominations
* park Park closed and verified candidates
* auto Do not ask before commiting edits to articles
* dry Do not submit any edits, just print them
* threads Use threads to speed things up, can't be used in interactive mode
* fpc Handle the featured candidates (if neither -fpc or -delist is used all candidates are handled)
* delist Handle the delisting candidates (if neither -fpc or -delist is used all candidates are handled)
* notime Avoid displaying timestamps in log output
* match pattern Only operate on candidates matching this pattern
### To close, park candidate automatically we use
```bash

```

## Emergency bot shutoff button, can be used by wikimedia commons Administrators only

[![FVCBot - Wikimedia Commons](https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Shutdown_button_red_wikimedia.svg/80px-Shutdown_button_red_wikimedia.svg.png)](https://commons.wikimedia.org/w/index.php?title=Special:Blockip&wpTarget=FVCBot&wpExpiry=indefinite&wpAnonOnly=0&wpHardBlock=1&wpAutoBlock=0&wpCreateAccount=0&wpReason=other&wpReason-other=Bot%20malfunctioning:%20)
