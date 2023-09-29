def businessOrgFound():
    return {
        'error' : {
            'code' : 'bussinessOrgFound_iDukaan',
            'message' : 'The registration number you entered already exists in our iDukaan app. Please double-check the registration number and try again. If you need further information or assistance, we recommend raising a request for more information.'
        }
    }

def businessOrgNotVerified(orgName):
    return {
        'error' : {
            'code' : 'bussinessOrgNotVerified_iDukaan',
            'message' : f'Verficiation in-progess for {orgName}. Please check your registered mail for verification process.'
        }
    }

def businessOrgListNotFound():
    return {
        'error' : {
            'code' : 'bussinessOrgListNotFound_iDukaan',
            'message' : 'You are not associated with organization. You can follow any one of the following point:\n\n'\
                        '- Add organization.\n'\
                        '- Request your manager to add you in organization.'
        }
    }