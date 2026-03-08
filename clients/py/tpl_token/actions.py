from solders.pubkey import Pubkey
from solders.keypair import Keypair
from trezoa.rpc.async_api import AsyncClient
from trezoa.rpc.commitment import Confirmed
from trezoa.rpc.types import TxOpts
from solders.transaction import Transaction
import solders.system_program as sys

from tpl.token.constants import TOKEN_PROGRAM_ID
from tpl.token.async_client import AsyncToken
from tpl.token._layouts import MINT_LAYOUT
import tpl.token.instructions as tpl_token


OPTS = TxOpts(skip_confirmation=False, preflight_commitment=Confirmed)


async def create_associated_token_account(
    client: AsyncClient,
    payer: Keypair,
    owner: Pubkey,
    mint: Pubkey
) -> Pubkey:
    recent_blockhash = (await client.get_latest_blockhash()).value.blockhash
    ix = tpl_token.create_associated_token_account(
            payer=payer.pubkey(), owner=owner, mint=mint
        )
    txn = Transaction.new_signed_with_payer(
        [ix],
        signing_keypairs=[payer],
        payer=payer.pubkey(),
        recent_blockhash=recent_blockhash
    )
    await client.send_transaction(txn, opts=OPTS)
    return ix.accounts[1].pubkey


async def create_mint(client: AsyncClient, payer: Keypair, mint: Keypair, mint_authority: Pubkey):
    print(f"Creating pool token mint {mint.pubkey()}")
    mint_balance = await AsyncToken.get_min_balance_rent_for_exempt_for_mint(client)
    recent_blockhash = (await client.get_latest_blockhash()).value.blockhash
    txn = Transaction.new_signed_with_payer(
        [
            sys.create_account(
                sys.CreateAccountParams(
                    from_pubkey=payer.pubkey(),
                    to_pubkey=mint.pubkey(),
                    lamports=mint_balance,
                    space=MINT_LAYOUT.sizeof(),
                    owner=TOKEN_PROGRAM_ID,
                )
            ),
            tpl_token.initialize_mint(
                tpl_token.InitializeMintParams(
                    program_id=TOKEN_PROGRAM_ID,
                    mint=mint.pubkey(),
                    decimals=9,
                    mint_authority=mint_authority,
                    freeze_authority=None,
                )
            )
        ],
        payer=payer.pubkey(),
        recent_blockhash=recent_blockhash,
        signing_keypairs=[payer, mint],
    )
    await client.send_transaction(txn, opts=OPTS)
