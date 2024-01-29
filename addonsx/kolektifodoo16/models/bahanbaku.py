from odoo import models, fields, api

class KolektifBahanBaku(models.Model):
    _name = 'kolektif.bahanbaku'
    _description = 'KolektifBahanBaku'
    _rec_name ='name'

    kode = fields.Char(string='Kode Bahan Baku')
    menu_id = fields.Many2one(comodel_name='kolektif.menu', string='Daftar Menu', store=True)
    name = fields.Char(string='Nama Bahan Baku')
    komposisi = fields.Integer(string='Komposisi')
    stock = fields.Integer(string='Stock')
    harga  = fields.Integer(string='Harga')
    supplier_ids = fields.Many2many(comodel_name='kolektif.supplier', string='Daftar Supplier')
    
    
    
    
    
