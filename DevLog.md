### The following are notes/roadblocks/issues/milestones during development

Suvivor Dash: a dashboad of survivor statistics

**DevLog**: Tried reriretrieving data via google sheets but the sheets were not "published"
to the web. they were only "Public". So i had to go the route of html table processing.

**DevLog**: Contestant place order
https://www.truedorktimes.com/s1/survivometer1.htm

**DevLog**: Challenge: Not all pages have full contestant name info.
And some seasons even have multiple people with the same name.
Find a way to attach a nickname to a full name

**DevLog**: Wikipedia has a well organized lists. perhaps we can match with wiki data.

DevThoughts: Debating on if I should group on player name since some players appear more than once?
I am leaning NO because we may want see statics on players that ONLY
appear in multiple seasons. ALSO we can always normalize player records later once the data is loaded.
Remember, our goal in this portion of ETL is to "get the data we want in". We can organize later.

**DevLog**: Make sure Player Hashes are consistent. Write tests

**DevLog**: Wrote first test. Using sub-package strategy

**DevLog**: Need to find a way to get standard name in season 2. (missing hyperlink names)

**DevLog**: Still determining how to distribute work. 
- wiki.py | data from survivor wiki
- truedorktimes.py | data from trudorktimes website
- stadardization.py | utility to help normalize names

**DevLog**:
Name matching
- levenstien doesnt work because Laura B and Laura V are both Levenstien of 1? Or it doesnt matter cause we will have their last name.

- Names the cause problems NOTE: TDT = trudorktimes.com
- Ben Wade -> Coach (there is no similarity, we cant match on this) - SOVLED - nickname on both wiki + TDT
- Rob Mariano -> Boston Rob (Boston Rob nickname not in wiki files but used in TDT) SOLVES - contains
- Alexis van den Berghe -> Lex (TDT called him Lex and Alex) SOLVED - nickname and contains
- Ryan O and Ryan S in season7 () same fist name and no nickname SOVLED - initials
- Shii Ann Huang "Shii Ann" sovlved by inital match
- Season 27 - Both Lauras are mapped to Laura Morette. Triggered by 

**DevLog**:
File issues
- season 16 has nicname "Kathy**" that breaks the name matchers
- season 33 has a key error 'name'. No Contestant label
- start with nickname, then firs an last initial.

Final Goal of table structure
    - Seasons [Number | Title]
    - Players [Name | "Player Hash","Standard Name","Nickname","Name","Age","Hometown","Profession",]
    - SeasonPlayers ["SeasonPlayerId", "SeasonNumber", "Player Hash", "Finish Place","COPLETE STATS..."]
    - IndividualChallengeStats ["SeasonPlayerId", "Stats" ]


**DevLog**: Finally down (ET)L in a good place. Need to clean it up and start github repository

**DevNote**: Create less files from boxscores etl.

**DevLog**: boxscores are not uniform. somtimes we get ep 11 reward 2 etc

**DevLog**: I think I need to tighten the scope. Small inconsistencies in trudorktimes.com is 
causing a headache. Instead of powering through. We sould reel it back to maek it more digestible.

**DevNote**: Find a way to to break down and indivisual challenge

**DevLog**: Lets start by only caring about challenge wins and voting blocks. 
Look at: you win challenges, how many people participated, and what side of the vote were you on.

**DevNote**: have a .sql fiel that create the tables we need.

**DevLog**: perhaps we should be loading to the database -> making transforms there. BIG changes to come

**DevLog**: We are going to depricate our voting history dataset.
Reasons:
- Voting rounds and elimation is an unreliable variable
- Sometimes they draw rocks, re-vote which can be solved by taking the final result 
- However when both tribes vote off (like Episode 6 of Season 11: Guatemala) it can mess with programattic consistency
- For the sake of time we will forgo this data
- There may hope using >>> df.loc[:,~df.columns.duplicated(keep='last')] on episode, but not now.

**DevNote**: Episodes with a simultanious quit + council will only record the Quit, missing the council entirely :(

**DevNote**: For challenge_game_stats we will ignore "individual_challenge_share" for simplicity since some
season have one-off immunity challenges and thus do not create a pattern we can learn from.
We will focus on challenges-particicpated-in and win percentage as our main metric. 

Big discovery using the metbase api to instantiate our datasources in our metabase instance! Lets gooo

We have a race condition where our pipline finishes before Metabase is finmished initilizing

**DevLog**: Cool Findings querying the data:

-- winners vote percentage
select s.season, p.fullname, s.jury_vote_pct
from staging.player_stats s
join staging.players p
on s.playerid=p.id
where jury_vote_pct>.5;

-- winners
select win.season, p.fullname
from (
select season, playerid from player_stats
where jury_vote_pct>.5
) win
join players p
on win.playerid=p.id
order by win.season;


-- group seasons contenstant won
select string_agg(win.season::VARCHAR, ', '), p.fullname
from (
select season, playerid from player_stats
where jury_vote_pct>.5
) win
join players p
on win.playerid=p.id
group by p.fullname;



-- most voted for note : bad match on Lillian Morris (shoudl be Laura Moretz)
-- Laura Moretz(threat), Phillip Sheppard(goat), Ozzy Lusth(challenge beast),  
-- Baylor(strategic threat), Johnathan Penner(strategic)
select s.season, p.fullname, s.* 
from player_stats s
join players p
on s.playerid=p.id
where votes_against_self is not null
order by votes_against_self desc
limit 5;



**DevLog**: https://survivor.fandom.com/wiki/<survivro_name>
is a great source for stats that might be better than true dork times. Somethign to look at
