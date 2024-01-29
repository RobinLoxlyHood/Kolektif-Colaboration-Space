from odoo import models, fields, api

class KolektifPelanggan(models.Model):
    _name = 'kolektif.pelanggan'
    _description = 'KolektifPelanggan'
    _inherit = 'kolektif.manusia'
    _rec_name = 'nama_pelanggan'

    kode = fields.Char(string='Kode')
    nama_pelanggan = fields.Char(string='Nama Pelanggan')
    level = fields.Char(compute='_onchange_point', string='Level Member')
    tgl_daftar = fields.Date(string='Tanggal Daftar',
                             default=fields.Date.today())
    penjualan_ids = fields.One2many(comodel_name='kolektif.penjualan', inverse_name='pelanggan_id', string='Data Pembelian')
    point = fields.Integer(compute='_compute_hitung_point', string='Point')

    @api.depends('penjualan_ids')
    def _compute_hitung_point(self):
        for rec in self:
            total = sum(self.env['kolektif.penjualan']
                        .search([('pelanggan_id','=',rec.id)])
                        .mapped('total_bayar'))
            rec.point = total // 10000
    @api.onchange('point')
    def _onchange_point(self):
        for rec in self:
            if rec.point > 500:
                rec.level = "Platinum"
            elif rec.point > 200:
                rec.level = "Gold"
            else:
                rec.level = "Silver"
