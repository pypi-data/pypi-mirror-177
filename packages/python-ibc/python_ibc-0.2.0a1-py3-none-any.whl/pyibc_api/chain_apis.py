'''
Dict of chains following the same schema so all my applications can use.

Used in / for:
- https://github.com/Reecepbcups/cosmos-validator-income-tracker (prices, queries, etc.)
- https://github.com/Reecepbcups/cosmos-governance-bot
- https://github.com/Reecepbcups/cosmos-balance-bot
'''

import requests
from dataclasses import dataclass

# NOTE: no /'s after any URL

# TODO: ping is now = ping-pub

PAGES = {
    "ping": {
        "gov_page": "gov/{id}",
        "staking_page": "staking/{valoper}",
    },
    "mintscan": {
        "gov_page": "proposals/{id}",
        "staking_page": "proposals/{valoper}",
    },
    "keplr": {
        "gov_page": "proposals/{id}",
        "staking_page": "validators/{valoper}", 
    },
    "dig": {
        "gov_page": "proposals/{id}",
        "staking_page": "https://app.digchain.org/staking", # no valoper view
    }
}

CUSTOM_EXPLORER_LINKS = {
    "dig": "https://app.digchain.org",    
}

REST_ENDPOINTS = {
    # DO NOT START WITH A /, this way we have to do in our f string
    "validator_info": "cosmos/staking/v1beta1/validators",
    "proposals": "cosmos/gov/v1beta1/proposals",
    "params": "cosmos/staking/v1beta1/params",
    "balances": "cosmos/bank/v1beta1/balances",
}

JUNO_REST_API = "https://rest-juno.ecostake.com/cosmwasm/wasm/v1/contract/"
DAOs = { # Juno DAO_DAO Chains here
    "raw": {
        "name": "RAW DAO",
        "proposals": f"{JUNO_REST_API}/juno1eqfqxc2ff6ywf8t278ls3h3rdk7urmawyrthagl6dyac29r7c5vqtu0zlf/smart/eyJsaXN0X3Byb3Bvc2FscyI6e319?encoding=base64",
        "vote": "https://www.rawdao.zone/vote",
        "twitter": "@raw_dao",
    },
    "rac": {
        "name": "Racøøn DAO",
        "proposals": f"{JUNO_REST_API}/juno16l0ymhpwfm63gdcjv8q32z7hqzv8g22spw6ul75l76s5lxtw4anscc5eek/smart/eyJsaXN0X3Byb3Bvc2FscyI6e319?encoding=base64",
        "vote": "https://daodao.zone/dao/juno1svduqrvcmzpl5g74q8rkm6rhcjnhch2yaagzu4ljuv2u9tf86ltqx9a54s/proposals/A",
        "twitter": "@RacoonSupply",
    }
}


# CHAIN_APIS = {
#     "dig": {
#         "denom": "udig",
#         "name": "Dig Chain",
#         "coingecko_id": "dig-chain",
#         "explorers": {
#             "ping": 'https://ping.pub/dig',
#         },
#         "rest_root": "https://api-1-dig.notional.ventures",
#         "rpc_root": "https://rpc.cosmos.directory/dig",
#         "twitter": "@dig_chain",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/dig/images/dig.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/dig/chain.json",
#     },

