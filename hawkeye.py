import pandas as pd
import pickle
from scapy.all import *
import multiprocessing as mp


"""
Packets have a field that specify what protocol is being used.

It's difficult to keep all of these number-name mappings in mind however, so this function maps the numbers to the human-readable names.
"""
def protocol_mapper(protocol_number):
    with open('./protocol.pkl', 'rb') as f:
        protocols = pickle.load(f)
    value = protocols.get(str(protocol_number))

    if value != None:
        return value
    else:
        return str(value)

"""
Takes a tcpdump and converts each package into a dict
"""
def dump_to_dict(filepath):
    print("Converting dump into list of dicts...")
    packets = rdpcap(filepath)
    pc = []
    for packet in packets:
        packet_dict = {}

        for layer in packet.layers():
            packet_dict.update(packet[layer].fields)

            pc.append(packet_dict)
    return pc

"""
Dataframes have some advantages when it comes to readability and interpretation compared to dicts.

This function takes a list of dicts and turns each dict into a row in a dataframe.

The dicts do not need to have the same keys, the final dataframe will have one column for each unique key in the list of dicts.
"""
def normalize_dicts(dictlist):
    keys = set()
    for d in dictlist:
        keys.update(d.keys())

    for key in keys:
        for d in dictlist:
            if key not in d.keys():
                d.update({key: '-'})

    return dictlist

def tcpdump_to_dataframe(filepath, p=True):
    print("Reading tcp into scapy...")
    pc = dump_to_dict(filepath)

    print("Normalizing dicts")
    npc = normalize_dicts(pc)

    print("Converting into dataframe...")
    df = pd.DataFrame.from_dict(npc)
    
    #Switch integer representation to actual name
    df['proto'] = df['proto'].map(protocol_mapper)
    return pc, npc, df














