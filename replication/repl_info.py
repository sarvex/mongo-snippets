
# this computes and prints how far behind a slave is from a master

from pymongo.connection import Connection
from pymongo import ASCENDING, DESCENDING

import sys

def compute_diff( slaveHost="localhost" , port=27017 ):
    slave = Connection( slaveHost , port , slave_okay=True )

    source = slave["local"]["sources"].find_one()
    lastSyncedSeconds = source["syncedTo"][1]
    print( source )

    components = source["host"].split(":")
    host = components[0]
    port = len(components) > 1 and components[1] or "27017"
    master = Connection(host, int(port))

    oplog = master["local"]["oplog.$main"]
    lastOp = oplog.find().limit(1).sort( "ts" , DESCENDING )[0]
    lastOpSeconds = lastOp["ts"][1]
    print( lastOp )

    diffSeconds = lastOpSeconds - lastSyncedSeconds
    print(f"slave is behind by: {diffSeconds} seconds")


if __name__ == "__main__":
    host = sys.argv[1] if len( sys.argv ) > 1 else "localhost"
    port = int( sys.argv[2] ) if len( sys.argv ) > 2 else 27017
    print( compute_diff( host , port ) )




