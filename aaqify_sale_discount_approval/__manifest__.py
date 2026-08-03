{
    'name': 'Aaqify Sale Discount Approval',
    'version': '18.0.1.0.0',
    'sequence': 7,
    'summary': 'Automated approval activity generation for high sales discounts',
    'author': 'Aaqib Bajwa',
    'license': 'AGPL-3',
    'maintainer': 'Aaqib',
    'website': 'https://aaqibbajwa.com',
    'depends': [
        'sale',
        'mail',
    ],
    'category': 'Sales',
    'description': """
        If the applied discount percentage exceeds the pre-set threshold, a system approval activity is automatically routed to authorized users.
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/sale_discount_approval_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 0.00,
    'currency': 'USD',
    'images': [
        'static/description/banner.png',
        'static/description/main_screenshot.png',
    ],
}