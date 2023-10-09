class AddShopMsg:
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
        return "Your shop/stall has been successfully registered on the iDukaan platform. "\
        "Thank you for choosing us as your partner!\n"\
        "If you have any questions or need assistance, feel free to contact our support team.\n"\
        "Welcome to the iDukaan family!"
    

class ShopList:
    def irOrgShopListEmptyMng():
        return {
            'error' : {
                'code' : 'irOrgShopListEmptyMng_iDukaan',
                'message' : 'Shops/Stalls at railway station premises are not registered on iDukaan.'
            } 
        }
    