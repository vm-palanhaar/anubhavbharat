import http.client, os, json

def getPnrStatusApi(pnr: str):
    conn = http.client.HTTPSConnection("apigw.umangapp.in")

    payload = {
            'tkn' : os.getenv("TOKEN"),
            'lang' : "en",
            'usrid' : os.getenv("USER_ID"),
            'mode' : "web",
            'pltfrm' : "windows",
            'did' : None,
            'srvid' : os.getenv("INDRAIL_PNRSTATUS_SRV_ID"),
            'deptid' : os.getenv("INDRAIL_PNRSTATUS_DEPT_ID"),
            'subsid' : 0,
            'susid2' : 0,
            'formtrkr' : 0,
            'pnrnumber' : pnr,
            'pnrEnqType' : 'ALL'
        }
    
    headers = {
            'Content-Type': "application/json",
            'Accept': "application/json",
            'deptid': os.getenv("INDRAIL_PNRSTATUS_DEPT_ID"),
            'srvid': os.getenv("INDRAIL_PNRSTATUS_SRV_ID"),
            'subsid': "0",
            'subsid2': "0",
            'formtrkr': "0",
            'x-api-key': os.getenv("API_KEY"),
        }
    
    conn.request("POST", "/CRISApi/ws1/nget/pnrEnquiry", json.dumps(payload), headers)

    res = conn.getresponse()
    data = res.read()
    if res.status == 200:
        print("(API) Station List API response success")
    else:
        print(f"(API) Station List API response status code: {res.status}")
        print(data.decode())
        return
    conn.close()

    try:
        json_data = json.loads(data.decode())
    except json.JSONDecodeError as e:
        pass  

    if 'errorMessage' in json_data['pd']:
        print(json_data['pd']['errorMessage'])
    if 'fault' in json_data['pd']:
        print(json_data['pd']['fault'])
    if 'pnrNumber' in json_data['pd']:
        passenger_list = []
        for p in json_data['pd']['passengerList']:
            passenger_list.append({
                'bookingStatus' : p['bookingStatus'],
                'bookingBerthNo' : p['bookingBerthNo'],
                'bookingCoachId' : p['bookingCoachId'],
                'bookingBerthCode' : p['bookingBerthCode'],
                'currentStatus' : p['currentStatus'],
                'currentBerthNo' : p['currentBerthNo'],
            })
        response_data = {
            'trainNo' : json_data['pd']['trainNumber'],
            'trainName' : json_data['pd']['trainName'],
            'trainStartDate' : json_data['pd']['trainStartDate'].split("T")[0],
            'dateOfJourney' : json_data['pd']['dateOfJourney'].split("T")[0],
            'bookingFare' : json_data['pd']['bookingFare'],
            'pnrNumber' : json_data['pd']['pnrNumber'],
            'chartStatus' : json_data['pd']['chartStatus'],
            'journeyClass' : json_data['pd']['journeyClass'],
            'sourceStation' : json_data['pd']['sourceStation'],
            'boardingPoint' : json_data['pd']['boardingPoint'],
            'destinationStation' : json_data['pd']['destinationStation'],
            'reservationUpto' : json_data['pd']['reservationUpto'],
            'quota' : json_data['pd']['quota'],
            'passengerList' : passenger_list
        }
    return json_data