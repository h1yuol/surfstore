from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from socketserver import ThreadingMixIn

import hashlib

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class threadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

store = dict()  # hashvalue -> binary
meta = dict()  # filename -> [version, [hashval1, hashval2, hashval3]]

# A simple ping, returns true
def ping():
    """A simple ping method"""
    print("Ping()")
    return True

# Gets a block, given a specific hash value
def getblock(h):
    """Gets a block"""
    print("GetBlock(" + h + ")")

    blockData = store[h]
    return blockData

# Puts a block
def putblock(b):
    """Puts a block"""
    print("PutBlock()")
    # b is a 'xml.client.Binary' object, not a bytes object
    h = hashlib.sha256(b.data).hexdigest()
    store[h] = b
    return True

# Given a list of blocks, return the subset that are on this server
def hasblocks(blocklist):
    """Determines which blocks are on this server"""
    print("HasBlocks()")

    return [h for h in blocklist if h in store]

# Retrieves the server's FileInfoMap
def getfileinfomap():
    """Gets the fileinfo map"""
    print("GetFileInfoMap()")

    result = {}

    # # file1.dat
    # file1info = []
    # file1info.append(3) // version

    # file1blocks = []
    # file1blocks.append("h1")
    # file1blocks.append("h2")
    # file1blocks.append("h3")

    # file1info.append(file1blocks)
    
    # result["file1.dat"] = file1info

    return meta

# Update a file's fileinfo entry
def updatefile(filename, version, blocklist):
    """Updates a file's fileinfo entry"""
    print("UpdateFile()")

    finfo = meta.get(filename, [0, []]) # Check if the initiation of a new file is correct!

    if finfo[0]+1 != version:
        return False
    
    finfo[0] = version
    finfo[1] = blocklist

    meta[filename] = finfo

    return True

# PROJECT 3 APIs below

# Queries whether this metadata store is a leader
# Note that this call should work even when the server is "crashed"
def isLeader():
    """Is this metadata store a leader?"""
    print("IsLeader()")
    return True

# "Crashes" this metadata store
# Until Restore() is called, the server should reply to all RPCs
# with an error (unless indicated otherwise), and shouldn't send
# RPCs to other servers
def crash():
    """Crashes this metadata store"""
    print("Crash()")
    return True

# "Restores" this metadata store, allowing it to start responding
# to and sending RPCs to other nodes
def restore():
    """Restores this metadata store"""
    print("Restore()")
    return True


# "IsCrashed" returns the status of this metadata node (crashed or not)
# This method should always work, even when the node is crashed
def isCrashed():
    """Returns whether this node is crashed or not"""
    print("IsCrashed()")
    return True

if __name__ == "__main__":
    try:
        print("Attempting to start XML-RPC Server...")
        server = threadedXMLRPCServer(('localhost', 8080), requestHandler=RequestHandler)
        server.register_introspection_functions()
        server.register_function(ping,"surfstore.ping")
        server.register_function(getblock,"surfstore.getblock")
        server.register_function(putblock,"surfstore.putblock")
        server.register_function(hasblocks,"surfstore.hasblocks")
        server.register_function(getfileinfomap,"surfstore.getfileinfomap")
        server.register_function(updatefile,"surfstore.updatefile")

        server.register_function(isLeader,"surfstore.isleader")
        server.register_function(crash,"surfstore.crash")
        server.register_function(restore,"surfstore.restore")
        server.register_function(isCrashed,"surfstore.iscrashed")
        print("Started successfully.")
        print("Accepting requests. (Halt program to stop.)")
        server.serve_forever()
    except Exception as e:
        print("Server: " + str(e))
