from odoo import models, fields, api
from datetime import datetime

class kolektifPenyewaan(models.Model):
    _name = 'kolektif.penyewaan'
    _description = 'Penyewaan Ruangan'
    _rec_name = 'referensi'

    referensi = fields.Char(string='No. Referensi')
    ruangan_id = fields.Many2one(comodel_name='kolektif.ruangan', string='Daftar Ruangan', required=True)
    
    nama_pelanggan = fields.Char(string='Nama Pelanggan', required=True)
    tgl_sewa = fields.Date(string='Tanggal Sewa', default=fields.Date.today, required=True)
    jam_mulai = fields.Float(string='Jam Mulai', required=True)
    jam_selesai = fields.Float(string='Jam Selesai', required=True)
    durasi_sewa = fields.Float(string='Durasi Sewa', compute='_compute_durasi_sewa', store=True)

    @api.depends('jam_mulai', 'jam_selesai')
    def _compute_durasi_sewa(self):
        for record in self:
            if record.jam_mulai and record.jam_selesai:
                record.durasi_sewa = record.jam_selesai - record.jam_mulai
            else:
                record.durasi_sewa = 0.0