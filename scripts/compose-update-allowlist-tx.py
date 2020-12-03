#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import listdir
from os.path import join
from argparse import ArgumentParser
from enum import Enum
import json

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
        print(fullpath)
        entity = open(fullpath)
        entity_json = json.load(entity)
        print(entity_json)
        entity_id.append(entity_json['OasisEntityID'])
    return ','.join(entity_id)

def print_tx(args):
    output = f"""
    export ENTITY_DIR={args.entity_dir}
    export ENTITY_ID={get_entity_ids(args.network)}
    export GENESIS_JSON={args.genesis_json}
    export RUNTIME_ID={args.runtime_id}
    export NONCE={args.nonce}
    cd {args.data_dir}
    ../oasis-node registry runtime gen_register -y \\
      --transaction.fee.gas 10000 \\
      --transaction.fee.amount 0 \\
      --transaction.file register_runtime.tx \\
      --transaction.nonce $NONCE \\
      --genesis.file $GENESIS_JSON \\
      --signer.backend file \\
      --signer.dir $ENTITY_DIR \\
      --runtime.id $RUNTIME_ID \\
      --runtime.kind compute \\
      --runtime.executor.group_size 2 \\
      --runtime.storage.group_size 2 \\
      --runtime.storage.min_write_replication 2 \\
      --runtime.admission_policy entity-whitelist \\
      --runtime.admission_policy_entity_whitelist $ENTITY_ID \\
      --runtime.genesis.state ../etc/oasis_genesis_testing_21m.json \\
      --runtime.txn_scheduler.flush_timeout 1s \\
      --runtime.txn_scheduler.max_batch_size 10000 \\
      --runtime.txn_scheduler.max_batch_size_bytes 16mb \\
      --runtime.storage.checkpoint_chunk_size 16777216 \\
      --runtime.storage.checkpoint_interval 1000 \\
      --runtime.storage.checkpoint_num_kept 5
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
    parser.add_argument("runtime_id", help="Runtime id", type=str)
    parser.add_argument("data_dir", help="Your data dir", type=str)

    args = parser.parse_args()
    print_tx(args)

if __name__ == '__main__':
    main()
