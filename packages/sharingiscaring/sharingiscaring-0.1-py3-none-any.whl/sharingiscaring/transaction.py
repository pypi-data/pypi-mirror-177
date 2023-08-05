from enum import Enum
import dateutil
from .cns import CNSDomain, CNSActions
from .node import ConcordiumNode
from rich.console import Console
console = Console()

class TransactionClass (Enum):
    AccountTransaction='accountTransaction'
    CredentialDeploymentTransaction='credentialDeploymentTransaction'
    UpdateTransaction='updateTransaction'

class TransactionType(Enum):
    # https://github.com/Concordium/concordium-scan/blob/e95e8b2b191fefcf381ef4b4a1c918dd1f11ae05/frontend/src/queries/useTransactionQuery.ts
    AccountCreated = """
    ... on AccountCreated {
        accountAddress {
            asString
        }
    }
    """
    AmountAddedByDecryption = """
    ... on AmountAddedByDecryption {
        amount
        accountAddress {
            asString
        }
    }
    """
    BakerAdded="""
    ... on BakerAdded {
        bakerId
        restakeEarnings
        stakedAmount
        electionKey
        signKey
        aggregationKey
        accountAddress {
            asString
        }
    }
    """
    BakerKeysUpdated="""
    ... on BakerKeysUpdated {
        bakerId
        electionKey
        signKey
        aggregationKey
        accountAddress {
            asString
        }
    }
    """
    BakerRemoved="""
    ... on BakerRemoved {
        bakerId
        accountAddress {
            asString
        }
    }
    """
    BakerSetBakingRewardCommission="""
    ... on BakerSetBakingRewardCommission {
        bakerId
        bakingRewardCommission
        accountAddress {
            asString
        }
    }
    """
    BakerSetFinalizationRewardCommission="""
    ... on BakerSetFinalizationRewardCommission {
        bakerId
        finalizationRewardCommission
        accountAddress {
            asString
        }
    }
    """
    BakerSetMetadataURL="""
    ... on BakerSetMetadataURL {
        bakerId
        metadataUrl
        accountAddress {
            asString
        }
    }
    """
    BakerSetOpenStatus="""
    ... on BakerSetOpenStatus {
        bakerId
        openStatus
        accountAddress {
            asString
        }
    }
    """
    BakerSetRestakeEarnings="""
    ... on BakerSetRestakeEarnings {
        bakerId
        restakeEarnings
        accountAddress {
            asString
        }
    }    
    """
    BakerSetTransactionFeeCommission="""
    ... on BakerSetTransactionFeeCommission {
        bakerId
        transactionFeeCommission
        accountAddress {
            asString
        }
    }
    """
    BakerStakeDecreased="""
    ... on BakerStakeDecreased {
        bakerId
        newStakedAmount
        accountAddress {
            asString
        }
    }
    """
    BakerStakeIncreased="""
    ... on BakerStakeIncreased {
        bakerId
        newStakedAmount
        accountAddress {
            asString
        }
    }
    """
    ChainUpdateEnqueued="""
    ... on ChainUpdateEnqueued {
        effectiveImmediately
        effectiveTime
        payload {
            ... on AddAnonymityRevokerChainUpdatePayload {
                __typename
                arIdentity
                description
                name
                url
            }
            ... on AddIdentityProviderChainUpdatePayload {
                __typename
                description
                ipIdentity
                name
                url
            }
            ... on BakerStakeThresholdChainUpdatePayload {
                amount
                __typename
            }
            ... on CooldownParametersChainUpdatePayload {
                delegatorCooldown
                poolOwnerCooldown
                __typename
            }
            ... on ElectionDifficultyChainUpdatePayload {
                electionDifficulty
                __typename
            }
            ...on EuroPerEnergyChainUpdatePayload {
                exchangeRate {
                    numerator
                    denominator
                }
                __typename
            }
            ...on FoundationAccountChainUpdatePayload {
                accountAddress {
                    asString
                }
                __typename
            }
            ...on GasRewardsChainUpdatePayload {
                accountCreation
                baker
                chainUpdate
                finalizationProof
                __typename
            }
            ...on MicroCcdPerEuroChainUpdatePayload {
                exchangeRate {
                    denominator
                    numerator
                }
                __typename
            }
            ...on MintDistributionChainUpdatePayload {
                bakingReward
                finalizationReward
                mintPerSlot
                __typename
            }
            ...on ProtocolChainUpdatePayload {
                message
                specificationUrl
                specificationHash
                specificationAuxiliaryDataAsHex
                __typename
            }
            ...on TransactionFeeDistributionChainUpdatePayload {
                baker
                gasAccount
                __typename
            }
            ...on CooldownParametersChainUpdatePayload {
                delegatorCooldown
                poolOwnerCooldown
                __typename
            }
            ...on TimeParametersChainUpdatePayload {
                mintPerPayday
                rewardPeriodLength
                __typename
            }
            ...on MintDistributionV1ChainUpdatePayload {
                bakingReward
                finalizationReward
                __typename
            }
            ...on PoolParametersChainUpdatePayload {
                __typename
                bakingCommissionRange {
                    min
                    max
                }
                finalizationCommissionRange {
                    min
                    max
                }
                transactionCommissionRange {
                    min
                    max
                }
        }
    }
    }
    """
    ContractInitialized="""
    ... on ContractInitialized {
        amount
        contractAddress {
            __typename
            asString
            index
            subIndex
        }
        HEX:eventsAsHex {
            nodes 
        }
        initName
        moduleRef
    }
    """
    ContractInterrupted="""
    ... on ContractInterrupted {
        contractAddress {
            __typename
            asString
            index
            subIndex
        }
        HEX1:eventsAsHex
    }
    """
    ContractModuleDeployed="""
    ... on ContractModuleDeployed {
        moduleRef
        __typename
    }
    """
    ContractResumed="""
    ... on ContractResumed {
        contractAddress {
            __typename
            asString
            index
            subIndex
        }
        success
    }
    """
    ContractUpdated="""
    ... on ContractUpdated {
        amount
        contractAddress {
            __typename
            asString
            index
            subIndex
        }
        eventsAsHex {
            nodes 
        }
        instigator {
            __typename
            ... on AccountAddress {
                __typename
                asString
            }
            ... on ContractAddress {
                __typename
                asString
                index
                subIndex
            }
        }
        messageAsHex
        receiveName
    }
    """
    CredentialDeployed="""
    ... on CredentialDeployed {
        accountAddress {
            asString
        }
        regId
    }
    """
    CredentialKeysUpdated="""
    ... on CredentialKeysUpdated {
        credId
    }
    """
    CredentialsUpdated="""
    ... on CredentialsUpdated {
        accountAddress {
            asString
        }
        newCredIds
        newThreshold
        removedCredIds
    }
    """
    DataRegistered="""
    ... on DataRegistered {
        dataAsHex
    }
    """
    DelegationAdded="""
    ... on DelegationAdded {
        accountAddress {
            asString
        }
        delegatorId
    }
    """
    DelegationRemoved="""
    ... on DelegationRemoved {
        accountAddress {
            asString
        }
        delegatorId
    }
    """
    DelegationSetDelegationTarget="""
    ... on DelegationSetDelegationTarget {
        accountAddress {
            asString
        }
        delegationTarget {
            __typename
            ... on BakerDelegationTarget {
                bakerId
            }
        }
        delegatorId
    }
    """
    DelegationSetRestakeEarnings="""
    ... on DelegationSetRestakeEarnings {
        accountAddress {
            asString
        }
        delegatorId
        restakeEarnings
    }
    """
    DelegationStakeDecreased="""
    ... on DelegationStakeDecreased {
        accountAddress {
            asString
        }
        delegatorId
        newStakedAmount
    }
    """
    DelegationStakeIncreased="""
    ... on DelegationStakeIncreased {
        accountAddress {
            asString
        }
        delegatorId
        newStakedAmount
    }
    """
    EncryptedAmountsRemoved="""
    ... on EncryptedAmountsRemoved {
        accountAddress {
                asString
            }
        inputAmount
        newEncryptedAmount
        upToIndex
    }
    """
    EncryptedSelfAmountAdded="""
    ... on EncryptedSelfAmountAdded {
        accountAddress {
                asString
            }
        amount
        newEncryptedAmount
    }
    """
    NewEncryptedAmount="""
    ... on NewEncryptedAmount {
        accountAddress {
                asString
            }
        encryptedAmount
        newIndex
    }
    """
    TransferMemo="""
    ... on TransferMemo {
        decoded {
            text
        }
        rawHex
    }
    """
    Transferred = """
    ... on Transferred {
        amount
        from {
            ... on AccountAddress {
            __typename
            asString
            }
            ... on ContractAddress {
            __typename
            index
            subIndex
            }
            __typename
        }
        to {
            ... on AccountAddress {
            __typename
            asString
            }
            ... on ContractAddress {
            __typename
            index
            subIndex
            asString
            }
            __typename
        }
        __typename
        }
    """
    TransferredWithSchedule = """
    ... on TransferredWithSchedule {
        amountsSchedule (first: 50) {
            nodes {
                amount
                timestamp
            }
        }
        fromAccountAddress {
            asString
        }
            
        toAccountAddress {
            asString
        }
        totalAmount
        }
        
    """

