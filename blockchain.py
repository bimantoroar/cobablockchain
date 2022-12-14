import datetime as _dt
import hashlib as _hashlib
import json as _json
import random as rand

#kodingan milik
#https://github.com/sixfwa/blockchain-fastapi/

class Blockchain:
    def __init__(self):
        self.chain = list()
        self.reward = list()
        initial_block = self._create_block( #membuat block pertama
            pembayaran=0, proof=1, previous_hash="0", index=1,pemasukan=0,pengirim_pemasukan="genesis",nama="genesis",penerima="genesis"
        )
        self.chain.append(initial_block) #menanmbahkan block pertama ke blockchain

        
    def mine_block(self, nama:str,pemasukan:int,pengirim_pemasukan:str,pembayaran: int,penerima: str) -> dict:
        previous_block = self.get_previous_block()
        previous_proof = previous_block["proof"]
        reward = rand.randint(1,10)
        index = len(self.chain) + 1
        proof = self._proof_of_work(
            previous_proof=previous_proof, index=index
        )
        self.reward.append(reward)
        previous_hash = self._hash(block=previous_block)
        block = self._create_block(
            pembayaran=pembayaran, proof=proof, previous_hash=previous_hash, index=index,pemasukan=pemasukan,pengirim_pemasukan=pengirim_pemasukan,
            nama=nama,penerima=penerima
        )
        self.chain.append(block)
        return block

    def _create_block(
        self, pembayaran: int, proof: int, previous_hash: str,pemasukan: int,pengirim_pemasukan: str, index: int, nama:str,penerima:str
    ) -> dict:
        block = {
            "index": index,
            "timestamp": str(_dt.datetime.now()),
            "proof": proof,
            "previous_hash": previous_hash,
            "nama":nama,
            "pemasukan": pemasukan,
            "pengirim_pemasukan":pengirim_pemasukan,
            "pembayaran": pembayaran,
            "penerima":penerima,
            
        }

        return block

    def get_previous_block(self) -> dict:
        return self.chain[-1] #mengambil block sebelumnya

    def _to_digest(
        self, new_proof: int, previous_proof: int, index: int
    ) -> bytes:
        to_digest = str(new_proof ** 2 - previous_proof ** 2 + index) #algoritma matematika 
        return to_digest.encode()

    def _proof_of_work(self, previous_proof: str, index: int) -> int:
        new_proof = 1
        check_proof = False

        while not check_proof:
            to_digest = self._to_digest(new_proof, previous_proof, index)
            hash_operation = _hashlib.sha256(to_digest).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def _hash(self, block: dict) -> str:
        
        #Hash sebuah blok dan kembalikan hash kriptografi dari blok tersebut
        
        encoded_block = _json.dumps(block, sort_keys=True).encode()

        return _hashlib.sha256(encoded_block).hexdigest()
    
    def is_transaction_correct(self) -> str:
        block_index = 1
        
        for block_index in range(len(self.chain)):
            block = self.chain[block_index]
            # Check jika previous hash sama dengan hash block
            if block["pembayaran"] == block["pemasukan"]*0.05:
                res =  "Pembayaran Benar"
            else:
                res = "Pembayaran Tidak Benar"
            block_index += 1
            print(f'block {block_index}: {res}')

    def is_chain_valid(self) -> bool:
        previous_block = self.chain[0]
        block_index = 1

        while block_index < len(self.chain):
            block = self.chain[block_index]
            # Check jika previous hash sama dengan hash block
            if block["previous_hash"] != self._hash(previous_block):
                return False

            previous_block = block
            block_index += 1

        return True