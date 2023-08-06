import logging, json, datetime, pickle,re
from json.decoder import JSONDecodeError
import requests
from requests.exceptions import ConnectionError
import urllib3
from dataclasses import dataclass
from absbox.local.util import mkTag,query
from absbox.local.component import mkPool,mkAssumption
import pandas as pd

#logging.captureWarnings(True)
urllib3.disable_warnings()

def isDate(x):
    return re.match(r"\d{4}\-\d{2}\-\d{2}",x)


@dataclass
class API:
    url: str
    server_info = {}
    version:str = "0","5","0"

    def __post_init__(self):
        try:
            _r = requests.get(f"{self.url}/version",verify=False).text
        except (ConnectionRefusedError, ConnectionError):
            logging.error(f"Error: Can't not connect to API server {self.url}")
            self.url = None
            return

        echo = json.loads(_r)
        self.server_info = echo
        x,y,z = echo['version'].split(".")
        logging.info(f"Connect Successfully with engine version {echo['version']}")
        if self.version[1] != y:
            logging.error(f"Failed to init the api instance, lib support={self.version} but server version={echo['version']} , pls upgrade your api package by: pip -U absbox")
            return

    def build_req(self
                  ,deal
                  ,assumptions
                  ,pricing=None
                  ,read=None):

        if assumptions is None:
            return json.dumps({"deal": deal.json
                       ,"assump": None
                       ,"bondPricing": deal.read_pricing(pricing) if (pricing is not None) else None}
                   , ensure_ascii=False)

        if isinstance(assumptions, dict):
            return json.dumps({"deal": deal.json
                       ,"assump": mkTag(("Multiple"
                                          ,{ scenarioName:deal.read_assump(a) for (scenarioName,a) in assumptions.items()}))
                       ,"bondPricing": deal.read_pricing(pricing)}
                   , ensure_ascii=False)
        else:
            return json.dumps({"deal": deal.json
                       ,"assump": mkTag(("Single",deal.read_assump(assumptions)))
                       ,"bondPricing": deal.read_pricing(pricing)}
                   , ensure_ascii=False)

    def build_pool_req(self ,pool ,assumptions=[] ,read=None):
        return json.dumps({"pool": mkPool(pool)
                          ,"pAssump": [ mkAssumption(a) for a in assumptions]}
                          ,ensure_ascii=False)

    def validate(self, _r):
        error = []
        warning = []
        _r = json.loads(_r)
        _deal_key = 'deal' if 'deal' in _r else '_deal'
        __d = _r[_deal_key]
        _d = __d['contents']
        valid_acc = set(_d['accounts'].keys())
        valid_bnd = set(_d['bonds'].keys())
        valid_fee = set(_d['fees'].keys())
        _w = _d['waterfall']

        if _w is None:
            raise RuntimeError("Waterfall is None")

        # validatin waterfall
        for wn,wa in _w.items():
            for idx,action in enumerate(wa):
                #print(action)
                action = action[1]
                match action['tag']:
                    case 'PayFeeBy':
                        if (not set(action['contents'][1]).issubset(valid_acc)) \
                            or (not set(action['contents'][2]).issubset(valid_fee)):
                            error.append(f"{wn},{idx}")
                    case 'PayFee':
                        if (not set(action['contents'][0]).issubset(valid_acc)) \
                            or (not set(action['contents'][1]).issubset(valid_fee)):
                            error.append(f"{wn},{idx}")     
                    case 'PayInt':
                        if (action['contents'][0] not in valid_acc) \
                            or (not set(action['contents'][1]).issubset(valid_bnd)):
                            error.append(f"{wn},{idx}")  
                    case 'PayPrin':
                        if (action['contents'][0] not in valid_acc) \
                            or (not set(action['contents'][1]).issubset(valid_bnd)):
                            error.append(f"{wn},{idx}")  
                    case 'PayPrinBy':
                        if (action['contents'][1] not in valid_acc) \
                            or (not set(action['contents'][2]).issubset(valid_bnd)):
                            error.append(f"{wn},{idx}")  
                    case 'PayResidual':
                        if (action['contents'][1] not in valid_acc) \
                            or (action['contents'][2] not in valid_bnd):
                            error.append(f"{wn},{idx}")  
                    case 'Transfer':
                        if (action['contents'][0] not in valid_acc) \
                            or (action['contents'][1] not in valid_acc):
                            error.append(f"{wn},{idx}")
                    case 'TransferBy':
                        if (action['contents'][1] not in valid_acc) \
                            or (action['contents'][2] not in valid_acc):
                            error.append(f"{wn},{idx}")
                    case 'PayTillYield':
                        if (action['contents'][0] not in valid_acc) \
                            or (not set(action['contents'][1]).issubset(valid_bnd)):
                            error.append(f"{wn},{idx}")
                    case 'PayFeeResidual':
                        if (action['contents'][1] not in valid_acc) \
                            or (action['contents'][2] not in valid_fee):
                            error.append(f"{wn},{idx}")        

        if warning:
            logging.warning(f"Warning in modelling:{warning}")

        if len(error)>0:
            if error:
                logging.error(f"Error in modelling:{error}")
            return False,error,warning
        else:
            return True,error,warning


    def run(self,
            deal,
            assumptions=None,
            pricing=None,
            custom_endpoint=None,
            read=True,
            position=None,
            timing=False):

        if isinstance(assumptions,str):
            assumptions = pickle.load(assumptions)

        if assumptions:
            multi_run_flag = isinstance(assumptions, dict)
        else:
            multi_run_flag = False 
            
        if custom_endpoint:
            url = f"{self.url}/{custom_endpoint}"
        else:
            url = f"{self.url}/run_deal"

        hdrs = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        if isinstance(deal, str):
            with open(deal,'rb') as _f:
                c = _f.read()
                deal = pickle.loads(c)


        req = self.build_req(deal, assumptions, pricing)

        #validate deal
        deal_validate,err,warn = self.validate(req)
        if not deal_validate:
            return deal_validate,err,warn

        try:
            logging.info("sending req",datetime.datetime.now())
            r = requests.post(url
                              , data=req.encode('utf-8')
                              , headers=hdrs
                              , verify=False)
            logging.info("done req",datetime.datetime.now())
        except (ConnectionRefusedError, ConnectionError):
            return None

        if r.status_code != 200:
            __sending_req = req
            print(json.loads(__sending_req))
            raise RuntimeError(r.text)
        try:
            result = json.loads(r.text)
        except JSONDecodeError as e:
            raise RuntimeError(e)

        t_reading_s = datetime.datetime.now()
        if read:
            if multi_run_flag:
                __r = { n:deal.read(_r,position=position) for (n,_r) in result.items()}
            else:
                __r = deal.read(result,position=position)
            t_reading_e = datetime.datetime.now()
            return __r
        else:
            return result

    def runPool(self, pool, assumptions=[], custom_endpoint=None,read=True):
        if custom_endpoint:
            url = f"{self.url}/{custom_endpoint}"
        else:
            url = f"{self.url}/run_pool"        

        hdrs = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        req = self.build_pool_req(pool, assumptions=assumptions)

        try:
            logging.info("sending req",datetime.datetime.now())
            r = requests.post(url, data=req.encode('utf-8'), headers=hdrs, verify=False)
            logging.info("done req",datetime.datetime.now())
        except (ConnectionRefusedError, ConnectionError):
            return None

        if r.status_code != 200:
            __sending_req = req
            print(json.loads(__sending_req))
            raise RuntimeError(r.text)
        try:
            result = json.loads(r.text)
        except JSONDecodeError as e:
            raise RuntimeError(e)

        if read:
            result = pd.DataFrame([_['contents'] for _ in result]
                                                  , columns=["日期", "未偿余额", "本金", "利息", "早偿金额", "违约金额", "回收金额", "损失", "利率"])
            result = result.set_index("日期")
            result.index.rename("日期", inplace=True)
        return result


