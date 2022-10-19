import fastapi as _fastapi
import blockchain as _blockchain

blockchain = _blockchain.Blockchain()
app = _fastapi.FastAPI()


# endpoint to mine a block
@app.post("/mine_block/")
def mine_block(nama:str,pemasukan:int,pengirim_pemasukan:str,pembayaran: int,penerima: str):
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
    block = blockchain.mine_block(nama=nama,pemasukan=pemasukan,pengirim_pemasukan=pengirim_pemasukan,pembayaran=pembayaran,penerima=penerima)

    return block


# endpoint to return the blockchain
@app.get("/blockchain/")
def get_blockchain():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
    chain = blockchain.chain
    return chain

# endpoint to see if the chain is valid
@app.get("/validate/")
def is_blockchain_valid():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")

    return blockchain.is_chain_valid()

# endpoint to see if the chain is valid
@app.get("/transaction/")
def is_blockchain_valid():
    if not blockchain.is_transaction_correct():
        return _fastapi.HTTPException(status_code=400, detail="The transaction is invalid")

    return blockchain.is_transaction_correct()

# endpoint to return the last block
@app.get("/blockchain/last/")
def previous_block():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
        
    return blockchain.get_previous_block()