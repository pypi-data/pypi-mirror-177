import cfx_account
import eth_account
import eth_account.account
import eth_account.signers.local

eth_account.account.Account = cfx_account.Account
eth_account.Account = cfx_account.Account
eth_account.signers.local.LocalAccount = cfx_account.LocalAccount

from conflux_web3py_signer.hacked_signing import construct_sign_and_send_raw_middleware

import web3.middleware
import web3.middleware.signing

web3.middleware.construct_sign_and_send_raw_middleware = construct_sign_and_send_raw_middleware # type: ignore
web3.middleware.signing.construct_sign_and_send_raw_middleware = construct_sign_and_send_raw_middleware
