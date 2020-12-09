# --------- imports ---------

import sqlite3
import requests
import json

# --------- classes ---------

class Application:
    """
    initialise a block chain for post and inquiry
    """

    def __init__(self):
        self.url1 = "http://localhost:8089/v1/"
        self.url2 = "http://localhost:8088/v1/"
        self.chain_dic = {}
        self.entry_dic = {}
        self.db = sqlite3.connect('record.db')

    """
    post user data to a Factom block on the server
    url - url of the specified server
    action - Factom action
    target - Factom element
    values - submitted data
    """

    def post(self, method, action, target, values):
        jdata = json.dumps(values)
        if method == "fctwallet":
            s = requests.post(self.url + action + "/" + target, jdata)
            return s.json()
        else:
            # response 200
            return requests.post(self.url2 + action + "/" + target, jdata)

    """
    private base api
    this function for inquiry data from bitmedi svr from factom svr.
    url - factom svr url
    action - factom action, compose-chain-submit etc.
    target - factom element, address, chain (name) etc.
    url + action + target gives the whole URL to aceess fcactom svr
    """

    def fct_inquiry(self, method, action, target):
        if method == "fctwallet":
            return requests.get(self.url + action + "/" + target).json()
        else:
            return requests.get(self.url2 + action + "/" + target)

    def local_validate(self):
        pass

    def init_chain(self, seq, entry_name):
        """
        generate a new chain with humman-read seq for token chain
        """
        values = {"ExtIDs": ["bitmedi", seq],
                  "Content": "NO." + seq + " chain of bitmedi"}
        s = self.fct_post("fctwallet", "compose-chain-submit", entry_name, values)
        self.bitmedi_chain_dic.setdefault(seq, s['ChainID'])
        self.fct_post("factomd", "commit-chain", "", s[u'ChainCommit'])
        self.fct_post("factomd", "reveal-chain", "", s[u'EntryReveal'])

    def post_record_to_fct(self, seq, entry_name, user_id, enc_content):
        """
        post record to factom with user_id, enc_content
        """
        values = {"ChainID": self.bitmedi_chain_dic[seq],
                  "ExtIDs": [user_id],
                  "Content": enc_content}
        s = self.fct_post("fctwallet", "compose-entry-submit", entry_name, values)
        entry_hashed = s[u'EntryCommit'][u'CommitEntryMsg'][14:78]
