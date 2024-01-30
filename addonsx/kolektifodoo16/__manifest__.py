# -*- coding: utf-8 -*-
{
    'name': "Kolektif Colaboration Space",

    'summary': """
        Ini merupakan Modul Kolektif Colaboration Space,
        yang didalamnya ada penjualan, pembeliaan dari supplier dan Penyewaan Ruangan
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
        'data/referensi_penjualan.xml',
        'data/referensi_pelanggan.xml',
        'data/referensi_pembelian.xml',
        'data/referensi_ruangan.xml',
        'data/referensi_penyewaan.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/menu.xml',
        'views/karyawan_view.xml',
        'views/makanan_view.xml',
        'views/minuman_view.xml',
        'views/penjualan_view.xml',
        'views/bahanbaku_view.xml',
        'views/supplier_view.xml',
        'views/pelanggan_view.xml',
        'views/pembelian_view.xml',
        'views/ruangan_view.xml',
        'views/jenisruangan_view.xml',
        'views/penyewaan_view.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
