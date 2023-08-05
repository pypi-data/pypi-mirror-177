import requests
from rich.console import Console
console = Console()

# from app.classes.Enums import TransactionTypeQL
from sharingiscaring.transaction import TransactionType

class Mixin:
    def this_a_tx(self, value):
        headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15'}
        a = requests.get(f'https://dashboard.mainnet.concordium.software/v1/transactionStatus/{value}', headers=headers, verify=False)
        return a.json() is not None
        
    def pageInfo(self):
        query = """
            pageInfo {
                hasPreviousPage
                startCursor
                endCursor
                hasNextPage
            }
                """
        return query

    def standard_tx_fields(self):
        query = """
        
            block {
                blockHash
                blockHeight
                blockSlotTime
                finalized
            }
            transactionType {
                __typename
                ...on AccountTransaction{
                    accountTransactionType
                }
                ... on CredentialDeploymentTransaction{
                    credentialDeploymentTransactionType
                }
                ... on UpdateTransaction {
                    updateTransactionType
                }
            }
            id
            transactionHash
            transactionIndex
            senderAccountAddress {
                asString
            }
            ccdCost
            energyCost
            transactionHash
        """
        return query

    def ql_query_tx_events (self):
        # event
        query = """
        result {
            ... on Rejected {
                __typename
                reason {
                __typename
                }
            }
            ... on Success {
                __typename
                events (first: 50) {
                    nodes {
                    __typename
                                    
        """
        for tr in TransactionType:
            query += tr.value

        query += """
                        }
                    }
                }
            }
        }
                """

        return query