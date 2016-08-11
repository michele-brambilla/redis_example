import argparse
import redis
import json
import os

from pprint import pprint



def Populate(f):
    with open(f) as json_data:
        configs = json.load(json_data)
        print configs
        for config_name in configs:
            config = configs[config_name]
            
            for key, value in config['user'].items():
                r.hset(config_name+':user', key, value)
            
            for key, value in config['experiment'].items():
                r.hset(config_name+':experiment', key, value)
            
            for source, source_data in config['sources'].items():
                r.sadd(config_name+':sources', source)
                for key, value in source_data.items():
                    r.hset('source:'+config_name+':'+source, key, value)



def Query(config=None):
    d = dict()
    lst = dict()
    
    for key in r.scan_iter():
        key_type = r.type(key)
        
        if key_type == "hash" and key.startswith('source'):
            d[key] = r.hgetall(key)
        if key_type == "set":
            lst[key] = r.smembers(key)

    return d,lst


def Update(key,item,val,redis):
    d,lst = Query()
    if key in d.keys() and redis.hexists(key,item):
        old_val = redis.hget(key,item)
        redis.hset(key,item,val)
        r.publish(src[0],src[1])

        
def config_change_handler(message):
    print 'Change on hash '+message['channel']+' key: '+message['data']
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Redis client test")
    parser.add_argument("-p","--populate",
                        action="store",
                        nargs='?',
                        type=str,
                        help="populate redis with file content")
    parser.add_argument("-q","--query", 
                        action="store_true",
                        help="query redis dictionary")
    parser.add_argument("-k","--key", 
                        action="store",
                        nargs='?',
                        type=str,
                        help="dictionary keys to look for")
    parser.add_argument("-l","--listen", 
                        action="store",
                        nargs='?',
                        type=str,
                        help="sources to listen")
    parser.add_argument("-u","--update", 
                        action="store",
                        nargs='?',
                        type=str,
                        help="key-value to update")

    args = parser.parse_args()

    r = redis.StrictRedis('pc11997',port='63791')

    if args.populate != None:
        Populate(args.populate)

    if (args.query and args.key==None):
        sources_list = Query()
        pprint(sources_list)

    if args.listen != None:
        p = r.pubsub(ignore_subscribe_messages=True)
        # Split argument input into channels to wich subscribe
        for src in args.listen.split(','):
            p.subscribe(**{src:config_change_handler})

        thread = p.run_in_thread(sleep_time=0.001)
        print ''
        print 'Press any key to stop'
        print ''
        os.system('read')
        thread.stop()
                
    if args.update != None:
        src=args.update.split(',')
        Update(src[0],src[1],src[2],r)


    if args.key!=None:
        
        for key in r.scan_iter():
            if key == args.key:
                key_type = r.type(key)
                if key_type == "hash":
                    if key==args.key:
                        pprint(r.hgetall(key))
                if key_type == "set":
                    if key==args.key:
                        pprint(r.smembers(key))
