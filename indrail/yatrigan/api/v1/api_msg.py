class ShopListMsg:
    def irShopListInActiveNotVerified(stationName, stationCode):
        return {
            'error' : {
                'code' : 'irShopListInActiveNotVerified_Yatrigan',
                'message' : f'Verification in-progress for stalls/shops found at {stationName} - {stationCode}.'
            }
        }

    def irShopListEmpty(stationName, stationCode):
        return {
            'error' : {
                'code' : 'irShopListEmpty_Yatrigan',
                'message' : f'Stalls/Shops not found at {stationName} - {stationCode}. Following may be the reasons as stalls/shops are:\n\n'
                        '- not present on this station.\n'
                        '- not registered on iDukaan.'
            }
        }
    
class TrainMsg:
    def irTrainNotFound():
        return {
            'error' : {
                'code' : 'trainNotFound_Yatrigan',
                'message' : 'Train not found!'
            }
        }
