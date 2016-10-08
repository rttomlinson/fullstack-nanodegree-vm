-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
/* Make databases and schema for tournament program */
DROP DATABASE tournament;

CREATE DATABASE tournament;
\c tournament;

CREATE TABLE tournaments
(
tournamentid serial primary key
);

CREATE TABLE players
(
name text,
playerid serial PRIMARY KEY
);

CREATE TABLE matches
(
id SERIAL PRIMARY KEY,
tournament int references tournaments (tournamentid) ON DELETE CASCADE,
winner int references players (playerid) ON DELETE CASCADE,
loser int references players (playerid)
);

CREATE TABLE byes
(
tournament int references tournaments (tournamentid) ON DELETE CASCADE,
playerid int references players (playerid) ON DELETE CASCADE
);

CREATE TABLE tournamentplayers
(
	t_id int references tournaments (tournamentid) ON DELETE CASCADE,
	p_id int references players (playerid) ON DELETE CASCADE,
	CONSTRAINT pk_tplayers PRIMARY KEY (t_id, p_id) 
);

CREATE VIEW v_playeropponents AS
select tournament, playerid, winner as opponent FROM players join matches on playerid = loser
UNION ALL
SELECT tournament, playerid, loser as opponent FROM players JOIN matches on playerid = winner;

--Table of each player's total matches. Is used to make v_playerstandings table
CREATE VIEW v_totalmatches AS select t_id, p_id, count(winner) as matches from tournamentplayers
							left join matches on tournament = t_id and ((p_id = winner) or (p_id = loser)) GROUP BY t_id, p_id;


--Table of each player's total wins. Is used to make v_playerstandings table
CREATE VIEW v_totalwins AS select t_id, p_id, count(winner) as wins from tournamentplayers
							left join matches on tournament = t_id and p_id = winner GROUP BY t_id, p_id;

--Table of each player's total wins. Is used to make v_playerstandings table
CREATE VIEW v_opponentwins AS select v_playeropponents.tournament as tournament, v_playeropponents.playerid
							as playerid, sum(wins) as opponentwins FROM v_playeropponents JOIN v_totalwins
							ON tournament = t_id and opponent = p_id group by tournament, playerid;

--Table of player's standings
CREATE VIEW v_playerstandings AS select v_totalmatches.t_id as tournamentid, v_totalmatches.p_id as playid, players.name as name, v_totalwins.wins as wins, v_totalmatches.matches as matchesplayed,
								COALESCE(opponentwins, 0) as opponentwins from v_totalmatches left join v_totalwins on v_totalmatches.p_id = v_totalwins.p_id and v_totalmatches.t_id = v_totalwins.t_id
								join players on players.playerid = v_totalmatches.p_id LEFT JOIN v_opponentwins ON v_opponentwins.tournament = v_totalmatches.t_id and v_opponentwins.playerid = v_totalmatches.p_id ORDER BY wins DESC, opponentwins DESC;


