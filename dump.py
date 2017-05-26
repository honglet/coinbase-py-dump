import GDAX
import time
import os;
import sys;
from datetime import date
from datetime import timedelta
from datetime import datetime

def dumpProduct(sdate, edate, product_id, granularity = 600):
    publicClient = GDAX.PublicClient(product_id=product_id);
    data = publicClient.getProductHistoricRates(start = sdate, end = edate, granularity = granularity)
    return(data)


def printToFile(data, filename):
    f = open(filename, 'w')
    print >>f, 'timestamp|low|high|open|close|volume|datetime'
    for line in reversed(data):
        print >>f, str(line[0]) + '|' + str(line[1]) + '|' + str(line[2]) + '|' + str(line[3]) + '|' + str(line[4]) + '|' + str(line[5]) + '|' + datetime.fromtimestamp(line[0]).strftime('%Y%m%d %H:%M:%S')
    f.close()

def dumpDaily(date, data_dir, granularity):
    dtime = datetime.strptime(date, '%Y%m%d')
    sdate = datetime. strftime(dtime, '%Y-%m-%d'); edate = datetime.strftime(dtime + timedelta(days=1), '%Y-%m-%d');
    publicClient = GDAX.PublicClient();
    data_dir = os.path.expanduser(data_dir);
    for product in publicClient.getProducts():
        time.sleep(1)
        product_id = product['id'];
        output_dir = data_dir + '/' + product_id
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        filename = output_dir + '/' + date + '.txt';
        data = dumpProduct(sdate, edate, product_id, granularity);
        if data != None:
            printToFile(data, filename)
        else:
            print "Skipping " + date + ' for product ' + product_id;

def main(date, granularity, data_dir):
    dumpDaily(date, data_dir, granularity)
    
if __name__ == "__main__":
    granularity = 300;
    date = (date.today() - timedelta(days=1)).strftime('%Y%m%d');
    data_dir = '~/data/'
    if len(sys.argv)>3:
        data_dir = sys.argv[3];
        granularity = int(sys.argv[2]);
        date = sys.argv[1];
    elif len(sys.argv)>2:
        granularity = int(sys.argv[2]);
        date = sys.argv[1];
    elif len(sys.argv)>1:
        date = sys.argv[1]
    main(date, granularity, data_dir)