#     "juno": {
#         "denom": "ujuno",
#         "name": "Juno",
#         "coingecko_id": "juno-network",
#         "explorers": {
#             "ping": 'https://ping.pub/juno',
#             "mintscan": 'https://www.mintscan.io/juno',
#             "keplr": 'https://wallet.keplr.app/chains/juno',        
#         },
#         "rest_root": "https://rest.cosmos.directory/juno", # https://rest.cosmos.directory/juno
#         "rpc_root": "https://rpc.cosmos.directory/juno",
#         "twitter": "@JunoNetwork",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/juno/images/juno.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/juno/chain.json",
#     },    
#     "huahua": {
#         "denom": "uhuahua",
#         "name": "Chihuahua Chain",
#         "coingecko_id": "chihuahua-token",
#         "ibc_hash": "ibc/B9E0A1A524E98BB407D3CED8720EFEFD186002F90C1B1B7964811DD0CCC12228", # TODO: add to others as well, are these constant?
#         "explorers": {
#             "ping": 'https://ping.pub/chihuahua',
#             "mintscan": 'https://www.mintscan.io/chihuahua',
#         },
#         "rest_root": "https://rest.cosmos.directory/chihuahua", 
#         "rpc_root": "https://rpc.cosmos.directory/chihuahua",
#         "twitter": "@ChihuahuaChain",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/chihuahua/images/huahua.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/chihuahua/chain.json",
#     },    
#     "osmo": {
#         "denom": "uosmo",
#         "name": "Osmosis",
#         "coingecko_id": "osmosis",
#         "explorers": {
#             "ping": 'https://ping.pub/osmosis',
#             "mintscan": 'https://www.mintscan.io/osmosis',
#             "keplr": 'https://wallet.keplr.app/chains/osmosis',
#         },
#         "rest_root": "https://rest.cosmos.directory/osmosis", 
#         "rpc_root": "https://rpc.cosmos.directory/osmosis",
#         "twitter": "@OsmosisZone",
#         "logo": "https://info.osmosis.zone/static/media/logo.551f5780.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/osmosis/chain.json",
#     },    
#     "atom": {
#         "denom": "uatom",
#         "name": "Cosmos Hub",
#         "coingecko_id": "cosmos",
#         "explorers": {
#             "ping": 'https://ping.pub/cosmos',
#             "mintscan": 'https://www.mintscan.io/cosmos',
#             "keplr": 'https://wallet.keplr.app/chains/cosmos-hub'
#         },
#         "rest_root": "https://rest.cosmos.directory/cosmoshub",
#         "rpc_root": "https://rpc.cosmos.directory/cosmoshub",
#         "twitter": "@Cosmos",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/cosmoshub/images/atom.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/cosmoshub/chain.json",
#     },    
#     "akt": {
#         "denom": "uakt",
#         "name": "Akash",
#         "coingecko_id": "akash-network",
#         "explorers": {
#             "ping": 'https://ping.pub/akash-network',
#             "mintscan": 'https://www.mintscan.io/akash',
#             "keplr": 'https://wallet.keplr.app/chains/akash'
#         },
#         "rest_root": "https://rest.cosmos.directory/akash", 
#         "rpc_root": "https://rpc.cosmos.directory/akash",
#         "twitter": "@Akashnet_",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/akash/images/akt.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/akash/chain.json",
#     },    
#     "stars": {
#         "denom": "ustars",
#         "name": "Stargaze",
#         "coingecko_id": "stargaze",
#         "explorers": {
#             "ping": 'https://ping.pub/stargaze',
#             "mintscan": 'https://www.mintscan.io/stargaze',
#             "keplr": 'https://wallet.keplr.app/chains/stargaze'
#         },
#         "rest_root": "https://rest.cosmos.directory/stargaze", 
#         "rpc_root": "https://rpc.cosmos.directory/stargaze",
#         "twitter": "@StargazeZone",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/stargaze/images/stars.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/stargaze/chain.json",
#     },
#     "kava": {
#         "denom": "ukava",
#         "name": "Kava",
#         "coingecko_id": "kava",
#         "explorers": {
#             "ping": 'https://ping.pub/kava',
#             "mintscan": 'https://www.mintscan.io/kava',
#             "keplr": 'https://wallet.keplr.app/chains/kava'
#         },
#         "rest_root": "https://rest.cosmos.directory/kava", 
#         "rpc_root": "https://rpc.cosmos.directory/kava",
#         "twitter": "@kava_platform",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/kava/images/kava.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/kava/chain.json",
#     },
#     "like": {
#         "denom": "ulike",
#         "name": "Likecoin",
#         "coingecko_id": "likecoin",
#         "explorers": {
#             "ping": 'https://ping.pub/likecoin',
#         },
#         "rest_root": "https://rest.cosmos.directory/likecoin", 
#         "rpc_root": "https://rpc.cosmos.directory/likecoin",
#         "twitter": "@likecoin",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/likecoin/images/like.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/likecoin/chain.json",
#     },    
#     "xprt": {
#         "denom": "uxprt",
#         "name": "Persistence",
#         "coingecko_id": "persistence",
#         "explorers": {
#             "ping": 'https://ping.pub/persistence',
#             "mintscan": 'https://www.mintscan.io/persistence',
#             "keplr": 'https://wallet.keplr.app/chains/persistence',            
#         },
#         "rest_root": "https://rest.cosmos.directory/persistence", 
#         "rpc_root": "https://rpc.cosmos.directory/persistence",
#         "twitter": "@PersistenceOne",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/persistence/images/xprt.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/persistence/chain.json",
#     },    
#     "cmdx": {
#         "denom": "uxmdx",
#         "name": "Comdex",
#         "coingecko_id": "",
#         "explorers": {
#             "ping": 'https://ping.pub/comdex',
#             "mintscan": 'https://www.mintscan.io/comdex',            
#         },
#         "rest_root": "https://rest.cosmos.directory/comdex", 
#         "rpc_root": "https://rpc.cosmos.directory/comdex",
#         "twitter": "@ComdexOfficial",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/comdex/images/cmdx.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/comdex/chain.json",
#     },
#     'bcna': {
#         "denom": "ubcna",
#         "name": "BitCanna",
#         "coingecko_id": "bitcanna",
#         "explorers": {
#             "ping": "https://ping.pub/bitcanna",
#             "mintscan": "https://www.mintscan.io/bitcanna"
#         },
#         "rest_root": "https://rest.cosmos.directory/bitcanna",
#         "rpc_root": "https://rpc.cosmos.directory/bitcanna",
#         "twitter": "@BitCannaGlobal",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/bitcanna/images/bcna.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/bitcanna/chain.json"
#     },    
#     'btsg': {
#         "denom": "ubtsg",
#         "name": "BitSong",
#         "coingecko_id": "bitsong",
#         "explorers": {
#             "ping": "https://ping.pub/bitsong",
#             "mintscan": "https://www.mintscan.io/bitsong"
#         },
#         "rest_root": "https://rest.cosmos.directory/bitsong",
#         "rpc_root": "https://rpc.cosmos.directory/bitsong",
#         "twitter": "@BitSongOfficial",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/bitsong/images/btsg.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/bitsong/chain.json"
#     },    
#     'band': {
#         "denom": "uband",
#         "name": "Band Protocol",
#         "coingecko_id": "band-protocol",
#         "explorers": {
#             "ping": "https://ping.pub/band-protocol",
#             "mintscan": "https://www.mintscan.io/akash"
#         },
#         "rest_root": "https://rest.cosmos.directory/bandchain",
#         "rpc_root": "https://rpc.cosmos.directory/bandchain",
#         "twitter": "@BandProtocol",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/bandchain/images/band.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/bandchain/chain.json"
#     },    
#     'boot': {
#         "denom": "boot",
#         "name": "Bostrom",
#         "coingecko_id": "bostrom",
#         "explorers": {
#             "ping": "https://ping.pub/bostrom",
#             "keplr": "https://wallet.keplr.app/chains/bostrom"
#         },
#         "rest_root": "https://rest.cosmos.directory/bostrom",
#         "rpc_root": "https://rpc.cosmos.directory/bostrom",
#         "twitter": "@Cyber_devs",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/bostrom/images/boot.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/bostrom/chain.json"
#     },
#     'cheqd': {
#         "denom": "ncheq",
#         "name": "cheqd",
#         "coingecko_id": "cheqd-network",
#         "explorers": {
#             "ping": "https://ping.pub/cheqd"
#         },
#         "rest_root": "https://rest.cosmos.directory/cheqd",
#         "rpc_root": "https://rpc.cosmos.directory/cheqd",
#         "twitter": "@cheqd_io",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/cheqd/images/cheq.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/cheqd/chain.json"
#     },
#     'cro': {
#         "denom": "basecro",
#         "name": "Cronos",
#         "coingecko_id": "cronos",
#         "explorers": {
#             "ping": "https://ping.pub/crypto-com-chain",
#             "mintscan": "https://www.mintscan.io/crypto-org",
#             "keplr": "https://wallet.keplr.app/chains/crypto-org"
#         },
#         "rest_root": "https://rest.cosmos.directory/cronos",
#         "rpc_root": "https://rpc.cosmos.directory/cronos",
#         "twitter": "@cryptocom",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/cronos/images/cronos.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/cronos/chain.json"
#     },
#     'evmos': {
#         "denom": "uevmos",
#         "name": "Evmos",
#         "coingecko_id": "evmos",
#         "explorers": {
#             "ping": "https://ping.pub/evmos",
#             "mintscan": "https://www.mintscan.io/evmos",
#             "keplr": "https://wallet.keplr.app/chains/evmos"
#         },
#         "rest_root": "https://rest.cosmos.directory/evmos",
#         "rpc_root": "https://rpc.cosmos.directory/evmos",
#         "twitter": "@EvmosOrg",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/evmos/images/evmos.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/evmos/chain.json"
#     },
#     'fetch': {
#         "denom": "afet",
#         "name": "Fetch",
#         "coingecko_id": "fetch-ai",
#         "explorers": {
#             "ping": "https://ping.pub/fetchhub",
#             "mintscan": "https://www.mintscan.io/fetchai"
#         },
#         "rest_root": "https://rest-fetchhub.fetch.ai",
#         "rpc_root": "https://rpc.cosmos.directory/fetchhub",
#         "twitter": "@Fetch_ai",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/fetchhub/images/fet.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/fetchhub/chain.json"
#     },
#     'grav': {
#         "denom": "ugraviton",
#         "name": "Gravity Bridge",
#         "coingecko_id": "graviton",
#         "explorers": {
#             "ping": "https://ping.pub/gravity-bridge",
#             "mintscan": "https://www.mintscan.io/gravity-bridge",
#             "keplr": "https://wallet.keplr.app/chains/gravity-bridge"
#         },
#         "rest_root": "https://rest.cosmos.directory/gravitybridge",
#         "rpc_root": "https://rpc.cosmos.directory/gravitybridge",
#         "twitter": "@gravity_bridge",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/gravitybridge/images/grav.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/gravitybridge/chain.json"
#     },
#     'inj': {
#         "denom": "uinj",
#         "name": "Injective",
#         "coingecko_id": "injective-protocol",
#         "explorers": {
#             "ping": "https://ping.pub/injective",
#             "mintscan": "https://www.mintscan.io/injective"
#         },
#         "rest_root": "https://rest.cosmos.directory/injective",
#         "rpc_root": "https://rpc.cosmos.directory/injective",
#         "twitter": "@InjectiveLabs",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/injective/images/inj.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/injective/chain.json"
#     },
#     'iris': {
#         "denom": "uiris",
#         "name": "IRISnet",
#         "coingecko_id": "iris-network",
#         "explorers": {
#             "ping": "https://ping.pub/iris-network",
#             "mintscan": "https://www.mintscan.io/iris",
#             "keplr": "https://wallet.keplr.app/chains/irisnet"
#         },
#         "rest_root": "https://rest.cosmos.directory/irisnet",
#         "rpc_root": "https://rpc.cosmos.directory/irisnet",
#         "twitter": "@irisnetwork",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/irisnet/images/iris.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/irisnet/chain.json"
#     },
#     'iov': {
#         "denom": "uiov",
#         "name": "Starname",
#         "coingecko_id": "starname",
#         "explorers": {
#             "ping": "https://ping.pub/starname",
#             "mintscan": "https://www.mintscan.io/starname",
#             "keplr": "https://wallet.keplr.app/chains/starname"
#         },
#         "rest_root": "https://rest.cosmos.directory/starname",
#         "rpc_root": "https://rpc.cosmos.directory/starname",
#         "twitter": "@starname_me",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/starname/images/iov.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/starname/chain.json"
#     },
#     'lum': {
#         "denom": "ulum",
#         "name": "Lum Network",
#         "coingecko_id": "lum-network",
#         "explorers": {
#             "ping": "https://ping.pub/lum-network",
#             "mintscan": "https://www.mintscan.io/lum"
#         },
#         "rest_root": "https://rest.cosmos.directory/lumnetwork",
#         "rpc_root": "https://rpc.cosmos.directory/lumnetwork",
#         "twitter": "@lum_network",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/lumnetwork/images/lum.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/lumnetwork/chain.json"
#     },
#     'regen': {
#         "denom": "uregen",
#         "name": "Regen Network",
#         "coingecko_id": "regen",
#         "explorers": {
#             "ping": "https://ping.pub/regen",
#             "mintscan": "https://www.mintscan.io/regen",
#             "keplr": "https://wallet.keplr.app/chains/regen"
#         },
#         "rest_root": "https://rest.cosmos.directory/regen",
#         "rpc_root": "https://rpc.cosmos.directory/regen",
#         "twitter": "@regen_network",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/regen/images/regen.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/regen/chain.json"
#     },    
#     'hash': {
#         "denom": "nhash",
#         "name": "Provenance Blockchain",
#         "coingecko_id": "provenance-blockchain",
#         "explorers": {
#             "ping": "https://ping.pub/provenance",
#             "mintscan": "https://www.mintscan.io/provenance",
#         },
#         "rest_root": "https://rest.cosmos.directory/provenance",
#         "rpc_root": "https://rpc.cosmos.directory/provenance",
#         "twitter": "@provenancefdn",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/provenance/images/hash.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/provenance/chain.json"
#     },
#     'secret': {
#         "denom": "uscrt",
#         "name": "Secret Network",
#         "coingecko_id": "secret",
#         "explorers": {
#             "ping": "https://ping.pub/secret",
#             "mintscan": "https://www.mintscan.io/secret",
#             "keplr": "https://wallet.keplr.app/chains/secret-network"
#         },
#         "rest_root": "https://rest.cosmos.directory/secretnetwork",
#         "rpc_root": "https://rpc.cosmos.directory/secretnetwork",
#         "twitter": "@SecretNetwork",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/secretnetwork/images/scrt.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/secretnetwork/chain.json"
#     },    
#     'sent': {
#         "denom": "udvpn",
#         "name": "Sentinel",
#         "coingecko_id": "sentinel",
#         "explorers": {
#             "ping": "https://ping.pub/sentinel",
#             "mintscan": "https://www.mintscan.io/sentinel",
#             "keplr": "https://wallet.keplr.app/chains/sentinel"
#         },
#         "rest_root": "https://rest.cosmos.directory/sentinel",
#         "rpc_root": "https://rpc.cosmos.directory/sentinel",
#         "twitter": "@Sentinel_co",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/sentinel/images/dvpn.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/sentinel/chain.json"
#     },
#     'sif': {
#         "denom": "rowan",
#         "name": "Sifchain",
#         "coingecko_id": "sifchain",
#         "explorers": {
#             "ping": "https://ping.pub/sifchain",
#             "mintscan": "https://www.mintscan.io/sifchain",
#             "keplr": "https://wallet.keplr.app/chains/sifchain"
#         },
#         "rest_root": "https://api.sifchain.finance:443",
#         "rpc_root": "https://rpc.cosmos.directory/sifchain",
#         "twitter": "@sifchain",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/sifchain/images/rowan.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/sifchain/chain.json"
#     },
#     'kuji': {
#         "denom": "ukuji",
#         "name": "Kujira",
#         "coingecko_id": "kujira",
#         "explorers": {
#             "ping": "https://explorer.chaintools.tech/kujira",
#             # "kujira": "https://kujira.explorers.guru/" # TODO: add
#         },
#         "rest_root": "https://kujira-api.polkachu.com",
#         "rpc_root": "https://rpc.cosmos.directory/kujira",
#         "twitter": "@TeamKujira",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/kujira/images/kuji.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/kujira/chains.json"
#     },    
#     'terraC': {
#         "denom": "uluna",
#         "name": "Terra Classic",
#         "coingecko_id": "terra-luna",
#         "explorers": {
#             "ping": "https://ping.pub/terra-luna"
#         },
#         "rest_root": "https://rest.cosmos.directory/terra",
#         "rpc_root": "https://rpc.cosmos.directory/terra",
#         "twitter": "@terraC_money",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/terra/images/luna.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/terra/chains.json"
#     },
#     'terra': {
#         "denom": "uluna",
#         "name": "Terra2",
#         "coingecko_id": "terra-luna-2",
#         "explorers": {
#             "ping": "https://ping.pub/terra2"
#         },
#         "rest_root": "https://rest.cosmos.directory/terra2",
#         "rpc_root": "https://rpc.cosmos.directory/terra2",
#         "twitter": "@terra_money",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/terra2/images/luna.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/terra2/chain.json"
#     },
#     'pasg': {
#         "denom": "upasg",
#         "name": "Passage",
#         "explorers": {
#             "ping": 'https://ping.pub/passage',
#             "mintscan": 'https://www.mintscan.io/passage',  
#         },
#         "rest_root": "https://rest.cosmos.directory/passage", # https://rest.cosmos.directory/juno
#         "rpc_root": "https://rpc.cosmos.directory/passage",
#         "twitter": "@Passage3D",
#         "logo": "https://github.com/cosmos/chain-registry/raw/master/passage/images/pasg.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/passage/chain.json",
#     },
#     'umee': {
#         "denom": "uumee",
#         "name": "umee",
#         "coingecko_id": "umee",
#         "explorers": {
#             "ping": "https://ping.pub/umee",
#             "mintscan": "https://www.mintscan.io/umee",
#             "keplr": "https://wallet.keplr.app/chains/umee"
#         },
#         "rest_root": "https://rest.cosmos.directory/umee",
#         "rpc_root": "https://rpc.cosmos.directory/umee",
#         "twitter": "@Umee_CrossChain",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/umee/images/umee.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/umee/chain.json"
#     },
#     'canto': {
#         "denom": "ucanto",
#         "name": "Canto",
#         "coingecko_id": "canto",
#         "explorers": {
#             "ping": "https://ping.pub/canto"
#         },
#         "rest_root": "https://rest.cosmos.directory/canto",
#         "rpc_root": "https://rpc.cosmos.directory/canto",
#         "twitter": "@CantoPublic",
#         "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/canto/images/canto.png",
#         "chain-registry": "https://raw.githubusercontent.com/cosmos/chain-registry/master/canto/chain.json"
#     },
# }

