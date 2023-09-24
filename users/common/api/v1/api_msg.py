class UserSignUpMsg:
    def userSignupSuccess():
        return 'We are happy to on-board you. Please check registered  mail for account verification link and instructions to verify identity.'

    def userSignupFailed():
        return "We're sorry, but we couldn't sign you up. Please check your information and try again."
    
class UserLoginMsg:
    def userLoginFailed_UserCredInvalid():
        return "Your username or password is incorrect. Please try again."
    
    def userLoginFailed_UserInActive():
        return "Your account is not yet active because you have not verified your email address."\
        " Please check your email and click on the verification link to activate your account."
    
    def userLoginSuccess_UserInVerfieid():
        return "Your account is not yet secure because you have not verified your identity."\
        " Please verify your identity to access all features of the app."
    
    def userLoginSuccess():
        return "Loading your business diary..."
