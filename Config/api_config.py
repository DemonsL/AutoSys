
file_sql_name = ['AscAsinBussiness', 'AscSearchWeek', 'AscSearchMonth', 'AscPayments']

file_path = {
    'AscAsinBussiness': {
        'src': '/home/data/bussiness/parse/',
        'dst': '/home/data/bussiness/achieve/'
    },
    'AscSearchWeek': {
        'src': '/home/data/keyword/parse/week/',
        'dst': '/home/data/keyword/achieve/week/'
    },
    'AscSearchMonth':{
        'src': '/home/data/keyword/parse/month/',
        'dst': '/home/data/keyword/achieve/month/'
    },
    'AscPayments':{
        'src': '/home/data/payments/parse/',
        'dst': '/home/data/payments/achieve/'
    }
}


# Amazon搜索下拉框关键词

amz_dropdown_host = {
    'US': 'https://completion.amazon.com',
    'CA': 'https://completion.amazon.com',
    'UK': 'https://completion.amazon.co.uk',
    'DE': 'https://completion.amazon.co.uk',
    'JP': 'https://completion.amazon.co.jp'
}

amz_dropdown_interface = '/api/2017/suggestions?site-variant=desktop&mid={marketplace}&alias=aps&prefix={prefix}'

amz_marketplace = {
    'US': 'ATVPDKIKX0DER',
    'CA': 'A2EUQ1WTGCTBG2',
    'UK': 'A1F83G8C2ARO7P',
    'DE': 'A1PA6795UKMFR9',
    'JP': 'A1VC38T7YXB528'
}