class EventOpenStatusFromQLToNode(Enum):
    OPEN_FOR_ALL = 'openForAll'
    CLOSED_FOR_NEW = 'closedForNew'
    CLOSED_FOR_ALL = 'closedForAll'

class TransactionTypeFromQLToNode(Enum):
    AccountTransaction              = 'accountTransaction'
    CredentialDeploymentTransaction = 'credentialDeploymentTransaction'
    UpdateTransaction               = 'updateTransaction'

class TransactionContentsFromQLToNode(Enum):
    # AccountTransaction
    ADD_BAKER = 'addBaker'
    CONFIGURE_BAKER = 'configureBaker'
    CONFIGURE_DELEGATION = 'configureDelegation'
    DEPLOY_MODULE = 'deployModule'
    ENCRYPTED_TRANSFER = 'encryptedAmountTransfer'
    ENCRYPTED_TRANSFER_WITH_MEMO = 'encryptedAmountTransferWithMemo'
    INITIALIZE_SMART_CONTRACT_INSTANCE = 'initContract'
    REGISTER_DATA = 'registerData'
    REMOVE_BAKER = 'removeBaker'
    SIMPLE_TRANSFER = 'transfer'
    SIMPLE_TRANSFER_WITH_MEMO = 'transferWithMemo'
    TRANSFER_TO_ENCRYPTED = 'transferToEncrypted'
    TRANSFER_TO_PUBLIC = 'transferToPublic'
    TRANSFER_WITH_SCHEDULE = 'transferWithSchedule'
    TRANSFER_WITH_SCHEDULE_WITH_MEMO = 'transferWithScheduleAndMemo'
    UPDATE_BAKER_KEYS = 'updateBakerKeys'
    UPDATE_BAKER_RESTAKE_EARNINGS = 'updateBakerRestakeEarnings'
    UPDATE_BAKER_STAKE = 'updateBakerStake'
    UPDATE_CREDENTIAL_KEYS = 'updateCredentialKeys'
    UPDATE_CREDENTIALS = 'updateCredentials'
    UPDATE_SMART_CONTRACT_INSTANCE = 'update'
    UNKNOWN = '_unknown'

    # CredentialDeploymentTransaction
    NORMAL = 'normal'
    INITIAL = 'initial'

    # UpdateTransaction
    UPDATE_ADD_ANONYMITY_REVOKER = 'updateAddAnonymityRevoker'
    UPDATE_ADD_IDENTITY_PROVIDER = 'updateAddIdentityProvider'
    UPDATE_BAKER_STAKE_THRESHOLD = 'updateBakerStake'
    UPDATE_COOLDOWN_PARAMETERS = 'updateCooldownParameters'
    UPDATE_ELECTION_DIFFICULTY = 'updateElectionDifficulty'
    UPDATE_EURO_PER_ENERGY = 'updateEuroPerEnergy'
    UPDATE_FOUNDATION_ACCOUNT = 'updateFoundationAccount'
    UPDATE_GAS_REWARDS = 'updateGASRewards'
    UPDATE_LEVEL1_KEYS = 'updateLevel1Keys'
    UPDATE_LEVEL2_KEYS = 'updateLevel2Keys'
    UPDATE_MICRO_GTU_PER_EURO = 'updateMicroGTUPerEuro'
    UPDATE_MINT_DISTRIBUTION = 'updateMintDistribution'
    UPDATE_POOL_PARAMETERS = 'updatePoolParameters'
    UPDATE_PROTOCOL = 'updateProtocol'
    UPDATE_ROOT_KEYS = 'updateRootKeys'
    UPDATE_TIME_PARAMETERS = 'updateTimeParameters'
    UPDATE_TRANSACTION_FEE_DISTRIBUTION = 'updateTransactionFeeDistribution'

