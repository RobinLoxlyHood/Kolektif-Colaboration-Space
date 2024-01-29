from odoo import models, fields

class KolektifRuangan(models.Model):
    _name = 'kolektif.ruangan'
    _description = 'Ruangan'

    name = fields.Char(string='Nama Ruangan', required=True)
    kode = fields.Char(string='Kode Ruangan')
    kapasitas = fields.Integer(string='Kapasitas', required=True)
    fasilitas = fields.Text(string='Fasilitas')