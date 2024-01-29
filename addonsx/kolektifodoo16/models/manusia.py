from odoo import models, fields, api
from odoo.exceptions import ValidationError
class KolektifManusia(models.Model):
    _name = 'kolektif.manusia'
    _description = 'kolektif.manusia'

    name = fields.Char(string='Nama')
    tempat_lahir = fields.Char(string='Tempat Lahir')
    tanggal_lahir  = fields.Date(string='Tanggal Lahir')
    jenis_kelamin = fields.Selection(string='Jenis Kelamin', selection=[('pria', 'Pria'), 
                                                          ('wanita', 'Wanita'),])
    alamat = fields.Char(string='Alamat')
    # is_domisili = fields.Boolean(string='Alamat = Domisili')
    # domisili = fields.Char(string='Domisili')
    @api.constrains('tanggal_lahir')
    def _check_date_constraint(self):
        for record in self:
            if record.tanggal_lahir and record.tanggal_lahir > fields.Date.today():
                raise ValidationError("Tanggal tidak boleh melebihi tanggal sekarang.")
    
    

    
    