class Event:
    def __init__(self, _event):
        self._event = _event
        self.d = {}
        
    def determineAddress(self, address):
        a = {}

        if address['__typename'] == 'AccountAddress':
            a = {'type': 'AddressAccount', 'address': address['asString']}
        elif address['__typename'] == 'ContractAddress':
            a = {'type': 'AddressContract', 'address': {'index': address['index'], 'subindex': address['subIndex']} }
        return a 

    def translate_event_from_graphQL(self):
        e = self._event
        etype = e['__typename']
        self.d['tag'] = etype
        
        if etype == TransactionType.AccountCreated.name:
            self.d['contents'] = e['accountAddress']['asString']

        if etype == TransactionType.AmountAddedByDecryption.name:
            self.d['amount'] = int(e['amount'])
            self.d['account'] = e['accountAddress']['asString']
        
        elif etype == TransactionType.BakerSetOpenStatus.name:
            self.d['account'] = e['accountAddress']['asString']
            self.d['bakerId'] = e['bakerId']
            self.d['openStatus'] = EventOpenStatusFromQLToNode[e['openStatus']].value

        elif etype == TransactionType.BakerSetBakingRewardCommission.name:
            self.d['account'] = e['accountAddress']['asString']
            self.d['bakerId'] = e['bakerId']
            self.d['bakingRewardCommission'] = e['bakingRewardCommission']
        
        elif etype == TransactionType.BakerSetFinalizationRewardCommission.name:
            self.d['account'] = e['accountAddress']['asString']
            self.d['bakerId'] = e['bakerId']
            self.d['finalizationRewardCommission'] = e['finalizationRewardCommission']

        elif etype == TransactionType.BakerSetTransactionFeeCommission.name:
            self.d['account'] = e['accountAddress']['asString']
            self.d['bakerId'] = e['bakerId']
            self.d['transactionFeeCommission'] = e['transactionFeeCommission']

        elif etype == TransactionType.BakerSetMetadataURL.name:
            self.d['account'] = e['accountAddress']['asString']
            self.d['bakerId'] = e['bakerId']
            self.d['metadataUrl'] = e['metadataUrl']
        
        elif etype == TransactionType.DelegationAdded.name:
            self.d['account'] = e['accountAddress']['asString']
            self.d['delegatorId'] = e['delegatorId']
        
        elif etype == TransactionType.DelegationSetDelegationTarget.name:
            self.d['account'] = e['accountAddress']['asString']
            self.d['delegatorId'] = e['delegatorId']
            if e['delegationTarget']['__typename'] == 'PassiveDelegationTarget':
                self.d['delegationTarget'] = {'delegateType': 'Passive'}
            else:
                self.d['delegationTarget'] = {'delegateType': 'Baker', 'bakerId': e['delegationTarget']['bakerId']}
            
        elif etype == TransactionType.DelegationSetRestakeEarnings.name:
            self.d['account'] = e['accountAddress']['asString']
            self.d['delegatorId'] = e['delegatorId']
            self.d['restakeEarnings'] = e['restakeEarnings']
        
        elif etype == TransactionType.DelegationRemoved.name:
            self.d['account'] = e['accountAddress']['asString']
            self.d['delegatorId'] = e['delegatorId']
        
        elif etype == TransactionType.DelegationStakeDecreased.name:
            self.d['account'] = e['accountAddress']['asString']
            self.d['delegatorId'] = e['delegatorId']
            self.d['newStake'] = e['newStakedAmount']
        
        elif etype == TransactionType.DelegationStakeIncreased.name:
            self.d['account'] = e['accountAddress']['asString']
            self.d['delegatorId'] = e['delegatorId']
            self.d['newStake'] = e['newStakedAmount']
            
        elif etype == TransactionType.BakerAdded.name:
            self.d['account'] = e['accountAddress']['asString']
            self.d['bakerId'] = e['bakerId']
            self.d['aggregationKey'] = e['aggregationKey']
            self.d['electionKey'] = e['electionKey']
            self.d['restakeEarnings'] = e['restakeEarnings']
            self.d['signKey'] = e['signKey']
            self.d['stake'] = e['stakedAmount']
            
        elif etype == TransactionType.BakerKeysUpdated.name:
            self.d['account'] = e['accountAddress']['asString']
            self.d['bakerId'] = e['bakerId']
            self.d['aggregationKey'] = e['aggregationKey']
            self.d['electionKey'] = e['electionKey']
            self.d['signKey'] = e['signKey']
            
        elif etype == TransactionType.BakerRemoved.name:
            self.d['account'] = e['accountAddress']['asString']
            self.d['bakerId'] = e['bakerId']
            
        elif etype == TransactionType.BakerSetRestakeEarnings.name:
            self.d['account'] = e['accountAddress']['asString']
            self.d['bakerId'] = e['bakerId']
            self.d['restakeEarnings'] = e['restakeEarnings']
        
        elif etype == TransactionType.BakerStakeDecreased.name:
            self.d['account'] = e['accountAddress']['asString']
            self.d['bakerId'] = e['bakerId']
            self.d['newStake'] = e['newStakedAmount']
        
        elif etype == TransactionType.BakerStakeIncreased.name:
            self.d['account'] = e['accountAddress']['asString']
            self.d['bakerId'] = e['bakerId']
            self.d['newStake'] = e['newStakedAmount']

        elif etype == TransactionType.ChainUpdateEnqueued.name:
            self.d['effectiveTime'] = dateutil.parser.parse(e['effectiveTime']).timestamp()
            if e['payload']['__typename'] == 'BakerStakeThresholdChainUpdatePayload':
                self.d['payload'] = {}
                self.d['payload']['update'] = {'minimumThresholdForBaking': e['payload']['amount']}
                self.d['payload']['updateType'] = 'bakerStakeThreshold'

            elif e['payload']['__typename'] == 'ProtocolChainUpdatePayload':
                self.d['payload'] = {}
                self.d['payload']['update'] = {
                    'specificationUrl': e['payload']['specificationUrl'],
                    'message': e['payload']['message'],
                    'specificationHash': e['payload']['specificationHash'],
                    'specificationAuxiliaryData': e['payload']['specificationAuxiliaryDataAsHex']
                    }
                self.d['payload']['updateType'] = 'protocol'
            else:
                self.d['payload'] = e['payload']

        elif etype == TransactionType.ContractInitialized.name:
            self.d['address'] = {'index': e['contractAddress']['index'], 'subindex': e['contractAddress']['subIndex'] }
            self.d['amount'] = e['amount']
            self.d['contractVersion'] = 0 # note: not available in QL
            self.d['initName'] = e['initName']
            self.d['ref'] = e['moduleRef']
            self.d['events'] = e['HEX']['nodes']

        elif etype == TransactionType.ContractResumed.name:
            self.d['address'] = {'index': e['contractAddress']['index'], 'subindex': e['contractAddress']['subIndex']}
            self.d['success'] = e['success']

        elif etype == TransactionType.ContractInterrupted.name:
            self.d['address'] = {'index': e['contractAddress']['index'], 'subindex': e['contractAddress']['subIndex']}

        elif etype == TransactionType.ContractUpdated.name:
            self.d['address'] = {'index': e['contractAddress']['index'], 'subindex': e['contractAddress']['subIndex']}
            self.d['amount'] = e['amount']
            self.d['contractVersion'] = 0  # note: not available in QL
            self.d['instigator'] = self.determineAddress(e['instigator'])
            self.d['message'] = e['messageAsHex']
            self.d['receiveName'] = e['receiveName']
            self.d['events'] = e['eventsAsHex']['nodes']

        elif etype == TransactionType.ContractModuleDeployed.name:
            self.d['contents'] = e['moduleRef']
            
        elif etype == TransactionType.CredentialDeployed.name:
            self.d['account'] = e['accountAddress']['asString']
            self.d['regId'] = e['regId']
            

        elif etype == TransactionType.CredentialsUpdated.name:
            self.d['account'] = e['accountAddress']['asString']
            self.d['newCredIds'] = e['newCredIds']
            self.d['newThreshold'] = e['newThreshold']
            self.d['removedCredIds'] = e['removedCredIds']

        elif etype == TransactionType.DataRegistered.name:
            self.d['data'] = e['dataAsHex']
            
        elif etype == TransactionType.EncryptedAmountsRemoved.name:
            pass

        elif etype == TransactionType.NewEncryptedAmount.name:
            pass
        
        elif etype == TransactionType.TransferMemo.name:
            # note this is actually NOT the same as the node, as the node does NOT decode.
            self.d['memo'] = e['decoded']['text']
            
        elif etype == TransactionType.Transferred.name:
            self.d['amount'] = int(e['amount'])
            self.d['from'] = self.determineAddress(e['from'])
            self.d['to']   = self.determineAddress(e['to'])
            
        elif etype == TransactionType.TransferredWithSchedule.name:
            self.d['from'] = e['fromAccountAddress']['asString']
            self.d['to']   = e['toAccountAddress']['asString']
            self.d['amount'] = [(dateutil.parser.parse(x['timestamp']).timestamp()*1000, x['amount']) for x in e['amountsSchedule']['nodes']]
    
        return self.d

