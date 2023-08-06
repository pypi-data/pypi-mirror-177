import io
import base58
import sha3
import json
from enum import Enum
from .node import ConcordiumNode
from rich.console import Console
console = Console()

class CNSActions(Enum):
    bid = "bid"
    setAddress= "setAddress"
    setData = "setData"
    transfer = "transfer"
    register = "register"
    createSubdomain = "createSubdomain"
    getTokenExpiry = "getTokenExpiry"

class CNSDomain:
    def __init__(self):
        self.function_calls = {} # event["receiveName"] : event["message"]
        self.transfer_to = None
        self.amount = None
        self.subdomain = None
        self.tokenId = None
        self.action = None
        self.action_message = None
        self.domain_name = None
        
    # Helper functions

    def bytes_from_hex_tokenID(self, hex):
        the_list = list(bytes.fromhex(hex[2:]))
        the_list.insert(0, 32)
        return the_list

    def write_binary_to_file(self, hex):
        newFileBytes = self.bytes_from_hex_tokenID(hex)
        newFileByteArray = bytearray(newFileBytes)
        newFile = open("token.bin", "wb")
        newFile.write(newFileByteArray)

    # Namehas, from name to tokenID
    def namehash(self, name: str, encoding  = 'utf-8'):
        '''ENS "namehash()" convention mapping of strings to bytes(32) hashes.
        
        Recursive function variant. Performs slightly better than the
        generator-based variant, but can't handle names with infinite (or
        extremely large) number of labels.

        :param name: name to hash, labels separated by dots
        :type name: str
        :returns: bytes(32)'''

        if name == '':
            return b'\x00' * 32
        else:
            label, _, remainder = name.partition('.')
            return sha3.keccak_256(self.namehash(remainder) +
                                sha3.keccak_256(bytes(label, encoding = encoding)).digest()).digest()

    # CNS utilities
    def read_domain_owner(self, bs):
        t = int.from_bytes(bs.read(1), byteorder='little')
        if t == 0:
            return (0, "Token doesn't exist.")
        elif t == 1:
            to_ = self.address(bs)
            return (1, to_)

    # CNS Defined terms
    def token_id(self, bs):
        n = int.from_bytes(bs.read(1), byteorder='little')
        return int.from_bytes(bs.read(n), byteorder='little')

    def token (self, bs):
        contract_index, contract_subindex = self.contract_address(bs)
        tokenID = self.token_id(bs)
        return contract_index, contract_subindex, tokenID

    def account_address(self, bs):
        addr = bs.read(32)
        return base58.b58encode_check(b'\x01' + addr).decode()

    def contract_address(self, bs):
            return int.from_bytes(bs.read(8), byteorder='little'), int.from_bytes(bs.read(8), byteorder='little')

    def royalty_length(self, bs):
            return int.from_bytes(bs.read(4))

    def royalty(self, bs):
        beneficiary_ = self.account_address(bs)
        percentage = self.percentage(bs)

    def address(self, bs):
        t = int.from_bytes(bs.read(1), byteorder='little')
        if t == 0:
            return self.account_address(bs)
        elif t == 1:
            return self.contract_address(bs)
        else:
            raise Exception('invalid type')

    def get_cns_domain_name(self, concordium_node: ConcordiumNode, hex):
        self.write_binary_to_file('0x' + hex)
        res = concordium_node.call_client_with(['contract', 'invoke', '7073', '--entrypoint', 'getTokenInfo', '--parameter-binary', 'token.bin'])
        try:
            by = json.loads(res.split()[-2])
            by = bytes(by[5:-8])
            domain_name = by.decode()
        except:
            domain_name = "Unable to determine..."
        self.domain_name = domain_name

    def get_domain_name_owner(self, concordium_node: ConcordiumNode, domain_name):
        console.log(f"get_domain_name_owner for {domain_name}")
        hex = concordium_node.cns_cache_by_name.get(domain_name, None)
        if not hex:
            bb = self.namehash(domain_name)
            hex = bytes.hex(bb)
            concordium_node.cns_cache_by_name[domain_name] = hex
            concordium_node.cns_cache_by_token_id[hex] = domain_name
            concordium_node.save_cns_cache()
            # console.log("write_to_file)")
        self.write_binary_to_file('0x' + hex)
        res = concordium_node.call_client_with(['contract', 'invoke', '7073', '--entrypoint', 'getTokenExpiry', '--parameter-binary', 'token.bin'])
        by = json.loads(res.split()[-2])

        byt = io.BytesIO(bytes(by))
        # console.log('read_domain_owner')
        (status, to) = self.read_domain_owner(byt)
        return (status, to)

    def decode_subdomain_from(self, hex):
        the_list = list(bytes.fromhex(hex[2:]))
        return bytes(the_list[3:]).decode()

    def decode_transfer_to_from(self, hex):
        all_data = self.transfer_parameter(io.BytesIO(bytes.fromhex(hex)))
        if len (all_data) > 0:
            if len (all_data[0]) > 3:
                return all_data[0][0], all_data[0][3] # tokenId, to_address
            else:
                return None
        else:
            return None

    def transfer_parameter(self, bs):
        n = int.from_bytes(bs.read(2), byteorder='little')
        return self.transfers(bs, n)

    def transfers(self, bs, n):
        return [self.transfer(bs) for _ in range(n)]

    def transfer(self, bs):
        id_ = self.token_id(bs)
        amount = self.token_amount(bs)
        from_ = self.address(bs)
        to = self.receiver(bs)
        data = self.additional_data(bs)
        return [id_, amount, from_, to, data]

    def token_id(self, bs):
        n = int.from_bytes(bs.read(1), byteorder='little')
        return bytes.hex(bs.read(n))

    def token_amount(self, bs):
        return int.from_bytes(bs.read(8), byteorder='little')
    
    def percentage(self, bs):
        return int.from_bytes(bs.read(8), byteorder='little')

    def receiver(self, bs):
        t = int.from_bytes(bs.read(1), byteorder='little')
        if t == 0:
            return self.account_address(bs)
        elif t == 1:
            return self.contract_address(bs), self.receive_hook_name(bs)
        else:
            raise Exception('invalid type')

    def receive_hook_name(self, bs):
        n = int.from_bytes(bs.read(2), byteorder='little')
        name = bs.read(n)
        return bytes.decode(name, 'ascii')

    def additional_data(self, bs):
        n = int.from_bytes(bs.read(2), byteorder='little')
        data = bs.read(n)
        return data

    # CNS Event
    def bidEvent(self, hexParameter):
        bs = io.BytesIO(bytes.fromhex(hexParameter))
        
        tag_ = int.from_bytes(bs.read(1), byteorder='little')
        contract_index, contract_subindex, token_id_ = self.token(bs)
        bidder_ = self.account_address(bs)
        amount_ = self.token_amount(bs)

        return [tag_, contract_index, contract_subindex, token_id_, bidder_, amount_]

    def cancelEvent(self, hexParameter):
        bs = io.BytesIO(bytes.fromhex(hexParameter))
        
        tag_ = int.from_bytes(bs.read(1), byteorder='little')
        contract_index, contract_subindex, token_id_ = self.token(bs)
        owner_ = self.account_address(bs)
        
        return [tag_, contract_index, contract_subindex, token_id_, owner_]

    def abortEvent(self, hexParameter):
        bs = io.BytesIO(bytes.fromhex(hexParameter))
        
        tag_ = int.from_bytes(bs.read(1), byteorder='little')
        contract_index, contract_subindex, token_id_ = self.token(bs)
        owner_ = self.account_address(bs)
        bidder_ = self.account_address(bs)
        amount_ = self.token_amount(bs)
        
        return [tag_, contract_index, contract_subindex, token_id_, owner_, bidder_, amount_]

    def finalizeEvent(self, hexParameter):
        bs = io.BytesIO(bytes.fromhex(hexParameter))
        
        tag_ = int.from_bytes(bs.read(1), byteorder='little')
        contract_index, contract_subindex, token_id_ = self.token(bs)
        seller_ = self.account_address(bs)
        winner_ = self.account_address(bs)
        price_ = self.token_amount(bs)
        seller_share = self.token_amount(bs)
        royalty_length_ = self.royalty_length(bs)
        royalties = [self.royalty(bs) for x in range(royalty_length_)] 
        
        return [tag_, contract_index, contract_subindex, token_id_, 
                seller_, winner_, price_, seller_share, royalty_length_, royalties]


    
