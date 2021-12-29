-- Table of winners derrived from staging
-- wherew season < 34 because I havent seent he rest and dont want spoilers :D
CREATE SCHEMA IF NOT EXISTS datamarts;

DROP TABLE IF EXISTS datamarts.winners;

CREATE TABLE datamarts.winners AS
SELECT winners.season, p.id as playerid, p.fullname, winners.jury_vote_pct
FROM staging.players p
JOIN (
    select distinct on (ps.season) ps.season, ps.playerid, ps.jury_vote_pct
    FROM (select * from player_stats where jury_vote_pct is not null) ps
    order by ps.season, ps.jury_vote_pct desc
    ) winners
on p.id=winners.playerid
where season < 34
order by winners.season;