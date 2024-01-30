from odoo import models, fields, api

class KolektifMinuman(models.Model):
    _name = 'kolektif.minuman'
    _description = 'model.technical.name'

    name = fields.Char(string='Nama Minuman')
    restominumandetail_ids = fields.One2many(comodel_name='kolektif.minumandetail', inverse_name='restominuman_id', string='Bahan-bahan')
    harga = fields.Integer(string='Harga per Porsi')
    
class KolektifMinumanDetail(models.Model):
    _name = 'kolektif.minumandetail'
    _description = 'RestoMinumanDetail'
    restobahan_id = fields.Many2one(comodel_name='kolektif.bahanbaku', string='Nama Bahan')
    kebutuhan = fields.Integer(string='Kebutuhan')
    restominuman_id = fields.Many2one(comodel_name='kolektif.minuman', string='Makanan')