COSMOS_DIR_URL = "https://chains.cosmos.directory/"
@dataclass
class ChainInfo:
    '''Object to track important data about a chain'''
    name: str
    denom: str
    coingecko_id: str
    bech32_prefix: str
    rest_root: str
    rpc_root: str
    twitter: str
    logo: str
    chain_registry: str
    explorers: dict
    def __init__(self) -> None:
        pass

# TODO: Ticker symbols -> CHAIN_APIs here for py gov bot. (ticker alises to the wallet prefix)
# ^ This should be handled now
CHAIN_APIS = {} # symbols -> chain info
CHAIN_APIS_WALLETS = {} # wallet prefix -> symbol (-> chain information from there)

info = requests.get(COSMOS_DIR_URL).json().get("chains", [])
chain: dict # annotation
for chain in info:
    symbol = str(chain.get("symbol", ""))
    if len(symbol) == 0: continue

    bech32 = chain.get("bech32_prefix", "")    

    explorers = {}
    for expl in chain.get("explorers", []):   
        name = expl.get("name", expl.get('kind', ""))
        url = expl.get("url", '') 
        if len(name) == 0 or len(url) == 0: continue
        explorers[name] = url
    
    apis = {}
    for api_type in chain.get("best_apis", []): # rest, rpc
        v = chain.get("best_apis", {}).get(api_type, [{}])
        apis[api_type] = v[0].get("address", "") if len(v) > 0 else ""        

    # TODO: Do this or just save the data as it is in cosmos dir?
    cinfo = ChainInfo()
    cinfo.name = chain.get("pretty_name", "")
    cinfo.denom = chain.get("denom", "")
    cinfo.coingecko_id = chain.get("coingecko_id", "")
    cinfo.bech32_prefix = bech32
    cinfo.explorers = explorers
    cinfo.rest_root = apis['rest']
    cinfo.rpc_root = apis['rpc']
    cinfo.twitter = chain.get("twitter", "")
    cinfo.logo = chain.get("image", "")
    cinfo.chain_registry = f"https://raw.githubusercontent.com/cosmos/chain-registry/master/{chain.get('path')}/chain.json"

    CHAIN_APIS[symbol.lower()] = cinfo
    CHAIN_APIS_WALLETS[bech32] = symbol.lower()
    continue

