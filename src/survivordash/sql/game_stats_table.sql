SET search_path TO warehouse;


-- clean lake.game_stats
update lake.game_stats
set jury_votes_for=NULLIF(jury_votes_for, '')
, total_jurors=NULLIF(total_jurors, '')
, jury_vote_pct=NULLIF(jury_vote_pct, '')
, challenge_sat_out=NULLIF(challenge_sat_out, '')
, challenge_win_pct=NULLIF(challenge_win_pct, '');


update lake.game_stats
set challenge_win_pct=COALESCE(challenge_win_pct, "ChW.1", NULL);


update lake.game_stats
set jury_votes_for=NULLIF(jury_votes_for, '-')
, total_jurors=NULLIF(total_jurors, '-')
, jury_vote_pct=NULLIF(jury_vote_pct, '-')
, votes_for_bootee=NULLIF(votes_for_bootee, '-')
, votes_against_self=NULLIF(votes_against_self, '-')
, total_votes_cast=NULLIF(total_votes_cast, '-')
, tribal_council_appear=NULLIF(tribal_council_appear, '-')
, tribal_council_success_pct=NULLIF(tribal_council_success_pct, '-')
, weighted_tc_ratio=NULLIF(weighted_tc_ratio, '-');

update lake.game_stats
set votes_against_self=REPLACE(votes_against_self, '*', '')
, total_votes_cast=REPLACE(total_votes_cast, '*', '')
, tribal_council_appear=REPLACE(tribal_council_appear, '*', '');

-- create tables
DROP TABLE IF EXISTS staging.player_stats;
CREATE TABLE staging.player_stats(
    playerid smallint,
    season smallint,
    survivor_score numeric(5, 2),
    survivor_avg numeric(5, 2),
    challenge_wins numeric(5, 2),
    challenge_appear numeric(5, 2),
    challenge_win_pct numeric(5, 2),
    challenge_sat_out smallint,
    votes_for_bootee smallint,
    votes_against_self smallint,
    total_votes_cast smallint,
    tribal_council_appear smallint,
    tribal_council_success_pct numeric(5, 2),
    weighted_tc_ratio numeric(5, 2),
    jury_votes_for smallint,
    total_jurors smallint,
    jury_vote_pct numeric(5, 2)
);




INSERT INTO staging.player_stats(playerid, season, survivor_score, survivor_avg, 
    challenge_wins, challenge_appear, challenge_win_pct, challenge_sat_out, 
    votes_for_bootee, votes_against_self, total_votes_cast, tribal_council_appear, 
    tribal_council_success_pct, weighted_tc_ratio, jury_votes_for, total_jurors, jury_vote_pct)
SELECT p.id
    , s.season::NUMERIC
    , TO_NUMBER(s.survivor_score, 'S99D00')
    , s.survivor_avg::NUMERIC
    , s.challenge_wins::NUMERIC
    , s.challenge_appear::NUMERIC
    , s.challenge_win_pct::NUMERIC
    , s.challenge_sat_out::NUMERIC
    , s.votes_for_bootee::NUMERIC
    , s.votes_against_self::NUMERIC
    , s.total_votes_cast::NUMERIC
    , s.tribal_council_appear::NUMERIC
    , s.tribal_council_success_pct::NUMERIC
    , s.weighted_tc_ratio::NUMERIC
    , s.jury_votes_for::NUMERIC
    , s.total_jurors::NUMERIC
    , s.jury_vote_pct::NUMERIC
FROM lake.game_stats s
join staging.players p
on p.fullname=s.matched_name;


