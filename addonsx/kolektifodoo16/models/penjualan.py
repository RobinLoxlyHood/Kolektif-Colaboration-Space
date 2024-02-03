from odoo import models, fields, api, _
try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None

from io import BytesIO

from odoo.exceptions import ValidationError, UserError


class KolektifPenjualan(models.Model):
    _name = 'kolektif.penjualan'
    _description = 'RestoPenjualan'
    _rec_name = 'kode_penjualan'
    
    qr_code = fields.Char(compute='_compute_qr_code', string='QR Code', store = False)    
    kode_penjualan = fields.Char(string="Kode Penjualan",
                                 required=True, 
                                 copy=False, 
                                 readonly=True,
                                 default=lambda self: _('New'))    
    nama = fields.Char(string='Nama Pembeli')
    membership = fields.Boolean(string='Apakah member ?', default = True)
    pelanggan_id = fields.Many2one(comodel_name='kolektif.pelanggan', string='ID Pelanggan')
    id_member_penjualan = fields.Char(compute='_compute_id_member_penjualan', 
                                      string='Nama Member') 
    tgl_transaksi = fields.Datetime(string='Tanggal Transaksi', default=fields.Datetime.now())
    total_bayar = fields.Integer(compute='_compute_total_bayar', string='Total Bayar', store=True)
    restodetailpenjualanmakanan_ids = fields.One2many(comodel_name='kolektif.detailpenjualanmakanan', inverse_name='restopenjualanmakanan_id', string='Detail Penjualan Makanan')
    restodetailpenjualanminuman_ids = fields.One2many(comodel_name='kolektif.detailpenjualanminuman', inverse_name='restopenjualanminuman_id', string='Detail Penjualan Minuman')
    
    @api.depends('pelanggan_id')
    def _compute_id_member_penjualan(self):
        for rec in self:
            rec.id_member_penjualan = rec.pelanggan_id.nama_pelanggan

    @api.depends('kode_penjualan')
    def _compute_qr_code(self):
        for rec in self:
            if qrcode and base64:
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=4)
                qr.add_data(rec.kode_penjualan)
                qr.make(fit=True)
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())
                rec.update({'qr_code': qr_image})
    
    @api.depends('restodetailpenjualanmakanan_ids','restodetailpenjualanminuman_ids')
    def _compute_total_bayar(self):
        for rec in self:
            a = self.env['kolektif.detailpenjualanmakanan'].search([('restopenjualanmakanan_id','=',rec.id)]).mapped('subtotal')   
            b = self.env['kolektif.detailpenjualanminuman'].search([('restopenjualanminuman_id','=',rec.id)]).mapped('subtotal')        
            total = sum(a) + sum(b)
            rec.total_bayar = total

    @api.model
    def create(self,vals):        
        if vals.get('kode_penjualan', _("New")) == _("New"):   
            membership = vals.get('membership',False)
            if membership == True:            
                vals['kode_penjualan'] = self.env['ir.sequence'].next_by_code('kolektifodoo16.referensi.penjualan_member') or _("New")    
            else:
                vals['kode_penjualan'] = self.env['ir.sequence'].next_by_code('kolektifodoo16.referensi.penjualan_nonmember') or _("New")
        record = super(KolektifPenjualan, self).create(vals)
        return record

    def unlink(self):
        if self.restodetailpenjualanmakanan_ids:
            a = []
            for detail in self.restodetailpenjualanmakanan_ids:
                a = self.env['kolektif.makanan'].search([('id','=',detail.restomakanan_id.id)]).mapped('restomakanandetail_ids')   
                for rec in a:
                    self.env['kolektif.bahanbaku'].search([('id','=',rec.restobahan_id.id)]).write({'stok': rec.restobahan_id.stok + (rec.kebutuhan * detail.qty)})
        if self.restodetailpenjualanminuman_ids:
            a = []
            for detail in self.restodetailpenjualanminuman_ids:
                a = self.env['kolektif.minuman'].search([('id','=',detail.restominuman_id.id)]).mapped('restominumandetail_ids')   
                for rec in a:
                    self.env['kolektif.bahanbaku'].search([('id','=',rec.restobahan_id.id)]).write({'stok': rec.restobahan_id.stok + (rec.kebutuhan * detail.qty)})
        record = super(KolektifPenjualan, self).unlink()

    def write(self, vals):
        if self.restodetailpenjualanmakanan_ids:
            for rec in self.restodetailpenjualanmakanan_ids:
                if rec :
                    a = self.env['kolektif.makanan'].search([('id','=',rec.restomakanan_id.id)]).mapped('restomakanandetail_ids')   
                    for detail in a:
                        self.env['kolektif.bahanbaku'].search([('id','=',detail.restobahan_id.id)]).write({'stok': detail.restobahan_id.stok + (detail.kebutuhan * rec.qty)})
        if self.restodetailpenjualanminuman_ids:
            for rec in self.restodetailpenjualanminuman_ids:
                if rec :
                    a = self.env['kolektif.minuman'].search([('id','=',rec.restominuman_id.id)]).mapped('restominumandetail_ids')   
                    for detail in a:
                        self.env['kolektif.bahanbaku'].search([('id','=',detail.restobahan_id.id)]).write({'stok': detail.restobahan_id.stok + (detail.kebutuhan * rec.qty)})
        record = super(KolektifPenjualan, self).write(vals)
        if self.restodetailpenjualanmakanan_ids:
            for rec in self.restodetailpenjualanmakanan_ids:
                if rec :
                    a = self.env['kolektif.makanan'].search([('id','=',rec.restomakanan_id.id)]).mapped('restomakanandetail_ids')   
                    for detail in a:
                        self.env['kolektif.bahanbaku'].search([('id','=',detail.restobahan_id.id)]).write({'stok': detail.restobahan_id.stok - (detail.kebutuhan * rec.qty)})
        if self.restodetailpenjualanminuman_ids:
            for rec in self.restodetailpenjualanminuman_ids:
                if rec :
                    a = self.env['kolektif.minuman'].search([('id','=',rec.restominuman_id.id)]).mapped('restominumandetail_ids')   
                    for detail in a:
                        self.env['kolektif.bahanbaku'].search([('id','=',detail.restobahan_id.id)]).write({'stok': detail.restobahan_id.stok - (detail.kebutuhan * rec.qty)})
        return record

