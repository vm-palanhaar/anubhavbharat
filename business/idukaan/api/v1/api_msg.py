class AddOrgMsg:
    def addOrgSuccess():
        return "Your organization has been successfully registered on the iDukaan platform. We've just sent a "\
        "verification email to the registered email address of the organization to complete the process. "\
        "Please check you inbox and follow the instructions to get started with iDukaan."\
        "Thank you for choosing us as your partner!\n"\
        "If you have any questions or need assistance, feel free to contact our support team.\n"\
        "Welcome to the iDukaan family!"

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

    def orgVerificationInProcess():
        return "Your organization's verification process is currently pending. Until verification is complete, certain features "\
        "will remain disabled. To verify your organization, please refer to the Settings and Help section.\n"\


def businessOrgNotVerified(org):
    return {
        'error' : {
            'code' : 'bussinessOrgNotVerified_iDukaan',
            'message' : f'Verficiation in-progess for {org.name}. Please check your registered mail for verification process.'
        }
    }


class OrgEmpMsg:
    def businessOrgEmpFound(emp): 
        return {
            'error' : {
                'code' : 'businessOrgEmpFound_iDukaan',
                'message' : f'{emp.user.first_name} {emp.user.last_name} is already associated with {emp.org.name}'
            }
        }
    
    def businessOrgEmpNotMng(org):
        return {
            'error' : {
                'code' : 'bussinessOrgEmpNotManager_iDukaan',
                'message' : f'You are not authorized to add/update/view specific resources in {org.name}!'
            }
        }
    
    def businessOrgEmpSelfNotFound():
        return {
            'error' : {
                'code' : 'businessSelfOrgEmpNotFound_iDukaan',
                'message' : 'You are no longer associated with organization.'
            }
        }