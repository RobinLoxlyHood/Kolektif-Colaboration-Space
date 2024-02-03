from odoo import models, fields

class KolektifJenisRuangan(models.Model):
    _name = 'kolektif.jenisruangan'
    _description = 'Jenis Ruangan'

    name = fields.Char(string='Jenis Ruangan', required=True)
    kapasitas = fields.Char(string='Kapasitas', required=True)
    harga_sewa_per_jam = fields.Integer(string='Harga Sewa per Jam', required=True)