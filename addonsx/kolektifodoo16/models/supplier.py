from odoo import models, fields, api


class KolektifSupplier(models.Model):
    _name = 'kolektif.supplier'
    _description = 'KolektifSupplier'

    name = fields.Char(string='Nama Supplier')
    telp = fields.Char(string='No. Telp.')
    cp  = fields.Char(string='Contact Person')
    bahanbaku_ids = fields.Many2many(comodel_name='kolektif.bahanbaku', string='Supply Bahan Baku')
    alamat = fields.Char(string='Alamat')