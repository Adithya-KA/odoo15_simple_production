{
    'name': 'Simple Production',
    'version': '15.0.1.0.0',
    'sequence': 100,
    'depends': ['base',
                'product',
                'stock',
                'mrp'
                ],
    'data': [
        'security/ir.model.access.csv',
        'view/production_order.xml',
        'data/production_order_sequence.xml',
             ],
    'license': 'LGPL-3',
}