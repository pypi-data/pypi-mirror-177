''' created 10/19/2022 '''

from .constants import *

class formula_api:
    http_headers = {"Content-type": "application/json", "Accept": "application/json"}
    time_series_url = 'https://api.factset.com/formula-api/v1/time-series'
    cross_sectional_url = 'https://api.factset.com/formula-api/v1/cross-sectional'
    batch_status_url = 'https://api.factset.com/formula-api/v1/batch-status'
    batch_results_url = 'https://api.factset.com/formula-api/v1/batch-result'
    def __init__(self, formulas, ep='cs', ids=None, uni=None, batch=False, dnames=None, bof=False, sof=False):
        self.auths = auth()
        self.authorization = self.auths.auth
        self.formulas = formulas
        self.ep = ep
        self.ids = ids
        self.uni = uni
        self.batch = batch
        self.dnames = dnames
        self.bof = bof
        self.sof = sof
        self.st = time.time()
        self.response = formula_api.request_handling(self)

    def request_handling(self):
        # send request as initially defined
        req = formula_api.make_request(self)
        # print(req.status_code)

        # if request returns an error and bof is set to true, override endpoint and batch settings and resend as batch
        if req.status_code >= 408 and self.bof == True:
            # print('non-batch request failed, batching')
            self.ep = 'ts'
            self.batch = True
            req = formula_api.make_request(self)

        # if error 429 is returned, override endpoint and batch settings, switch authorization, and resent
        if self.status_code == 429:
            self.ep = 'ts'
            self.batch = True
            formula_api.switch_auth(self)
            req = formula_api.make_request(self)
            # print('resubmitted with authswitch')
            if self.status_code == 429:
                # print('waiting 600 for timeout window')
                sleep(600)
                req = formula_api.make_request(self)

        # if batching, call batch handling fxn, print message if something is wrong(req.text doesnt exist)
        if self.batch == True and type(req) != dict:
            req = formula_api.__poll_return_batch(self, req)
        try:
            response = json.loads(req.text)
        except:
            response = req
        # load json and return response
        
        self.ft = time.time()
        
        #build in request logging here
        # formula_api.log_request()
        return response 
        

    def make_request(self):
        request_json = formula_api.__create_request_json(self)
        if self.ep in ['ts', 'time', 'timeseries', 'time_series', 'time series']:
            req = formula_api.time_series_request(
                self,
                request_json=request_json
            )
        elif self.ep in ['cs', 'cross', 'crosssectional', 'cross_sectional', 'cross sectional']:
            req =  formula_api.cross_sectional_request(
                self,
                request_json=request_json
            )
        else:
            raise Exception('Exception no valid endpoint provided, use \"ts\" or \"cs\"')
        self.status_code = req.status_code
        return req

    
    def __poll_return_batch(self, req):
        sleep(10)
        try:
            batch_id_request_json = json.dumps({"data": {"id": json.loads(req.text)['data']['id']}})
        except:
            # print('failed batch_id_request')
            print(req)
            return
        while True:
            batch_status = requests.post(url=status_endpoint,
                                                  data=batch_id_request_json,
                                                  auth=self.authorization,
                                                  headers=headers,
                                                  verify=False)
            # print(batch_status.status_code)
            sleep(10)
            # print(type(batch_status.text))
            try:
                batch_status_response = json.loads(batch_status.text)
            except:
                print(batch_status.text)
                print('failed batch_status_response load')
                print(batch_status.status_code)
                
            # print(batch_status_data['data']['status'])
            if batch_status_response['data']['status'] == 'DONE':
                batch_result = requests.post(url=result_endpoint,
                                                    data=batch_id_request_json,
                                                    auth=self.authorization,
                                                    headers=headers,
                                                    verify=False)
                
                if batch_result.status_code == 200:
                    return batch_result
                elif batch_result.status_code >= 400:
                    print('error in retrieving batch_result_response')
                    print(batch_result.status_code)
                    print(batch_result)
                    # print(batch_result_response.text)
                    return
            elif batch_status_response['data']['status'] != 'DONE':
                pass


    def time_series_request(self, request_json):
        return formula_api.__http_post(
            self,
            URL=formula_api.time_series_url,
            json_string=request_json
        )


    def cross_sectional_request(self, request_json):
        return formula_api.__http_post(
            self,
            URL=formula_api.cross_sectional_url,
            json_string=request_json
        )

    def __create_request_json(self):
        request = {
            "data": {
                "formulas": self.formulas,
                "flatten": "Y"
            }
        }
        if self.batch == True:
            request['data']['batch'] = 'Y'
        if self.dnames is not None:
            request['data']['displayName'] = self.dnames
        if self.ids is not None:
            request['data']['ids'] = self.ids
        elif self.uni is not None:
            request['data']['universe'] = self.uni
        elif self.uni == None and self.ids == None:
            request['data']['ids'] = ['dummy']
        return json.dumps(request)

    
    def __http_post(self, URL, json_string):
        try:
            r = requests.post(
                URL,
                auth=self.authorization,
                headers=formula_api.http_headers,
                data=json_string,
                verify=False,
            )
            return r
        except Exception as e:
            return False, str(e)

    def status_code(self):
        return self.status_code

    def df(self):
        try:
            self.df = pd.json_normalize(self.response['data'])
        except:
            self.df = pd.DataFrame(self.response, index=range(math.ceil(len(list(self.response.values()))/len(list(self.response.keys())))))
        return self.df

    @property
    def runtime(self):
        self.rt = (self.ft - self.st)
        return self.rt

    def switch_auth(self):
        self.authorization = next(self.auths)
        # print('ratelimit reached, switching')
        # print(self.authorization)
        return

    def generate_meta(self):
        df_log = pd.DataFrame()
        df_log['name'] = [self.dnames]
        df_log['form'] = [self.formulas]
        df_log['ep'] = [self.ep]
        df_log['size'] = [sys.getsizeof(self.df().iloc[0,1])]
        df_log['time'] = [self.runtime]
        df_log['time/id'] = [self.runtime/len(self.ids)]
        if self.ids != None:
            df_log['n_ids'] = len(self.ids)
        elif self.uni != None:
            df_log['n_ids'] = len(formula_api(formulas=[f'{self.uni}'], uni=self.uni, ep='ts').df())
        return df_log


    def log_request(self):
        df_log = formula_api.generate_meta()
        db = mysql.connector.connect(
            host='localhost',
            user='append',
            password='Appendaccess1!',
            database='request_logs')
        df_log.to_sql('request_log', con=db, if_exists='append', method='multi')
        





