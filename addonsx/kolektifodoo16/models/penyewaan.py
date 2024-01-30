from odoo import models, fields, api, _
from datetime import datetime

class kolektifPenyewaan(models.Model):
    _name = 'kolektif.penyewaan'
    _description = 'Penyewaan Ruangan'
    _rec_name = 'referensi'

    referensi = fields.Char(string="No. Referensi",
                                 required=True, 
                                 copy=False, 
                                 readonly=True,
                                 default=lambda self: _('New'))
    membership = fields.Boolean(string='Apakah member ?', default = False)
    pelanggan_id = fields.Many2one(comodel_name='kolektif.pelanggan', string='ID Pelanggan')
    ruangan_id = fields.Many2one(comodel_name='kolektif.ruangan', string='Daftar Ruangan', required=True)
    nama_pelanggan = fields.Char(string='Nama Pelanggan')
    tgl_sewa = fields.Date(string='Tanggal Sewa', default=fields.Date.today, required=True)
    jam_mulai = fields.Float(string='Jam Mulai', required=True)
    jam_selesai = fields.Float(string='Jam Selesai', required=True)
    durasi_sewa = fields.Float(string='Durasi Sewa', compute='_compute_durasi_sewa', store=True)
    total_biaya = fields.Float(string='Total Biaya', compute='_compute_total_biaya', store=True)
    
    
    @api.depends('jam_mulai', 'jam_selesai', 'ruangan_id.jenisruangan_id.harga_sewa_per_jam')
    def _compute_durasi_sewa(self):
        for record in self:
            if record.jam_mulai and record.jam_selesai:
                record.durasi_sewa = record.jam_selesai - record.jam_mulai
            else:
                record.durasi_sewa = 0.0

    @api.depends('durasi_sewa', 'ruangan_id.jenisruangan_id.harga_sewa_per_jam')
    def _compute_total_biaya(self):
        for record in self:
            harga_per_jam = record.ruangan_id.jenisruangan_id.harga_sewa_per_jam
            durasi_sewa = record.durasi_sewa
            total_biaya = durasi_sewa * harga_per_jam
            record.total_biaya = total_biaya

    @api.model
    def create(self,vals):        
        if vals.get('referensi', _("New")) == _("New"):   
            membership = vals.get('membership',False)
            if membership == True:            
                vals['referensi'] = self.env['ir.sequence'].next_by_code('kolektifodoo16.referensi.penyewaan_member') or _("New")    
            else:
                vals['referensi'] = self.env['ir.sequence'].next_by_code('kolektifodoo16.referensi.penyewaan_nonmember') or _("New")
        record = super(kolektifPenyewaan, self).create(vals)
        return record