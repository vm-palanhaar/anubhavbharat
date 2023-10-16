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


class IrShopStatusMsg:
    def irShopNotVerified():
        return {
            'error' : {
                'code' : 'irShopNotVerified_iDukaan',
                'message' : "Your stall's verification process is currently pending. Until verification is complete, certain features "\
                            "will remain disabled. To know more about verification process, please refer to the Settings and Help section.\n"\
            }
        }