# Dexpresso Python SDK 
A python SDK for better interactions with Dexpresso decentralized exchange (DEX).

## Quickstart

### Installation

Dexpresso-SDK can be installed (preferably in a virtualenv) using `pip` as follows:

`$ pip install dexpresso`

#### **Note**

If you run into problems during installation, you might have a broken environment. See the troubleshooting guide to setting up a clean environment.

### Using Dexpresso-py
Since Dexpresso is a decentralized exchange (DEX) working on multiple blockchains, this library/SDK depends on a connection to the blockchain fullnode that user wishes to place orders on. To eliminate any complexity while using this python SDK, we provide multiple **"pre-configured"** providers and standard token addresses on main supported networks. Therefore, you do not need to build and set up a working environment with the underlying blockchain (_i.e. Web3.py for ETH-like networks or Tronpy for Tron blockchain_). 

The following diagram shows two ways of using `Dexpresso.py`: 1) **Normal** flow, and 2) **Easy** flow.



                      ┌─────                                     ┌──────
                      │                                          │
                      │ ┌────────────┐                           │ ┌───────────┐
                      │ │ Configs.py │                           │ │ Client.py │
                      │ └────────────┘                           │ └───────────┘
          Offline  ───┤                              Online   ───┤
       (No Internet)  │ ┌──────────────────┐    (Internet Conn.) │ ┌───────────────┐
                      │ │ OfflineSigner.py │                     │ │ EasyClient.py │
                      │ └──────────────────┘                     │ └───────────────┘
                      │                                          │
                      └──────                                    └──────


                                  Normal Flow:                    Easy Flow:
                    ┌─────────────────────────────────────┐  ┌───────────────────┐
                    │                                     │  │                   │
                    │  ┌───────────┐ ┌──────────────────┐ │  │ ┌───────────────┐ │
                    │  │ Client.py │ │ OfflineSigner.py │ │  │ │ EasyClient.py │ │
                    │  └─────┬─────┘ └─────────┬────────┘ │  │ └───────┬───────┘ │
                    │        │                 │          │  │         │         │
                    │        │                 │          │  │         │         │
                    │  create order            │          │  │   create order    │
                    │        │  ────────────►  │          │  │         │         │
                    │        │                 │          │  │         │         │
                    │        │             Sign Order     │  │     sign order    │
                    │        │                 │          │  │         │         │
                    │        │  ◄────────────  │          │  │         │         │
                    │        │                 │          │  │   submit order    │
                    │  submit order            │          │  │         │         │
                    │        │                 │          │  │         │         │
                    │        │                 │          │  │         │         │
                    │                                     │  │                   │
                    └─────────────────────────────────────┘  └───────────────────┘



### Normal Flow:
This is the standard flow where many SDK users prefer to ensure their private assets (_private keys_) are always accessed **"Offline"**. To this end, we distinguished order creation process from signing the order. The `Client` class is responsible for `creating order` and `submitting` a signed order to the Dexpresso exchange. On the other hand, the `OfflineSigner` class takes user's private key to be able to sign created orders by `Client`, while being completely offline.
### Easy Flow:
In some cases, users may not be needing to completely separate and isolate creation and signature generation processes in their already developed projects. Therefore, we also provide an all-in-one class `EasyClient` that can handle entire process within one line of code. We note that the underlying functions and objects used to implement the `EasyClient` are the exact classes and methods from the **Normal Flow**, which ensure that not private asset of the user is in danger of being exposed outside of user's local device.



