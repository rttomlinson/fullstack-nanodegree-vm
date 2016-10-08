#!/usr/bin/env python
#
# Test cases for tournament.py
# These tests are not exhaustive, but they should cover the majority of cases.
#
# If you do add any of the extra credit options, be sure to add/modify these test cases
# as appropriate to account for your module's added functionality.

from tournament import *

def testCode():
    deleteTournaments()
    deleteMatches()
    deletePlayers()
    makeTournament(1)
    makeTournament(2)
    tsid = registerPlayer("Twilight Sparkle")
    fsid = registerPlayer("Fluttershy")
    ajid = registerPlayer("Applejack")
    ppid = registerPlayer("Pinkie Pie")
    rtid = registerPlayer("Rarity")
    rdid = registerPlayer("Rainbow Dash")
    pcid = registerPlayer("Princess Celestia")
    plid = registerPlayer("Princess Luna")
    renzoid = registerPlayer("Renzo")
    addPlayertoTournament(1, tsid)
    addPlayertoTournament(1, fsid)
    addPlayertoTournament(1, ajid)
    addPlayertoTournament(1, ppid)
    addPlayertoTournament(1, rtid)
    addPlayertoTournament(1, rdid)
    addPlayertoTournament(1, pcid)
    addPlayertoTournament(1, plid)
    addPlayertoTournament(1, renzoid)
    addPlayertoTournament(2, tsid)
    addPlayertoTournament(2, fsid)
    addPlayertoTournament(2, ajid)
    addPlayertoTournament(2, ppid)
    addPlayertoTournament(2, rtid)
    addPlayertoTournament(2, rdid)
    addPlayertoTournament(2, pcid)
    addPlayertoTournament(2, plid)
    reportMatch(1, ajid, rtid)
    reportMatch(1, fsid, rdid)
    reportMatch(1, tsid, plid)
    reportMatch(1, pcid, ppid)
    reportMatch(2, tsid, ajid)
    reportMatch(2, rtid, fsid)
    reportMatch(2, plid, pcid)
    reportMatch(2, rdid, ppid)
    pairings = swissPairings(1)
    # Get the pairings and randomly assign the winner of one of them. Or I could just default to the first person in the pairing
    for i in range(0, 4):
    	for each in pairings:
    		reportMatch(1, each[0], each[2])
    	pairings = swissPairings(1)


def testCount():
    """
    Test for initial player count,
             player count after 1 and 2 players registered,
             player count after players deleted.
    """
    deleteTournaments()
    makeTournament(1)
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deletion, countPlayers should return zero.")
    print "1. countPlayers() returns 0 after initial deletePlayers() execution."
    chanid = registerPlayer("Chandra Nalaar")
    addPlayertoTournament(1, chanid)
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1. Got {c}".format(c=c))
    print "2. countPlayers() returns 1 after one player is registered."
    jaceid = registerPlayer("Jace Beleren")
    addPlayertoTournament(1, jaceid)
    c = countPlayers()
    if c != 2:
        raise ValueError(
            "After two players register, countPlayers() should be 2. Got {c}".format(c=c))
    print "3. countPlayers() returns 2 after two players are registered."
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError(
            "After deletion, countPlayers should return zero.")
    print "4. countPlayers() returns zero after registered players are deleted.\n5. Player records successfully deleted."

def testStandingsBeforeMatches():
    """
    Test to ensure players are properly represented in standings prior
    to any matches being reported.
    """
    tid = 1
    deleteTournaments()
    makeTournament(tid)
    deleteMatches()
    deletePlayers()
    mmid = registerPlayer("Melpomene Murray")
    rcid = registerPlayer("Randy Schwartz")
    addPlayertoTournament(1, mmid)
    addPlayertoTournament(1, rcid)
    standings = playerStandings(tid)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 6:
        raise ValueError("Each playerStandings row should have six columns.")
    [(t_id1, id1, name1, wins1, matches1, opwins1), (t_id2, id2, name2, wins2, matches2, opwins2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."

def testReportMatches():
    """
    Test that matches are reported properly.
    Test to confirm matches are deleted properly.
    """
    tid = 1
    deleteTournaments()
    makeTournament(tid)
    deleteMatches()
    deletePlayers()
    bwid = registerPlayer("Bruno Walton")
    bonid = registerPlayer("Boots O'Neal")
    cbid = registerPlayer("Cathy Burton")
    dgid = registerPlayer("Diane Grant")
    addPlayertoTournament(1,bwid)
    addPlayertoTournament(1,bonid)
    addPlayertoTournament(1,cbid)
    addPlayertoTournament(1,dgid)
    standings = playerStandings(tid)
    [id1, id2, id3, id4] = [row[1] for row in standings]
    reportMatch(tid, id1, id2)
    reportMatch(tid, id3, id4)
    standings = playerStandings(tid)
    for (t, i, n, w, m, ow) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."
    deleteMatches()
    standings = playerStandings(tid)
    if len(standings) != 4:
        raise ValueError("Match deletion should not change number of players in standings.")
    for (t, i, n, w, m, ow) in standings:
        if m != 0:
            raise ValueError("After deleting matches, players should have zero matches recorded.")
        if w != 0:
            raise ValueError("After deleting matches, players should have zero wins recorded.")
    print "8. After match deletion, player standings are properly reset.\n9. Matches are properly deleted."

def testPairings():
    """
    Test that pairings are generated properly both before and after match reporting.
    """
    tid = 1
    deleteTournaments()
    makeTournament(tid)
    deleteMatches()
    deletePlayers()
    tsid = registerPlayer("Twilight Sparkle")
    fsid = registerPlayer("Fluttershy")
    ajid = registerPlayer("Applejack")
    ppid = registerPlayer("Pinkie Pie")
    rtid = registerPlayer("Rarity")
    rdid = registerPlayer("Rainbow Dash")
    pcid = registerPlayer("Princess Celestia")
    plid = registerPlayer("Princess Luna")
    addPlayertoTournament(1, tsid)
    addPlayertoTournament(1, fsid)
    addPlayertoTournament(1, ajid)
    addPlayertoTournament(1, ppid)
    addPlayertoTournament(1, rtid)
    addPlayertoTournament(1, rdid)
    addPlayertoTournament(1, pcid)
    addPlayertoTournament(1, plid)
    standings = playerStandings(tid)
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[1] for row in standings]
    pairings = swissPairings(tid)
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    reportMatch(tid, id1, id2)
    reportMatch(tid, id3, id4)
    reportMatch(tid, id5, id6)
    reportMatch(tid, id7, id8)
    pairings = swissPairings(tid)
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4), (pid5, pname5, pid6, pname6), (pid7, pname7, pid8, pname8)] = pairings
    possible_pairs = set([frozenset([id1, id3]), frozenset([id1, id5]),
                          frozenset([id1, id7]), frozenset([id3, id5]),
                          frozenset([id3, id7]), frozenset([id5, id7]),
                          frozenset([id2, id4]), frozenset([id2, id6]),
                          frozenset([id2, id8]), frozenset([id4, id6]),
                          frozenset([id4, id8]), frozenset([id6, id8])
                          ])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4]), frozenset([pid5, pid6]), frozenset([pid7, pid8])])
    for pair in actual_pairs:
        if pair not in possible_pairs:
            raise ValueError(
                "After one match, players with one win should be paired.")
    print "10. After one match, players with one win are properly paired."


if __name__ == '__main__':
    testCode()
    #testCount()
    #testStandingsBeforeMatches()
    #testReportMatches()
    #testPairings()
    #print swissPairings()
    print "Success!  All tests pass!"
