import sys, argparse, shutil, os
import logging
from evtxtoelk import EvtxToElk

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputpath", help="Path containing EVTX to be imported")
    parser.add_argument("-o", "--outputpath", help="Path to move successfully imported EVTX")
    parser.add_argument("-e", "--errorpath", help="Path to move EVTX that failed to import")
    parser.add_argument("-es", "--elasticsearch", help="Elasticsearch server (http[s]://localhost:9200)")

    args=parser.parse_args()

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    inputpath=args.inputpath
    outputpath=args.outputpath
    errorpath=args.errorpath
    elasticsearch=args.elasticsearch

    print ('Input path is "', args.inputpath, '"')
    print ('Output path is "', outputpath, '"')
    print ('Error path is "', errorpath, '"')
    print ('Elasticsearch server is "', elasticsearch, '"')

    logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S')

    path = inputpath
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.evtx' in file:
                files.append(os.path.join(r, file))
    
    for f in files:
        logging.info(f)
        try:
            EvtxToElk.evtx_to_elk(f,elasticsearch)
            shutil.move(f,outputpath)
        except KeyboardInterrupt:
            # quit
            sys.exit()
        except:
            shutil.move(f,errorpath)

if __name__ == "__main__":
    main(sys.argv[1:])
