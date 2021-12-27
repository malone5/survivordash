SET search_path TO warehouse;

-- create tables
DROP TABLE IF EXISTS staging.players;
CREATE TABLE staging.players(
    id SERIAL,
    fullname varchar(255) UNIQUE,
    nickname varchar(255),
    age smallint,
    hometown varchar(255),
    profession varchar(255)
);


INSERT INTO staging.players(fullname, nickname, age, hometown,profession)
SELECT standard_name, nick_name, cast(age as smallint), hometown, profession
FROM lake.season_players
ON CONFLICT (fullname) DO NOTHING;


