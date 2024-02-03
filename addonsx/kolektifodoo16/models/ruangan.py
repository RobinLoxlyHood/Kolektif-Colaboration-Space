from odoo import models, fields,api, _

class KolektifRuangan(models.Model):
    _name = 'kolektif.ruangan'
    _description = 'Ruangan'

    name = fields.Char(string='Nama Ruangan', required=True)
    kode = fields.Char(string="Kode Pelanggan",
                                 required=True, 
                                 copy=False, 
                                 readonly=True,
                                 default=lambda self: _('New'))
    jenisruangan_id = fields.Many2one('kolektif.jenisruangan', string='Jenis Ruangan', required=True)
    
    @api.model
    def create(self,vals):
        if vals.get('kode', _("New")) == _("New"):  
            bag = vals.get('jenisruangan_id', 1)
            print(bag)
            if bag == 1:
                vals['kode'] = self.env['ir.sequence'].next_by_code('kolektifodoo16.referensi.ruangankecil') or _("New")
            elif bag == 2:
                vals['kode'] = self.env['ir.sequence'].next_by_code('kolektifodoo16.referensi.ruangansedang') or _("New") 
            elif bag == 3:
                vals['kode'] = self.env['ir.sequence'].next_by_code('kolektifodoo16.referensi.ruanganbesar') or _("New")  
        record = super(KolektifRuangan, self).create(vals)
        return record