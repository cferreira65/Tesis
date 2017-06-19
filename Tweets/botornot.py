import botometer


mashape_key = "iykKYyk7XTmshsUERrKagp0XxruZp1mWfoEjsnS24G5TOEopR1"
twitter_app_auth = {
    'consumer_key': '5Rcxy0B6hTefj4WfI83Ov4rGn',
    'consumer_secret': 'IROZKaE6Osnt7FlvVmZlWLEU9V1KT7TyZpda7CgrJKG5Qmtre5',
    'access_token': '86460420-9xJaN64nnrumh3QRJEfKWhTFcjf572kOtHGbRMkta',
    'access_token_secret': 'Rarw3wksqYiVDZsTMPebWDztDSuQuXSiIwfz40jgMkrsC',
  }
bom = botometer.Botometer(mashape_key=mashape_key, **twitter_app_auth)

result = bom.check_account('@clayadavis')

print(result['scores']['universal'])