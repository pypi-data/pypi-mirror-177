# Introduction

This is a library used to use `web3.py` on conflux-bridge(?). This library hacks the signing machanism of `web3.py`.

## Install

``` bash
pip install conflux-web3py-signer
```

## How to use

Import `conflux_we3py_signer` before import `web3`.

```python
import conflux_web3py_signer
import web3
```

## How

### Transaction Cast

When the modified `construct_sign_and_send_raw_middleware` is going to sign a transaction, it will convert an EIP-1559 transaction to conflux transaction following the rule:

* If `gasPrice` is missing, use `maxFeePerGas` as gas price.
* Fill `epochHeight` with `w3.eth.block_number`, which correspondes to `epoch_number` in conflux.
* Estimate the transaction and fill `storageLimit` from estimate result.

### Address Cast

EOA account addresses are all converted to begin with `0x1` and is encoded in checksum format
