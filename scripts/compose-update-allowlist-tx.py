#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import listdir
from os.path import join
from argparse import ArgumentParser
from enum import Enum
import json

runtime_descriptor_json = """
{
  "v": 2,
  "id": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/wQ=",
  "entity_id": "RDCyARTIdpiG75L9vVXAYIhRCToSrchZkv3JUW3Pji8=",
  "genesis": {
    "state_root": "F6lrOmNtgvH67OP3C6SkZrUi503CCT8j9jwFNYt0Ock=",
    "state": null,
    "storage_receipts": [{"public_key":"ovfRyilgOa65klzkJtwpSNnLqqstJFFJ5AZbAbtOWHg=","signature":"sDoGwrxXUZnJ/KUF2Fy0x4BwzPJ/Gcu03oSeLMLf1L6BHRp3p5ynbRdmyBmss44DWnq1UcfvaeduYD+nTMluDw=="}],
    "round": 44848
  },
  "kind": 1,
  "tee_hardware": 0,
  "versions": {
    "version": {}
  },
  "executor": {
    "group_size": 2,
    "group_backup_size": 0,
    "allowed_stragglers": 0,
    "round_timeout": 5,
    "max_messages": 32
  },
  "txn_scheduler": {
    "algorithm": "simple",
    "batch_flush_timeout": 1000000000,
    "max_batch_size": 10000,
    "max_batch_size_bytes": 16777216,
    "propose_batch_timeout": 5
  },
  "storage": {
    "group_size": 2,
    "min_write_replication": 2,
    "max_apply_write_log_entries": 100000,
    "max_apply_ops": 2,
    "checkpoint_interval": 1000,
    "checkpoint_num_kept": 5,
    "checkpoint_chunk_size": 16777216
  },
  "admission_policy": {
    "entity_whitelist": {
      "entities": {
      }
    }
  },
  "constraints": {
    "executor": {
      "backup-worker": {
        "min_pool_size": {
          "limit": 0
        }
      },
      "worker": {
        "min_pool_size": {
          "limit": 2
        }
      }
    },
    "storage": {
      "worker": {
        "min_pool_size": {
          "limit": 2
        }
      }
    }
  },
  "staking": {},
  "governance_model": "entity"
}
"""

class Network(Enum):
    mainnet = "mainnet"
    testnet = "testnet"

    def __str__(self):
        return self.value

def get_entity_ids(p):
    entity_id = []
    p = p.__str__();
    for f in listdir(p):
        if f == '.gitkeep':
            continue
        fullpath = join(p, f)
        entity = open(fullpath)
        entity_json = json.load(entity)
        entity_id.append(entity_json['OasisEntityID'])
    return entity_id

def print_tx(args):
    runtime_descriptor = json.loads(runtime_descriptor_json)
    for entity in get_entity_ids(args.network):
        runtime_descriptor['admission_policy']['entity_whitelist']['entities'][entity] = {}
    with open(args.runtime_descriptor, 'w') as f:
        f.write(json.dumps(runtime_descriptor, sort_keys=True, indent=2))

    output = f"""
cd {args.data_dir}
export GENESIS_JSON={args.genesis_json}
export NONCE={args.nonce}
export ENTITY_DIR={args.entity_dir}
export RUNTIME_DESCRIPTOR={args.runtime_descriptor}
../oasis-node-v21.1.2 registry runtime gen_register -y \\
    --transaction.fee.gas 10000 \\
    --transaction.fee.amount 0 \\
    --transaction.file register_runtime.tx \\
    --transaction.nonce $NONCE \\
    --genesis.file $GENESIS_JSON \\
    --signer.backend file \\
    --signer.dir $ENTITY_DIR \\
    --runtime.descriptor $RUNTIME_DESCRIPTOR
../oasis-node consensus submit_tx --transaction.file register_runtime.tx
rm -f register_runtime.tx
"""
    print(output)

def main():
    parser = ArgumentParser()
    parser.add_argument("network", type=Network, help="Choose network [mainnet|testnet]", choices=list(Network))
    parser.add_argument("nonce", help="Set tx nonce", type=int)
    parser.add_argument("entity_dir", help="Your entity dir", type=str)
    parser.add_argument("genesis_json", help="Your genesis json file", type=str)
    parser.add_argument("runtime_descriptor", help="Runtime descriptor file output path", type=str)
    parser.add_argument("data_dir", help="Your data dir", type=str)

    args = parser.parse_args()
    print_tx(args)

if __name__ == '__main__':
    main()
