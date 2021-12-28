SET search_path TO warehouse;


-- clean
update lake.season_players
set hometown=TRIM(REPLACE(hometown, ', New York', ', NY'));

update lake.season_players
set hometown=TRIM(REPLACE(hometown, ', California', ', CA'));

update lake.season_players
set hometown=TRIM(REPLACE(hometown, ', D.C.', ', DC'));



-- create table
DROP TABLE IF EXISTS staging.players;
CREATE TABLE staging.players(
    id SERIAL,
    fullname varchar(255) UNIQUE,
    nickname varchar(255),
    age smallint,
    hometown_city varchar(255),
    hometown_state varchar(3),
    profession varchar(255)
);


INSERT INTO staging.players(fullname, nickname, age, hometown_city, hometown_state, profession)
SELECT standard_name, nick_name, cast(age as smallint)
    , TRIM(split_part(hometown, ',', 1)),  TRIM(split_part(hometown, ',', 2)), profession
FROM lake.season_players
ON CONFLICT (fullname) DO NOTHING;


