#coding:utf-8

from lastfm import user_artists

def graphics():
    user1, user2 = 'panzersoldat', 'billionlights'
    user1artists = get_artists(user1)
    user2artists = get_artists(user2)
