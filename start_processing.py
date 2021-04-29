import os
import argparse
from time import time
from astropy.table import Table
from rta_dq_lib.api.DQLib import DQLib

import matplotlib.pyplot as plt

def get_data(filename):
    table = Table.read(filename, format="fits")
    table = table.as_array()
    return table


if __name__=='__main__':

    os.environ["DQLIBCONF"] = "./configurations"
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", required=True, help="The path to a folder containing the xml configuration files for the rta-dq-lib")
    args = parser.parse_args()

    table = get_data(args.filename)
    columns = table.dtype.names
    
    agileDqPipe = DQLib.get_dq_pipeline("agile-pipeline-1", "obs_1", debug_lvl = 1)

    time1 = time()
    output = agileDqPipe.process(table, "run_1")
    print(f"Took {time()-time1} seconds")

    print(output)
    print(output.events[0])

    #plt.plot(output.events[0]["PKTSEQCN_samples"])
    #plt.savefig("./test_temporal.png")

    plt.bar(x=list(range(0, len(output.events[0]["PKTSEQCN_distribution"]))), height=output.events[0]["PKTSEQCN_distribution"])
    plt.savefig("./test_distribution.png")


    from fast_histogram import histogram1d
    start = time()
    data = histogram1d(table["PKTSEQCN"], range=[0, 100], bins=10)
    print("fasthistogram:", data,"took ",time()-start)

    start = time()
    data = plt.hist(table["PKTSEQCN"], bins=10, range=(0, 100))
    print("matplotlib:", data[0],"took ",time()-start)
