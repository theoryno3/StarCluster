#!/usr/bin/env python
"""
StarCluster SunGrinEngine stats parsing module
"""
import types
import time
import datetime
from datetime import datetime
import logging
import pickle
import numpy as np
from pylab import figure, show
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
import matplotlib.ticker as ticker
from starcluster import balancers
from starcluster.balancers import LoadBalancer 
from starcluster import utils
from starcluster.logger import log, INFO_NO_NEWLINE
from starcluster.utils import print_timing

class SGEVisualizer(object):
    stat = None
    filepath = '/tmp/starcluster-sge-stats.csv'

    def record(self,s):
        """
        This function takes an SGEStats object and takes a snapshot to a CSV file.
        It takes an SGEStats object as a parameter.
        """
        stat = s
        bits = []
        #first field is the time
        now = datetime.datetime.utcnow()
        bits.append(now)
        #second field is the number of hosts
        bits.append(s.count_hosts())
        #third field is # of running jobs
        bits.append(len(s.get_running_jobs()))
        #fourth field is # of queued jobs
        bits.append(len(s.get_queued_jobs()))
        #fifth field is total # slots
        bits.append(s.count_total_slots())
        #sixth field is average job duration
        bits.append(s.avg_job_duration())
        #seventh field is average job wait time
        bits.append(s.avg_job_duration())
        #last field is array of loads for hosts
        bits.append(s.get_loads())

        #write to file
        f = open(self.filepath, 'a')
        flat = ','.join(str(n) for n in bits)
        #print bits
        f.write(flat)
        f.write('\n')
        f.close()

    def read(self):
        list = []
        file = open(self.filepath,'r')
        for line in file:
            parts = line.split(',')
            a = [datetime.strptime(parts[0],'%Y-%m-%d %H:%M:%S.%f'), int(parts[1]),int(parts[2]),
                 int(parts[3]),int(parts[4]),int(parts[5]),int(parts[6])]
            list.append(a)
        file.close()

        self.records = \
           np.rec.fromrecords(list,names='dt,hosts,running_jobs,queued_jobs,slots,avg_duration')

        #print self.records.queued_jobs

    def graph(self):
        if self.records == None:
            print "ERROR: File hasn't been read() yet."
            return -1
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(self.records.dt, self.records.queued_jobs)
        ax.grid(True)
    
        fig.autofmt_xdate()

        plt.show()
        show()
        print "showed graph"

    def run(self):
        """
        Creates the graphical stuffs
        """
    