def save(deal,p:str):
    def save_to(b):
        with open(p,'wb') as _f:
            pickle.dump(b,_f)

    match deal:
        case _:
            save_to(deal)

def init_jupyter():
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    pd.options.display.float_format = '{:,}'.format


def comp_df(x, y):
    return pd.merge(x, y, on="日期", how='outer').sort_index().sort_index(axis=1)

def comp_engines(engine1,engine2, d, a=None):
    
    r1 = engine1.run(d,assumptions=a,read=True)
    r2 = engine2.run(d,assumptions=a,read=True)


    comp_result = {}
    # pool check
    if not r1['pool']['flow'].equals(r2['pool']['flow']):
        comp_result['pool'] = comp_df(r1['pool']['flow'],r2['pool']['flow'])
    else:
        comp_result['pool'] = True

    # expense check  
    comp_result['fee'] = {}
    for fn,f in r1['fees'].items():
        if not f.equals(r2['fees'][fn]):
            comp_result['fee'][fn] = comp_df(f,r2['fees'][fn])
        else:
            comp_result['fee'][fn] = True

    # bond check
    comp_result['bond'] = {}
    for fn,f in r1['bonds'].items():
        if not f.equals(r2['bonds'][fn]):
            comp_result['bond'][fn] = comp_df(f,r2['bonds'][fn])
        else:
            comp_result['bond'][fn] = True


    # account check
    comp_result['account'] = {}
    for fn,f in r1['accounts'].items():
        if not f.equals(r2['accounts'][fn]):
            comp_result['account'][fn] = comp_df(f,r2['accounts'][fn])
        else:
            comp_result['account'][fn] = True

    return comp_result

