SET search_path TO warehouse;

-- create tables
DROP TABLE IF EXISTS staging.challenge_stats;
CREATE TABLE staging.challenge_stats(
    playerid smallint,
    season smallint,
    mean_finish_pct numeric(5, 1), -- the average percent finished, 1 = won all cahllenges
    appearances smallint,
    score numeric(5, 2)
);


INSERT INTO staging.challenge_stats(playerid, season, mean_finish_pct, appearances, score)
SELECT p.id, s.season::NUMERIC, REPLACE(s.challenge_finish_avg, '%', '')::NUMERIC
    , s.challenge_appear::NUMERIC, s.challenge_score::NUMERIC
FROM lake.challenge_game_stats s
join staging.players p
on p.fullname=s.matched_name;