# Normal names / aliases here
aliases = {
    # alias: name in CHAIN_APIS symbol
    "terra-classic": "lunc",
    "dvpn": "sent",
    "provenance": "hash",
    "bostrom": "boot",
    "bandchain": "band",
    "bitsong": "btsg",
    "comdex":"cmdx",
    "persistence":"xprt",
    "stargaze": "stars",
    "akash": "akt",
    "cosmos": "atom",
    "osmosis": "osmo",
    "chihuahua": "huahua",
    "dig-chain": "dig",
    "passage": "pasg",
}

def get_chain(name):
    if name not in CHAIN_APIS.keys() and name not in aliases.keys():
        raise ValueError("Unknown chain: {}".format(name))
    
    if name in aliases.keys():
        # name was an alias, so we get the real name by calling this function on itself again
        return CHAIN_APIS[aliases[name]]

    if name in CHAIN_APIS_WALLETS.keys():
        return CHAIN_APIS[CHAIN_APIS_WALLETS[name]]
        
    value = CHAIN_APIS[name]
    return value

def get_all_chains():
    # get all CHAIN_APIS keys & aliases keys
    keys = list(CHAIN_APIS.keys())
    for alias in aliases.keys():
        keys.append(alias)
    return keys

def get_all_chains_by_wallet_prefix():
    return list(CHAIN_APIS_WALLETS.keys())
    
def get_endpoint(key) -> str:
    if key not in REST_ENDPOINTS.keys():
        print("Unknown endpoint: {}. Available: \n{}".format(key, REST_ENDPOINTS))        

    return REST_ENDPOINTS.get(key, "")

if __name__ == "__main__":
    print(get_chain('dig'))