class ofdb_api:
    def __init__(self, path):
        self.host = "https://api.factset.com/analytics/ofdb/v1/database/"
        self.path = path
        self.uri = urllib.parse.quote(self.path, safe="")
        return

    def get_dates(self):
        url = f'{self.host}{self.uri}/dates'
        r = requests.get(url, auth=authorization, headers=headers)
        if r.status_code >= 400:
            print(r)
            print(r.text)
            return
        response = json.loads(r.text)
        return response

    def delete_date(self, d):
        url = f"{self.host}{self.uri}/dates/{d}"
        r = requests.delete(url, auth=authorization, headers=headers)
        if r.status_code >= 400:
            print(r)
            print(r.text)
        return

    def delete_symbol(self, symbol, d=None):
        if d is None:
            url = f'{self.host}{self.uri}/symbols/{symbol}'
        elif d is not None:
            url = f'{self.host}{self.uri}/dates/{d}/symbols/{symbol}'
        r = requests.delete(url, auth=authorization, headers=headers)
        if r.status_code > 204:
            print(r)
            print(r.text)
        return

    def parse_upload(self, df):
        df.fillna(0, inplace=True)
        df_dict = df.to_dict(orient='index')
        body = {'data': []}
        for i, j in df_dict.items():
            body['data'].append(j)
        url = f"{self.host}{self.uri}/dates/{self.d}"
        n = 0
        k = len(body['data']) / 200
        if k >= 1:
            body_temp = {'data': []}
            while n < len(body['data']):
                m = int(min(200, len(body['data']) - n))
                body_temp['data'] = body['data'][n:(n + m)]
                r = requests.put(url, auth=authorization, headers=headers, data=body_temp)
                if r.status_code >= 400:
                    print(r)
                    print(r.text)
        else:
            body = json.dumps(body)
            r = requests.put(url, auth=authorization, headers=headers, data=body)
            if r.status_code >= 400:
                print(r)
                print(r.text)
        return r, r.text

    def parse_upload_datewise(self, df):
        df.fillna(0, inplace=True)
        zz = list(set(df.index.to_list()))
        for i in tqdm(zz, total=len(zz), desc='uploading data: ', ncols=100):
            df_temp = df[df.index == i]
            df_temp.index = [j for j in range(len(df_temp.index.to_list()))]
            df_dict = df_temp.to_dict(orient='index')
            body = {'data': []}
            for z, j in df_dict.items():
                body['data'].append(j)
            for i in range(len(body['data'])):
                e = list(body['data'][i].values())
                if None in e:
                    del body['data'][i]
            url = f"{self.host}{self.uri}/dates/{i}"
            n = 0
            k = len(body['data']) / 200
            if k >= 1:
                while n < len(body['data']):
                    body_temp = {'data': []}
                    m = int(min(200, len(body['data']) - n))
                    body_temp['data'] = body['data'][n:(n + m)]
                    n += 200
                    body_temp = json.dumps(body_temp)
                    r = requests.put(url, auth=authorization, headers=headers, data=body_temp)
                    if r.status_code >= 400:
                        print(r)
                        print(r.text)
            else:
                body = json.dumps(body)
                r = requests.put(url, auth=authorization, headers=headers, data=body)
                if r.status_code >= 400:
                    print(r)
                    print(r.text)
        return r, r.text

