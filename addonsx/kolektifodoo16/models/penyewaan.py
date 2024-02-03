from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError
try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None

from io import BytesIO


class kolektifPenyewaan(models.Model):
    _name = 'kolektif.penyewaan'
    _description = 'Penyewaan Ruangan'
    _rec_name = 'referensi'

    qr_code = fields.Char(compute='_compute_qr_code', string='QR Code', store = False)
    referensi = fields.Char(string="No. Referensi",
                                 required=True, 
                                 copy=False, 
                                 readonly=True,
                                 default=lambda self: _('New'))
    membership = fields.Boolean(string='Apakah member ?', default = False)
    pelanggan_id = fields.Many2one(comodel_name='kolektif.pelanggan', string='ID Pelanggan')
    id_member_penjualan = fields.Char(compute='_compute_id_member_penjualan', 
                                      string='Nama Member')
    ruangan_id = fields.Many2one(comodel_name='kolektif.ruangan', 
                                 string='Daftar Ruangan', 
                                 required=True,)
    nama_pelanggan = fields.Char(string='Nama Pelanggan')

    tgl_sewa = fields.Date(string='Tanggal Sewa', default=fields.Date.today, required=True)
    jam_mulai = fields.Selection([('9.00', '09:00'),
                                  ('10.00', '10:00'),
                                  ('11.00', '11:00'),
                                  ('12.00', '12:00'),
                                  ('13.00', '13:00'),
                                  ('14.00', '14:00'),
                                  ('15.00', '15:00'),
                                  ('16.00', '16:00'),
                                  ('17.00', '17:00'),
                                  ('18.00', '18:00'),
                                  ('19.00', '19:00'),
                                  ('20.00', '20:00'),
                                  ('21.00', '21:00'),
                                  ('22.00', '22:00'),
                                  ('23.00', '23:00'),
                                  ('24.00', '24:00'),
                                ], string='Jam Mulai', required=True)
                                  
    jam_selesai = fields.Selection([('9.00', '09:00'),
                                  ('10.00', '10:00'),
                                  ('11.00', '11:00'),
                                  ('12.00', '12:00'),
                                  ('13.00', '13:00'),
                                  ('14.00', '14:00'),
                                  ('15.00', '15:00'),
                                  ('16.00', '16:00'),
                                  ('17.00', '17:00'),
                                  ('18.00', '18:00'),
                                  ('19.00', '19:00'),
                                  ('20.00', '20:00'),
                                  ('21.00', '21:00'),
                                  ('22.00', '22:00'),
                                  ('23.00', '23:00'),
                                  ('24.00', '24:00'),
                                ], string='Jam Selesai', required=True)
    durasi_sewa = fields.Integer(string='Durasi Sewa', compute='_compute_durasi_sewa', store=True)
    total_biaya = fields.Integer(string='Total Biaya', compute='_compute_total_biaya', store=True)
    
    
    @api.depends('pelanggan_id')
    def _compute_id_member_penjualan(self):
        for rec in self:
            rec.id_member_penjualan = rec.pelanggan_id.nama_pelanggan

    @api.depends('referensi')
    def _compute_qr_code(self):
        for rec in self:
            if qrcode and base64:
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=4)
                qr.add_data(rec.referensi)
                qr.make(fit=True)
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())
                rec.update({'qr_code': qr_image})

    @api.depends('jam_mulai', 'jam_selesai', 'ruangan_id.jenisruangan_id.harga_sewa_per_jam')
    def _compute_durasi_sewa(self):

        for record in self:
            if record.jam_mulai and record.jam_selesai:
                record.durasi_sewa = float(record.jam_selesai) - float(record.jam_mulai)
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
         
    @api.constrains('jam_mulai', 'jam_selesai', 'tgl_sewa')
    def _check_valid_time_range(self):
        for record in self:
            if float(record.jam_mulai) and float(record.jam_selesai) and float(record.jam_mulai) >= float(record.jam_selesai):
                raise ValidationError(_("Jam Selesai harus lebih besar dari Jam Mulai."))