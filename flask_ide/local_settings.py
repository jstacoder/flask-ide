class LocalConfig(object):
    RECAPTCHA_PUBLIC_KEY = '6Ld04u8SAAAAAA8b8NoE9tal4w3cNOnJ2zpG9vvs'
    RECAPTCHA_PRIVATE_KEY = '6Ld04u8SAAAAAFbm9sdLENomxVL1ZrxLAGd8E3ie'
    SECRET_KEY = 'A Secret Shhh'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_ee.db'# #'mysql://test:test@174.140.227.137/test_ee'#
    #FACEBOOK_APP_ID = '257401644383901'
    #FACEBOOK_APP_SECRET = 'cdd6c5a89f4de972612cba7e9255e3ca'
    FACEBOOK_APP_ID = '269689456488453'
    FACEBOOK_APP_SECRET = 'e9181efb775c5b60689bd4ad87fed86a'
    FACEBOOK_REDIRECT_URI = 'http://174.140.227.137:8089/facebook/auth'
    FACEBOOK_APP_SCOPE = 'publish_stream,email,user_friends,user_about_me,user_activities,user_photos,user_status,read_stream,publish_actions,read_mailbox'
    FACEBOOK_DISPLAY_TYPE = 'popup'
