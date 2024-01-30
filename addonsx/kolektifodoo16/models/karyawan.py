from odoo import models, fields, api

class KolektifKaryawan(models.Model):
    _name = 'kolektif.karyawan'
    _description = 'KolektifKaryawan'
    _inherit ='kolektif.manusia'
    
    npwp = fields.Char(string='No. NPWP')
    bagian = fields.Selection([('pelayan', 'Pelayan'),
                                ('barista', 'Barista'),
                                ('kasir', 'Kasir'),
                                ('pastryChef', 'Pastry Chef'),
                                ], string='Bagian')
    foto = fields.Image('Foto', max_width=150, max_height=150)
    
    
