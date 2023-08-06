import json
import os
from dateutil.relativedelta import relativedelta
from .transaction import Transaction
from .node import ConcordiumNode
from .ccdscan import CCDScan
from .mongodb import MongoDB
from enum import Enum

class SubscriptionDetails(Enum):
    EXPLORER_CCD                = os.environ.get('EXPLORER_CCD', '3cunMsEt2M3o9Rwgs2pNdsCWZKB5MkhcVbQheFHrvjjcRLSoGP')
    SUBSCRIPTION_ONE_TIME_FEE   = os.environ.get('SUBSCRIPTION_ONE_TIME_FEE', 0)
    SUBSCRIPTION_MESSAGE_FEE    = os.environ.get('SUBSCRIPTION_MESSAGE_FEE', 1)
    SUBSCRIPTION_UNLIMITED      = os.environ.get('SUBSCRIPTION_UNLIMITED', 0)
    # note that is this is True, 'test_user' test will fail in its current form...
    SUBSCRIPTION_PLAN_ACTIVE    = os.environ.get('SUBSCRIPTION_PLAN_ACTIVE', False)
class TestClass:
    def __init__(self):
        pass

class Subscription:
    def __init__(self, subscription):
        self.raw                    = subscription
        if subscription:
            self.start_date             = subscription.get('start_date', None)
            self.payment_transactions   = subscription.get('payment_transactions', [])
            self.subscription_active    = subscription.get('subscription_active', False)
            self.bot_active             = subscription.get('bot_active', False)
            self.out_of_credits         = subscription.get('out_of_credits', True)
            self.unlimited              = subscription.get('unlimited', False)
            self.unlimited_end_date     = subscription.get('unlimited_end_date', None)
            # not stored, calculcated
            self.count_messages         = 0
            self.paid_amount            = 0

class User:
    def __init__(self):
        self.bakers_to_follow = []
        
    def add_user_from_telegram(self, user):
        self.first_name = user.first_name
        self.username = user.username
        self.chat_id = user.id
        self.language_code = user.language_code
        return self

        
    def read_user_from_git(self, user):
        self.bakers_to_follow               = user.get('bakers_to_follow', [])
        self.chat_id                        = user.get('chat_id', None)
        self.token                          = user.get('token', None)
        self.first_name                     = user.get('first_name', None)
        self.username                       = user.get('username', None)
        self.accounts_to_follow             = user.get('accounts_to_follow', [])
        self.labels                         = user.get('labels', None)
        self.transactions_downloaded        = user.get('transactions_downloaded', {})
        self.transaction_limit_notifier     = user.get('transaction_limit_notifier', -1)
        self.smart_init                     = user.get('smart_init', False)
        self.smart_update                   = user.get('smart_update', False)
        self.cns_domain                     = user.get('cns_domain', False)
        self.nodes                          = user.get('nodes', {})
        self.subscription                   = Subscription(user.get('subscription', None))
        return self

    def perform_subscription_logic(self, 
        ccdscan: CCDScan, 
        node: ConcordiumNode, 
        mongodb: MongoDB
        ):
        
        payment_memo = 'coffee'
        
        # get transactions sent to EXPLORER.CCD
        explorer_ccd_transactions, _ = ccdscan.ql_get_all_transactions_for_exchange_graphs_for_account(None, SubscriptionDetails.EXPLORER_CCD.value)
        explorer_ccd_transactions = [x['node']['transaction'] for x in explorer_ccd_transactions]
        
        # check if the right memo is set, if so, count towards user.
        payment_txs = []
        paid_amount = 0
        SUBSCRIPTION_ONE_TIME_FEE_set = False
        for tx in explorer_ccd_transactions:
            concordium_tx = Transaction(node).init_from_graphQL(tx).find_memo_and_amount()
            if concordium_tx.memo:
                if payment_memo in concordium_tx.memo:
                    paid_amount += concordium_tx.amount/1_000_000
                    # Has the user paid the one time fee? If so, record the subscription start date
                    if not SUBSCRIPTION_ONE_TIME_FEE_set:
                        self.subscription.subscription_active = paid_amount >= SubscriptionDetails.SUBSCRIPTION_ONE_TIME_FEE.value
                        
                        if self.subscription.subscription_active:
                            SUBSCRIPTION_ONE_TIME_FEE_set = True
                            self.subscription.start_date = concordium_tx.block['blockSlotTime']

                    # Has the user paid enough for unlimited? If so, record the unlimited end date
                    self.subscription.unlimited = paid_amount >= SubscriptionDetails.SUBSCRIPTION_UNLIMITED.value
                    if self.subscription.unlimited:
                        self.subscription.unlimited_end_date = concordium_tx.block['blockSlotTime'] + relativedelta(years=1)
                    payment_txs.append(concordium_tx)

        self.subscription.payment_transactions = payment_txs
        self.subscription.paid_amount = paid_amount

        # # get count of messages sent to this user
        pipeline = mongodb.get_bot_messages_for_user(self)
        result = list(mongodb.collection_messages.aggregate(pipeline))
        
        self.subscription.count_messages = 0
        if len (result) > 0:
            if 'count_messages' in result[0]:
                self.subscription.count_messages = result[0]['count_messages']


        if self.subscription.subscription_active:
            if (self.subscription.paid_amount - SubscriptionDetails.SUBSCRIPTION_ONE_TIME_FEE.value - self.subscription.count_messages) > 0:
                self.subscription.bot_active = True
            else:
                self.subscription.bot_active = False

        # needed for parameterized test 'test_user'. 
        if not SubscriptionDetails.SUBSCRIPTION_PLAN_ACTIVE.value:
            self.subscription.bot_active = True

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)