class AddOrgMsg:
    def addOrgSuccess():
        return "\U0001F389 Congratulations \U0001F389\n"\
        "Your organization has been successfully registered on the iDukaan platform. We've just sent a "\
        "verification email to the registered email address of the organization to complete the process."\
        "Please check you inbox and follow the instructions to get started with iDukaan."\
        "Thank you for choosing us as your partner!\n"\
        "If you have any questions or need assistance, feel free to contact our support team.\n"\
        "Welcome to the iDukaan family! \U0001F680"
    
    def addOrgFoundFailed():
        return {
            'error' : {
                'code' : 'businessAddOrgFound_iDukaan',
                'message' : "We apologize, but it appears that the registration number you provided is already in use. "\
                    "Please double-check the information and ensure you haven't previously registered your organization on iDukaan. "\
                    "If you believe this is a mistake or need further assistance, please contact our support team for help. "\
                    "Thank you for your understanding."
            }
        }
    

class OrgListMsg:
    def orgListFailed_NotFound():
        return {
        'error' : {
            'code' : 'bussinessOrgListNotFound_iDukaan',
            'message' : "Sorry, we couldn't find the organization associated with your account. To resolve this:\n\n"\
                        "1. Add Organization: If you haven't already, please add your organization to your account.\n\n"\
                        "2. Request Your Manager: If you believe you should be part of an existing organization, kindly "\
                        "reach out to your manager and request them to add you to the organization.\n\n"\
                        "If you need any assistance, feel free to contact our support team."
        }
    }


def businessOrgNotVerified(orgName):
    return {
        'error' : {
            'code' : 'bussinessOrgNotVerified_iDukaan',
            'message' : f'Verficiation in-progess for {orgName}. Please check your registered mail for verification process.'
        }
    }
