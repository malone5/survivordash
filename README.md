# Suvivor Dash: a dashboad of survivor statistics

# DevLog: Tried reriretrieving data via google sheets but the sheets were not "published"
# to the web. they were only "Public". So i had to go the route of html table processing.

# DevLog: Contestant place order
# https://www.truedorktimes.com/s1/survivometer1.htm

# DevLog: Challenge: Not all pages have full contestant name info.
# And some seasons even have multiple people with the same name.
# Find a way to attach a nickname to a full name

# DevLog: Wikipedia has a well organized lists. perhaps we can match with wiki data.

# DevThoughts: Debating on if I should group on player name since some players appear more than once?
# I am leaning NO because we may want see statics on players that ONLY
# appear in multiple seasons. ALSO we can always normalize player records later once the data is loaded.
# Remember, our goal in this portion of ETL is to "get the data we want in". We can organize later.

# DevLog: Make sure Player Hashes are consistent. Write tests

# DevLog: Wrote first test. Using sub-package strategy

# DevLog: Need to find a way to get standard name in season 2. (missing hyperlink names)

# DevLog/Thoughts: Still determining how to distribute work. 
- wiki.py | data from survivor wiki
- truedorktimes.py | data from trudorktimes website
- stadardization.py | utility to help normalize names
    
# Name matching
- levenstien doesnt work because Laura B and Laura V are both Levenstien of 1? Or it doesnt matter cause we will have their last name.

- Names the cause problems NOTE: TDT = trudorktimes.com
- Ben Wade -> Coach (there is no similarity, we cant match on this) - SOVLED - nickname on both wiki + TDT
- Rob Mariano -> Boston Rob (Boston Rob nickname not in wiki files but used in TDT) SOLVES - contains
- Alexis van den Berghe -> Lex (TDT called him Lex and Alex) SOLVED - nickname and contains
- Ryan O and Ryan S in season7 () same fist name and no nickname SOVLED - initials
- Shii Ann Huang "Shii Ann" sovlved by inital match
- Season 27 - Both Lauras are mapped to Laura Morette. Triggered by 


# File issues
- season 16 has nicname "Kathy**" that breaks the name matchers
- season 33 has a key error 'name'. No Contestant label
- start with nickname, then firs an last initial.

# Final Goal of table structure
    - Seasons [Number | Title]
    - Players [Name | "Player Hash","Standard Name","Nickname","Name","Age","Hometown","Profession",]
    - SeasonPlayers ["SeasonPlayerId", "SeasonNumber", "Player Hash", "Finish Place","COPLETE STATS..."]
    - IndividualChallengeStats ["SeasonPlayerId", "Stats" ]


# DevLog: Finally down (ET)L in a good place. Need to clean it up and start github repository

# DevNotes: Create less files from boxscores etl.

# DevLog: boxscores are not uniform. somtimes we get ep 11 reward 2 etc

# DevLog: I think I need to tighten the scope. Small inconsistencies in trudorktimes.com is 
# causing a headache. Instead of powering through. We sould reel it back to maek it more digestible.

# DevNotes: Find a way to to break down and indivisual challenge

# DevLog: Lets start by only caring about challenge wins and voting blocks. 
# Look at: you win challenges, how many people participated, and what side of the vote were you on.

# Dev Note: have a .sql fiel that create the tables we need.
