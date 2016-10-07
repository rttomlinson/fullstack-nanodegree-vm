#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def pairings(tid, iterable):
    """Pairs players for next round of matches
        ARGS:
            iterable - player standings
        Returns list of tuples of pairs of players in the format (player1id, player1name, player2id, player2name)
    """
    rankings = iterable
    pairings = []
    if len(rankings) % 2 == 1: #Need to assign bye. Start with index -1
        negativeindexOfByeRecipient = byeAssignment(tid, rankings)
        byePlayerID = rankings.pop(negativeindexOfByeRecipient)[1]
        reportBye(tid, byePlayerID)
    while len(rankings) > 1:
        i = 1
        while not validPair(tid, 0, i):
            i += 1 #Find validPair of players for next match. And pop both
            if i >= len(rankings):
                i = 1
                break
        firstPlayer = rankings.pop(0)
        secondPlayer = rankings.pop(i-1)
        pairings.append((firstPlayer[1], firstPlayer[2], secondPlayer[1], secondPlayer[2]))
    return pairings


def validPair(tid, id1, id2):
    """Check to see if two players have played each other in a given tournament

        ARGS:
        id1 = player1 id
        id2 = player2 id

    Returns TRUE or FALSE depending on if players show up in matches table
    """
    db = connect()
    c = db.cursor()
    sql = """SELECT EXISTS(SELECT 1 FROM matches WHERE (winner=(%s) and loser=(%s)) or (winner=(%s) and loser=(%s)) and matches.tournament = (%s));"""
    c.execute(sql, (id1, id2, id2, id1, tid))
    bool_validPair = c.fetchone()[0]
    db.close()
    return bool_validPair

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM players;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT count(*) as num FROM players;")
    num_players = int((c.fetchone())[0])
    db.close()
    return num_players



def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).

    Returns unique playerID for that player, which can be used for registering for a tournament or reporting a match
    """
    db = connect()
    c = db.cursor()
    sqlplayer = "INSERT INTO players (name) values (%s) RETURNING playerid;"
    c.execute(sqlplayer, (name,))
    playerid = c.fetchone()[0]
    db.commit()
    db.close()
    return playerid

def addPlayertoTournament(tid, playerid):
    """Add player to tournamentplayers table.

    ARGS:
        tid = tournament id number
        playerid = player unique id number
    """
    db = connect()
    c = db.cursor()
    sqltournament = "INSERT INTO tournamentplayers (t_id, p_id) VALUES (%s, %s);"
    c.execute(sqltournament, (tid, playerid))
    db.commit()
    db.close()

def playerStandings(tid):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie. To get total matches we need a subquery and alias

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute("""SELECT * FROM v_playerstandingswithopponentwins WHERE tournamentid = (%s);""", (tid,))
    standings = c.fetchall()
    db.close()
    return standings

    #For total matches played - Make into view?

def reportMatch(tid, winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO matches (tournament, winner, loser) VALUES (%s, %s, %s);", (tid, winner, loser))
    db.commit()
    db.close()

def reportBye(tid, byeRecipient):
    """Records player's bye.

    Arg:
        byeRecipient: Player to recieve bye
    """
    db = connect()
    c = db.cursor()
    sql = """INSERT INTO byes (tournament, playerid) VALUES (%s, %s);""" #Insert into byes table
    c.execute(sql, (tid, byeRecipient))
    sql = """INSERT INTO matches (tournament, winner) VALUES (%s, %s);""" #Report bye has a win in matches table
    c.execute(sql, (tid, byeRecipient))
    db.commit()
    db.close()
 
def swissPairings(tid):
    """Returns a list of pairs of players for the next round of a match for a given tournament.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings(tid)
    s_pairings = pairings(tid, standings)
    return s_pairings

def hasBye(tid, playerid):
    """ Return whether or not player shows up in byes database for a given tournamentID

    ARGS:
        playerid - id of player to check
        tid = id of tournament

    Returns True or False
    """
    db = connect()
    c = db.cursor()
    sql = """SELECT EXISTS (SELECT 1 FROM byes WHERE playerid = (%s) and tournament = (%s));"""
    c.execute(sql, (playerid, tid))
    bool_Byes = c.fetchone()[0]
    db.close()
    return bool_Byes

def byeAssignment(tid, rankings):
    """Decides who to give bye to

        ARGS:
        tid - tournament id
        rankings - players in the tournament
    Returns index of players for bye assignment
    """
    byeRecipient = -1
    while abs(byeRecipient) <= len(rankings): 
        if hasBye(tid, rankings[byeRecipient][1]):
            byeRecipient -= 1
        else:
            return byeRecipient
    return -1

def makeTournament(tid):
    """Creates new tournament table

        ARGS:
        tid - tournament id desired by user
    """
    db = connect()
    c = db.cursor()
    sql = """INSERT INTO tournaments VALUES (%s);"""
    c.execute(sql, (tid,))
    db.commit()
    db.close()

def deleteTournaments():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM tournaments;")
    db.commit()
    db.close()
