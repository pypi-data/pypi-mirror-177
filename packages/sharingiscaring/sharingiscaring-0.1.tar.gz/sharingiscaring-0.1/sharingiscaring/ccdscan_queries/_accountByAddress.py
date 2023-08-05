import requests
from rich.console import Console
console = Console()


class Mixin:
    def ql_get_info_by_accountId(self, value):
        query = "query {"
        query += f'accountByAddress (accountAddress: "{value}")'
        query += """
                    {
                    baker {
                        bakerId
                        state {
                            ... on ActiveBakerState {
                                nodeStatus {
                                    nodeName
                                }
                                pool {
                                    __typename
                                }
                            }
                        }
                    }
                } }
        """
        try:
            r = requests.post(self.graphql_url, json={'query': query})
            if r.status_code == 200:
                return r.json()['data']['accountByAddress']
            else:
                console.log(r.text)
        except Exception as e:
            console.log(query, e)
            return None

    def ql_get_ql_account_id(self, account_id):
        query = "query {"
        query += f'accountByAddress (accountAddress: "{account_id}")'
        query += """
                    {
                        id
                    }
                }
        """
        try:
            r = requests.post(self.graphql_url, json={'query': query})
            if r.status_code == 200:
                return r.json()['data']['accountByAddress']['id']
            else:
                console.log(r.text)
        except Exception as e:
            console.log(query, e)
            return None

    def ql_request_accountInfo_for_account_for_baker(self, account: str):
        query = "query {"
        query += f'accountByAddress (accountAddress: "{account}") '
        query += """
            { 
            address {
                asString
                }
            baker {
                state {
                    ... on ActiveBakerState {
                        pool {
                            openStatus
                            delegatorCount
                            delegatedStake
                            totalStake
                        }
                        pendingChange {
                            ... on PendingBakerReduceStake {
                                effectiveTime
                                newStakedAmount
                            }
                            ... on PendingBakerRemoval {
                                effectiveTime
                            }
                            __typename
                        }
                        stakedAmount
                        restakeEarnings
                    }
                }
            }
            amount
        }
        } # query
        """
        
        try:
            r = requests.post(self.graphql_url, json={'query': query})
            if r.status_code == 200:
                return r.json()['data']['accountByAddress']
            else:
                console.log(r.text)
       
        except Exception as e:
            console.log(query, e)
            return None

    def ql_request_accountInfo_for_account(self, account: str):
        query = "query {"
        query += f'accountByAddress (accountAddress: "{account}") '
        query += """
            { 
            createdAt
            id
            transactionCount
            amount
            address {
            asString
            }
            delegation {
                stakedAmount
                delegatorId
                restakeEarnings
                delegationTarget {
                    ... on BakerDelegationTarget {
                    __typename
                    bakerId
                    }
                    ... on PassiveDelegationTarget {
                    __typename
                    }
                }
            }
            baker {
                state {
                    ... on ActiveBakerState {
                        pool {  
                            delegatorCount
                            delegatedStake
                            totalStake
                            apy_30: apy(period: LAST30_DAYS) {
                            bakerApy
                            delegatorsApy
                            totalApy
                            }
                            apy_7: apy(period: LAST7_DAYS) {
                            bakerApy
                            delegatorsApy
                            totalApy
                            }
                            }
                        stakedAmount
                        restakeEarnings
                    }
                }
            }
            releaseSchedule {
                schedule {
                    nodes {
                        amount
                        timestamp
                        transaction {
                            transactionHash
                        }
                    }
                }
                totalAmount
            }
        }
        } # query
        """
        
        try:
            r = requests.post(self.graphql_url, json={'query': query})
            if r.status_code == 200:
                return r.json()['data']['accountByAddress']
            else:
                return None
       
        except Exception as e:
            console.log(query, e)
            return None

    def ql_request_transactions_for_lookup(self, accountLookup: bool, lookup_value: str, before: str = None, after: str = None):
        query = "query {"
        if accountLookup:
            query += f'accountByAddress (accountAddress: "{lookup_value}") '
        else: # blocklookup 
            query += f'blockByBlockHash (blockHash: "{lookup_value}") '

        query += '{ transactionCount '
        if before == 'first':
            accounts_str  =  f'transactions (first: {self.nodes_request_limit}) '
        
        elif before != 'null':
            accounts_str  =  f'transactions (last: {self.nodes_request_limit}, before: "{before}") '
        elif 'last' in after:
            accounts_str  =  f'transactions ({after}) ' 
        
        elif after != 'null':
            accounts_str  =  f'transactions (first: {self.nodes_request_limit}, after: "{after}") ' 
        else:
            accounts_str = f'transactions (first: {self.nodes_request_limit})'
        query += accounts_str + '{'
        query += self.pageInfo()
        if accountLookup:
            query += 'nodes { transaction {'
        else:
            query += 'nodes { '

        query += self.standard_tx_fields()
        query += self.ql_query_tx_events()

        if accountLookup:
            query += '} } }  } '
        else:
            query += '} }  } '
        
        try:
            r = requests.post(self.graphql_url, json={'query': query})
            if r.status_code == 200:
                if accountLookup:
                    return r.json()['data']['accountByAddress']['transactions']['nodes'], \
                        r.json()['data']['accountByAddress']['transactions']['pageInfo'], \
                        r.json()['data']['accountByAddress']['transactionCount'],                           
                else:
                    return r.json()['data']['blockByBlockHash']['transactions']['nodes'], \
                       r.json()['data']['blockByBlockHash']['transactions']['pageInfo'], \
                       r.json()['data']['blockByBlockHash']['transactionCount'],                           
            else:
                console.log(r.text)
       
        except Exception as e:
            console.log(query, e)
            return [], {}, 0

    def ql_request_account_rewards_for_lookup(self, lookup_value: str, before: str = None, after: str = None):
        LIMIT = self.nodes_request_limit
        LIMIT = 21
        query = "query {"
        query += f'  accountByAddress (accountAddress: "{lookup_value}") {{ '

        if before == 'first':
            accounts_str  =  f'rewards (first: {LIMIT}) '
        
        elif before != 'null':
            accounts_str  =  f'rewards (last: {LIMIT}, before: "{before}") '
        elif 'last' in after:
            accounts_str  =  f'rewards ({after}) ' 
        
        elif after != 'null':
            accounts_str  =  f'rewards (first: {LIMIT}, after: "{after}") ' 
        else:
            accounts_str = f'rewards (first: {LIMIT})'
        query += accounts_str + '{'
        query += self.pageInfo()
        query += """
            nodes {
                amount
                timestamp
                __typename
                rewardType
            }
            } } } 
        """

        try:
            r = requests.post(self.graphql_url, json={'query': query})
            if r.status_code == 200:
                return r.json()['data']['accountByAddress']['rewards']['nodes'], \
                    r.json()['data']['accountByAddress']['rewards']['pageInfo']
                                            
            else:
                console.log(r.text)
       
        except Exception as e:
            console.log(query, e)
            return None

    def ql_request_transactions_for_lookup_using_edges(self, lookup_value: str, before_cursor: str = None, after: str = None):
        query = "query {"
        query += f'accountByAddress (accountAddress: "{lookup_value}") '
        
        query += '{ '
        if not before_cursor:
            if not after:
                accounts_str  =  f'transactions (first: 50) ' 
            else:
                accounts_str  =  f'transactions (first: 50, after: "{after}") ' 
        else:
            accounts_str  =  f'transactions (last: 50, before: "{before_cursor}") ' 

        query += accounts_str + '{'
        query += self.pageInfo()
        query += 'edges { before_cursor: cursor  node { transaction {'
    
        query += self.standard_tx_fields()
        query += self.ql_query_tx_events()

        query += '} } }  } } '
        
        try:
            r = requests.post(self.graphql_url, json={'query': query})
            if r.status_code == 200:
                return r.json()['data']['accountByAddress']['transactions']['edges'], \
                    r.json()['data']['accountByAddress']['transactions']['pageInfo']                    
            else:
                console.log(r.text, query)
                return [], {}
       
        except Exception as e:
            console.log(query, e)
            return [], {}