class Transaction:
    '''
    Canonical Transaction. Transactions from either the node or GraphQL will be morphed to fit this class
    Node language will be the go-to point, so graphQL terms are translated to fit the node. 
    '''

    def __init__(self, node):
        self.concordium_node = node
        
        
    def find_memo_and_amount(self):
        self.memo = None
        self.amount = None
        if ((self.contents == 'transferWithMemo') or (self.contents == 'Transferred')):
            for event in self.result['events']:
                if event['tag'] == TransactionType.TransferMemo.name:
                    self.memo = event['memo']
                if event['tag'] == TransactionType.Transferred.name:
                    self.amount = event['amount']

        return self

    def set_possible_cns_domain(self):
        self.cns_domain = CNSDomain()
        for event in self.result['events']:
            if event['tag'] == TransactionType.ContractUpdated.name:
                self.cns_domain.function_calls[event["receiveName"]] = event["message"]
                
                if event["receiveName"] == 'BictoryCnsNft.transfer':
                    self.cns_domain.action = CNSActions.transfer
                    self.cns_domain.tokenId, self.cns_domain.transfer_to = self.cns_domain.decode_transfer_to_from(event["message"])
                    
                if event["receiveName"] == 'BictoryCns.register':
                    self.cns_domain.amount = event['amount']
                    self.cns_domain.action = CNSActions.register
                    
                if event["receiveName"] == 'BictoryCns.createSubdomain':
                    self.cns_domain.action = CNSActions.createSubdomain
                    self.cns_domain.amount = event['amount']
                    self.cns_domain.subdomain = self.cns_domain.decode_subdomain_from(event["message"])
                    
                if event["receiveName"] == 'BictoryCns.setAddress':
                    self.cns_domain.action = CNSActions.setAddress
                    
                if event["receiveName"] == 'BictoryCns.setData':
                    self.cns_domain.action = CNSActions.setData
                    
                
                if event["receiveName"] == 'BictoryNftAuction.bid':
                    self.cns_domain.action = CNSActions.bid

                    if len (event['events']) > 0:
                        tag_, contract_index, contract_subindex, token_id_, bidder_, amount_ = self.cns_domain.bidEvent(event["events"][0])
                    else:
                        tag_, contract_index, contract_subindex, token_id_, bidder_, amount_ = self.cns_domain.bidEvent(event["message"])
                    self.cns_domain.tokenId = token_id_
                    self.cns_domain.amount = amount_  

                    if self.cns_domain.tokenId in self.concordium_node.cns_cache_by_token_id:
                        self.cns_domain.domain_name = self.concordium_node.cns_cache_by_token_id[self.cns_domain.tokenId]
                        console.log(f"Using cache for {self.cns_domain.domain_name}")
                    else:
                        self.cns_domain.get_cns_domain_name(self.concordium_node, self.cns_domain.tokenId)

                        self.concordium_node.cns_cache_by_token_id[self.cns_domain.tokenId] = self.cns_domain.domain_name
                        self.concordium_node.cns_cache_by_name[self.cns_domain.domain_name] = self.cns_domain.tokenId
                        self.concordium_node.save_cns_cache()
                        console.log(f"Saving cache for {self.cns_domain.domain_name}")
                    
                                      
                    
                
                if event["receiveName"] == 'BictoryCnsNft.getTokenExpiry':
                    self.cns_domain.action = CNSActions.getTokenExpiry
                    self.cns_domain.tokenId = event["message"][2:]

                    if self.cns_domain.tokenId in self.concordium_node.cns_cache_by_token_id:
                        self.cns_domain.domain_name = self.concordium_node.cns_cache_by_token_id[self.cns_domain.tokenId]
                        console.log(f"Using cache for {self.cns_domain.domain_name}")
                    else:
                        self.cns_domain.get_cns_domain_name(self.concordium_node, self.cns_domain.tokenId)
                        
                        self.concordium_node.cns_cache_by_token_id[self.cns_domain.tokenId] = self.cns_domain.domain_name
                        self.concordium_node.cns_cache_by_name[self.cns_domain.domain_name] = self.cns_domain.tokenId
                        self.concordium_node.save_cns_cache()
                        console.log(f"Saving cache for {self.cns_domain.domain_name}")
                    

    def init_from_node(self, t):
        # note that only blockHash, blockHeight, blockSlotTime, finalized is used
        self.block      = t['blockInfo']
        self.cost       = t['cost']
        self.energyCost = t['energyCost']
        self.hash       = t['hash']
        self.index      = t['index']
        self.result     = {'events': t['result']['events'], 'outcome': t['result']['outcome']}
        self.sender     = t['sender']
        self.type       = t['type']['type'] # accountTransaction
        self.contents   = t['type']['contents'] # transfer
        self.set_possible_cns_domain()
        self.concordium_node = None
        return self
       
    def define_type_and_contents_from_graphQL(self, t):
        _type       = t['transactionType']['__typename'] # AccountTransaction
        
        if _type == 'AccountTransaction':
            try:
                _contents = t['transactionType']['accountTransactionType']
            except:
                _contents = 'UNKNOWN'
        elif _type == 'CredentialDeploymentTransaction':
            try:
                _contents = t['transactionType']['credentialDeploymentTransactionType']
            except:
                _contents = 'UNKNOWN'
        elif _type == 'UpdateTransaction':
            try:
                _contents = t['transactionType']['updateTransactionType']
            except:
                _contents = 'UNKNOWN'
        else:
            _contents = 'UNKNOWN'

        # now translate to node language
        # console.log(f"{_type=}, {_contents=}")
        self.type       = TransactionTypeFromQLToNode[_type].value
        self.contents   = TransactionContentsFromQLToNode[_contents].value

    def translate_result_from_graphQL(self, t):
        if t['result']['__typename'] == 'Success':
            _outcome = 'success'
        elif t['result']['__typename'] == 'Rejected':
            _outcome = 'reject'
            _rejectReason = t["result"]["reason"]["__typename"]
        
        _events = []
        if 'events' in t['result']:
            for event in t['result']['events']['nodes']:
                e = Event(event).translate_event_from_graphQL()
                _events.append(e)

        if _outcome == 'success':
            return  {'events': _events, 'outcome': _outcome}
        else:
            return  {'events': _events, 'outcome': _outcome, 'rejectReason': _rejectReason}
        

    def init_from_graphQL(self, t):
        t['block']['blockSlotTime'] = dateutil.parser.parse(t['block']['blockSlotTime'])
        self.block      = t['block']
        self.cost       = t['ccdCost']
        self.energyCost = t['energyCost']
        self.hash       = t['transactionHash']
        self.index      = t['transactionIndex'] 
        self.sender     = t['senderAccountAddress']['asString'] if t['senderAccountAddress'] is not None else None
        self.define_type_and_contents_from_graphQL(t)
        self.result     = self.translate_result_from_graphQL(t)
        self.set_possible_cns_domain()
        self.concordium_node = None
        return self

