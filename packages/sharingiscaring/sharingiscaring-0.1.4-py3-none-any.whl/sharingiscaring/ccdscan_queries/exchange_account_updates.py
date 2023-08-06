from rich.console import Console
console = Console()

import time

class Mixin:
    def ql_get_all_transactions_for_exchange_graphs_for_account(self, before_cursor, account_id):
        done = False
        after = None
        txs = []
        total_retrieved = 0
        while not done:
            this_batch, pageInfo = self.ql_request_transactions_for_lookup_using_edges(account_id, before_cursor=before_cursor, after=after)
            total_retrieved += len(this_batch)
            console.log(f"Retrieved {len(this_batch):,.0f} trades in this batch, totaling {total_retrieved:,.0f}.")
            if before_cursor:
                done = pageInfo['hasPreviousPage'] == False
                if not done:
                    before_cursor = pageInfo['startCursor']
            else:
                    
                done = pageInfo['hasNextPage'] == False
                if not done:
                    after = pageInfo['endCursor']
            txs.extend(this_batch)
            time.sleep(0.01)

        if len(txs) > 0:
            cursor_to_return = pageInfo['startCursor'] if before_cursor else txs[0]['before_cursor']
        else:
            cursor_to_return = before_cursor
        return txs, cursor_to_return