class KolektifDetailPenjualanMakanan(models.Model):
    _name = 'kolektif.detailpenjualanmakanan'
    _description = 'DetailPenjualanMakanan'
    _rec_name = 'restomakanan_id'

    restomakanan_id = fields.Many2one(comodel_name='kolektif.makanan', string='Nama Makanan')
    restopenjualanmakanan_id = fields.Many2one(comodel_name='kolektif.penjualan', string='Penjualan Makanan')
    
    qty = fields.Integer(string='Quantity')
    subtotal = fields.Integer(compute='_compute_subtotal', string='Sub Total')
    
    @api.depends('restomakanan_id','qty')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.qty * rec.restomakanan_id.harga    
    
    @api.model
    def create(self, vals):    
        record = super(KolektifDetailPenjualanMakanan, self).create(vals)   
        a = self.env['kolektif.makanan'].search([('id','=',record.restomakanan_id.id)]).mapped('restomakanandetail_ids')   
        for rec in a:
            self.env['kolektif.bahanbaku'].search([('id','=',rec.restobahan_id.id)]).write({'stok': rec.restobahan_id.stok - (rec.kebutuhan * record.qty)})
        return record
    
    @api.constrains('qty')
    def _checkQuantity(self):
        for record in self:
            if record.qty < 1:
                raise ValidationError('Masa mau beli {} cuma {} pcs'.format(record.restomakanan_id.name,
                                                                            record.qty))


class KolektifDetailPenjualanMinuman(models.Model):
    _name = 'kolektif.detailpenjualanminuman'
    _description = 'RestoDetailPenjualanMinuman'
    _rec_name = 'restominuman_id'
    
    restominuman_id = fields.Many2one(comodel_name='kolektif.minuman', string='Nama Minuman')
    restopenjualanminuman_id = fields.Many2one(comodel_name='kolektif.penjualan', string='Penjualan Minuman')
    qty = fields.Integer(string='Quantity')
    subtotal = fields.Integer(compute='_compute_subtotal', string='Sub Total')
    
    @api.depends('restominuman_id','qty')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.qty * rec.restominuman_id.harga

    @api.model
    def create(self, vals):    
        record = super(KolektifDetailPenjualanMinuman, self).create(vals)   
        a = self.env['kolektif.minuman'].search([('id','=',record.restominuman_id.id)]).mapped('restominumandetail_ids')   
        for rec in a:
            self.env['kolektif.bahanbaku'].search([('id','=',rec.restobahan_id.id)]).write({'stok': rec.restobahan_id.stok - (rec.kebutuhan * record.qty)})
        return record