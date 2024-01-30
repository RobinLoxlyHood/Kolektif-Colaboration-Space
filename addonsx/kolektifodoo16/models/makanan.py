from odoo import models, fields, api

class KolektifMakanan(models.Model):
    _name = 'kolektif.makanan'
    _description = 'model.technical.name'

    name = fields.Char(string='Nama Makanan')
    restomakanandetail_ids = fields.One2many(comodel_name='kolektif.makanandetail', inverse_name='restomakanan_id', string='Bahan-bahan')
    harga = fields.Integer(string='Harga per Porsi')
    qty_jual = fields.Integer(string='Quantity Penjualan')
    
class KolektifMakananDetail(models.Model):
    _name = 'kolektif.makanandetail'
    _description = 'Kolektif Makanan Detail'
    restobahan_id = fields.Many2one(comodel_name='kolektif.bahanbaku', string='Nama Bahan')
    kebutuhan = fields.Integer(string='Kebutuhan')
    restomakanan_id = fields.Many2one(comodel_name='kolektif.makanan', string='Makanan')