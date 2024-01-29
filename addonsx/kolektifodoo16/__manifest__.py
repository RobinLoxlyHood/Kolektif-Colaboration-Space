# -*- coding: utf-8 -*-
{
    'name': "kolektifodoo16",

    'summary': """
        ini modul kolektif
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'productivity',
    'application':True,
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/menu.xml',
        'views/karyawan_view.xml',
        'views/menu_view.xml',
        'views/jenismenu_view.xml',
        'views/pelanggan_view.xml',
        'views/penjualan_view.xml',
        'views/bahanbaku_view.xml',
        'views/supplier_view.xml',
        'views/pembelian_view.xml',
        'views/ruangan_view.xml',
        'views/penyewaan_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
