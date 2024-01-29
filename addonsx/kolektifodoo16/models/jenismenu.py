from odoo import models, fields, api

class KolektifJenisMenu(models.Model):
    _name = 'kolektif.jenismenu'
    _description = 'KolektifJenisMenu'

    name = fields.Selection(string='Jenis ', 
                            selection=[('makanan', 'Makanan'), 
                                        ('minuman', 'Minuman'),])
    daftarbarang_ids = fields.One2many(comodel_name='kolektif.menu', 
                                       inverse_name='jenis', 
                                       string='Daftar Menu')
    kode = fields.Char(string='Kode')
    
    


