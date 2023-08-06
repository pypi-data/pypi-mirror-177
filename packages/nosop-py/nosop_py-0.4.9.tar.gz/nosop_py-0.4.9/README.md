# NosoP-Py

Set of classes and tools to communicate with a Noso wallet using NosoP(Noso Protocol).

The data that can be retrieved consist of:

- Node information
- Pool information

## Instruction for use

### Node Info

```py
from nosop_py import NosoNode

node = NosoNode('Node 1', '66.151.117.247', 8080)

node_info = node.get_info()

if node_info is not None:
    print(f'Node: "{node.name}" {node.host}:{node.port}')
    print('  Peers:', node_info.peers)
    print('  Block:', node_info.block)
    print('  Pending:', node_info.pending)
    print('  Sync Delta:', node_info.sync_delta)
    print('  Branch:', node_info.branch)
    print('  Version:', node_info.version)
    print('  Time:', node_info.time)
    print('  MN Hash:', node_info.mn_hash)
    print('  MN Count:', node_info.mn_count)
    print('  Block Hash:', node_info.last_block_hash)
    print('  Best Hash Diff:', node_info.best_hash_diff)
    print('  Block Time End:', node_info.last_block_time_end)
    print('  Best Hast Miner:', node_info.last_best_hash_miner)
    print('  Checks:', node_info.checks_count)
    print('  Block PoW:', node_info.last_block_pow)
    print('  Block Diff:', node_info.last_block_diff)
    print('  Summary:', node_info.summary)
    print('  GVTs:', node_info.gvts)
    print('  CFGs:', node_info.cfgs)
else:
    print('Something went wrong while retreiving the NodeInfo')
```

### Pool Info

```py
from nosop_py import NosoPool

pools = [
    {"name": 'GoneFishing', "host":'nosofish.xyz', "port":8082},
    {"name": 'rukzuk', "host":'pool.rukzuk.xyz', "port":8082},
    {"name": 'Estripa', "host":'nosopool.estripa.online', "port":8082},
    {"name": 'nosomn', "host":'pool.nosomn.com', "port":8082},
    {"name": 'RaviFj', "host":'159.196.1.198', "port":8082}
]

for pool in pools:
    pool_conn = NosoPool(pool["name"], pool["host"], pool["port"])

    pool_info = pool_conn.get_info()

    print(f'Pool: "{pool["name"]}" {pool["host"]}:{pool["port"]}')
    print(f'  Miners: {pool_info.miners_count}')
    print(f'  Last Block Rate: {pool_info.last_block_rate}')
    print(f'  Fee: {pool_info.pool_fee}')
    print(f'  Main Net Hash Rate: {pool_info.main_net_hash_rate}')
    print( '=======================================================')
```

### Pool Public

```py
from nosop_py import NosoPool

pools = [
    {"name": 'GoneFishing', "host":'nosofish.xyz', "port":8082},
    {"name": 'rukzuk', "host":'pool.rukzuk.xyz', "port":8082},
    {"name": 'Estripa', "host":'nosopool.estripa.online', "port":8082},
    {"name": 'nosomn', "host":'pool.nosomn.com', "port":8082},
    {"name": 'RaviFj', "host":'159.196.1.198', "port":8082}
]

for pool in pools:
    pool_conn = NosoPool(pool["name"], pool["host"], pool["port"])

    pool_public = pool_conn.get_public()

    print(f'Pool: "{pool["name"]}" {pool["host"]}:{pool["port"]}')
    print(f'  Version: {pool_public.version}')
    print(f'  IPs Count: {pool_public.ips_count}')
    print(f'  Max Shares: {pool_public.max_share}')
    print(f'  Pool Pay Interval: {pool_public.pool_pay_interval}')
    print(f'  Requester Range: {pool_public.requester_range}')
    print( '=======================================================')
```
