# MetaMask Institutional SDK (Beta)

A Python library to create and submit Ethereum transactions to custodians connected with [MetaMask Institutional](https://metamask.io/institutions); the most trusted DeFi wallet and Web3 gateway for organizations.

> **BETA DISCLAIMER.** By using this library, you acknowledge the technology is still in Beta access and for internal testing purposes only. You are responsible for your use of the Beta access to Open Source SDK and ConsenSys is not responsible for any bugs, deficiencies or issues that may occur.

![Banner](https://image-server-xab.s3.eu-west-1.amazonaws.com/mmisdk-banner.png)

## Usage

Use this SDK to programmatically create Ethereum transactions, and submit them to custodians connected with MetaMask Institutional. Automate trading strategies on your wallets under custody, and still benefit from the institutional-grade security of your favorite qualified custodian and custody provider.

## Getting started

### Setting up

```bash
$ pip install mmisdk
```

```python
>>> from mmisdk import CustodianFactory

>>> factory = CustodianFactory()

>>> custodian = factory.create_for("qredo", "YOUR-TOKEN")
```

Use the custodian's Factory name param in the table below to instantiate a client for the right custodian.

| Custodian   | Supported | As of version | Factory name param |
| ----------- | --------- | ------------- | ------------------ |
| Bitgo       | ✅        | `0.3.0`       | `"bitgo"`          |
| Cactus      | ✅        | `0.2.0`       | `"cactus"`         |
| FPG         | ✅        | `0.4.0`       | `"fpg-prod"`       |
| Gnosis Safe | ✅        | `0.4.0`       | `"gnosis-safe"`    |
| Qredo       | ✅        | `0.2.0`       | `"qredo"`          |
| Saturn      | ✅        | `0.4.0`       | `"saturn"`         |

### Creating a transaction

```python
import os

from mmisdk import CustodianFactory

# Instantiate the factory
factory = CustodianFactory()

# Grab your token from the environment, or anywhere else
token = os.environ["MMISDK_TOKEN_QREDO"]

# Create the custodian, using the factory
custodian = factory.create_for("qredo", token)

# Build tx details
tx_params = {
    "from": "0x62468FD916bF27A3b76d3de2e5280e53078e13E1",
    "to": "0x62468FD916bF27A3b76d3de2e5280e53078e13E1",
    "value": "100000000000000000",  # in Wei
    "gas": "21000",
    "gasPrice": "1000",
    # "data": "0xsomething",
    # "type": "2"
    # "maxPriorityFeePerGas": "12321321",
    # "maxFeePerGas": "12321321",
}
qredo_extra_params = {
    "chainID": "3",
}

# Create the tx from details and send it to the custodian
transaction = custodian.create_transaction(tx_params, qredo_extra_params)
print(type(transaction))
# <class 'mmisdk.common.transaction.Transaction'>

print(transaction)
# id='2EzDJkLVIjmH6LZQ2W1T4wPcTtK'
# type='1'
# from_='0x62468FD916bF27A3b76d3de2e5280e53078e13E1'
# to='0x62468FD916bF27A3b76d3de2e5280e53078e13E1'
# value='100000000000000000'
# gas='21000'
# gasPrice='1000'
# maxPriorityFeePerGas=None
# maxFeePerGas=None
# nonce='0'
# data=''
# hash=''
# status=TransactionStatus(finished=False, submitted=False, signed=False, success=False, displayText='Created', reason='Unknown')
```

### Getting a transaction

```python
import os

from mmisdk import CustodianFactory

# Instantiate the factory
factory = CustodianFactory()

# Grab your token from the environment, or anywhere else
token = os.environ["MMISDK_TOKEN_CACTUS"]

# Create the custodian, using the factory
custodian = factory.create_for("cactus", token)

# Get the transaction
transaction = custodian.get_transaction("5CM05NCLMRD888888000800", 5)

print(type(transaction))
# <class 'mmisdk.common.transaction.Transaction'>

print(transaction)
# id='5CM05NCLMRD888888000800'
# type='1'
# from_='0xFA42B2eCf59abD6d6BD4BF07021D870E2FC0eF20'
# to=None
# value=None
# gas='133997'
# gasPrice='2151'
# maxPriorityFeePerGas=None
# maxFeePerGas=None
# nonce=''
# data=None
# hash=None
# status=TransactionStatus(finished=False, submitted=False, signed=False, success=False, displayText='Created', reason='Unknown')

```

## Examples

Continue on the page [Examples](https://consensys.gitlab.io/codefi/products/mmi/mmi-sdk-py/examples/) to see all code examples.
