from odoo import models, fields, api

class KolektifBahanBaku(models.Model):
    _name = 'kolektif.bahanbaku'
    _description = 'Bahan Baku'

    name = fields.Char(string='Nama Bahan')
    stok = fields.Integer(string='Stok', default=0)
    harga = fields.Integer(string='Harga')
    
    # restomakanan_id = fields.Many2one(comodel_name='kolektif.makanan', string='Makanannya')
    # restominuman_id = fields.Many2one(comodel_name='kolektif.minuman', string='Minumannya')
    restomakanan_id = fields.Many2many(comodel_name='kolektif.makanan', string='Makanan')
    restominuman_id = fields.Many2many(comodel_name='kolektif.minuman', string='Minuman')
    supplier_ids = fields.Many2many(comodel_name='kolektif.supplier', string='Daftar Supplier')
    
    
    