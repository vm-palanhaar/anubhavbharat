class IrAddShopMsg:
    def addShopFoundFailed():
        return {
            'error' : {
                'code' : 'irAddShopFound_iDukaan',
                'message' : "We apologize, but it appears that the registration number you provided is already in use. "\
                    "Please double-check the information and ensure you haven't previously registered your shop/stall on iDukaan. "\
                    "If you believe this is a mistake or need further assistance, please contact our support team for help. "\
                    "Thank you for your understanding."
            }
        }
    
    def addShopSuccess():
        return "Your stall has been successfully registered on the iDukaan platform. "\
        "Thank you for choosing us as your partner!\n"\
        "If you have any questions or need assistance, feel free to contact our support team.\n"\
        "Welcome to the iDukaan family!"
    

class IrShopList:
    def irOrgShopListEmptyMng():
        return {
            'error' : {
                'code' : 'irOrgShopListEmptyMng_iDukaan',
                'message' : 'Stalls at railway station premises are not registered on iDukaan.'
            } 
        }
    
    def irOrgShopNotFound():
        return {
            'error' : {
                'code' : 'irOrgShopNotFound_iDukaan',
                'message' : 'This stall had been deleted from iDukaan.'
            }
        }


class IrShopEmpMsg:
    def addIrShopEmpSuccess(emp_user):
        return f"Good news! {emp_user.first_name} {emp_user.last_name} has been successfully onboarded and is now part of our team. "\
        "Please extend a warm welcome and provide any necessary guidance as they begin their journey with us."
    
    def addIrShopEmpFound(user, shop): 
        return {
            'error' : {
                'code' : 'irShopEmpFound_iDukaan',
                'message' : f'{user.first_name} {user.last_name} is already associated with {shop.name}'
            }
        }
    
    def irOrgShopEmpNotMng(shop):
        return {
            'error' : {
                'code' : 'irOrgShopEmpNotManager_iDukaan',
                'message' : f'You are not authorized to add/update/view specific resources in {shop.name}!'
            }
        }
    
    def irOrgShopEmpSelfNotFound():
        return {
            'error' : {
                'code' : 'irOrgShopEmpSelfNotFound_iDukaan',
                'message' : 'You are no longer associated with shop/stall.'
            }
        }
    
    def addIrOrgShopEmpListDuplicate():
        return {
            'error' : {
                'code' : 'addIrOrgShopEmpListDuplicate_iDukaan',
                'message' : "Great news, Manager! All employees from your organization are already associated "\
                "with this stall. Your team is ready to shine, and your event is set for success. If you "\
                "have any other needs or questions, please don't hesitate to reach out iDukaan. Best of luck!"
            }
        }
    
    def addIrShopEmpListMessage():
        return {
            'message' : "Welcome, Manager! To streamline your onboarding process, please select an employee from "\
                        "the list to bring them on board at your stall. Your choice plays a vital role in building "\
                        "a dynamic team. Let\'s get started!"
        }


class IrShopStatusMsg:
    def irShopNotVerified():
        return {
            'error' : {
                'code' : 'irShopNotVerified_iDukaan',
                'message' : "Your stall's verification process is currently pending. Until verification is complete, certain features "\
                            "will remain disabled. To know more about verification process, please refer to the Settings and Help section.\n"\
            }
        }