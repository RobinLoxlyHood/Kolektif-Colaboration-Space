from odoo import models, fields, api
from odoo.exceptions import ValidationError

class KolektifPenjualan(models.Model):
    _name = 'kolektif.penjualan'
    _description = 'KolektifPenjualan'
    _rec_name = 'kode'
 
    kode = fields.Char(string='Kode')
    membership = fields.Boolean(string='Apakah Member?', default = False)
    nama_nonmember = fields.Char(string='Nama')
    pelanggan_id = fields.Many2one(comodel_name='kolektif.pelanggan', 
                                   string='ID Pelanggan')
    id_member_penjualan = fields.Char(compute='_compute_id_member_penjualan', 
                                      string='Nama Member')
    tgl_transaksi = fields.Datetime(string='Tanggal Transaksi', 
                                    default=fields.Datetime.now())
    detailpenjualan_ids = fields.One2many(comodel_name='kolektif.detailpenjualan', 
                                          inverse_name='penjualan_id', 
                                          string='Detail Barang')
    total_bayar = fields.Integer(compute='_compute_total_bayar', 
                              string='Total Bayar', store=True, readonly=True)
         
    @api.depends('detailpenjualan_ids')
    def _compute_total_bayar(self):
        for rec in self:
            total = sum(self.env['kolektif.detailpenjualan']
                        .search([('penjualan_id','=',rec.id)])
                        .mapped('subtotal'))
            rec.total_bayar = total
        
 
    @api.depends('pelanggan_id')
    def _compute_id_member_penjualan(self):
        for rec in self:
            rec.id_member_penjualan = rec.pelanggan_id.kode

    def unlink(self):
        for penjualan in self:
            for detail in penjualan.detailpenjualan_ids:
                for bahanbaku in detail.menu_id.bahanbaku_ids:
                    bahanbaku_qty = bahanbaku.komposisi * detail.qty
                    bahanbaku.stock += bahanbaku_qty

        return super(KolektifPenjualan, self).unlink()
    
    def write(self, vals):
        # Check if the sale has any detail records, indicating it has been made
        for penjualan in self:
            if penjualan.detailpenjualan_ids:
                raise ValidationError('Menu yang sudah dipesan tidak bisa di ubah, Silahkan membuat Pesanan baru')

        # Continue with the normal write operation
        record = super(KolektifPenjualan, self).write(vals)
        return record
    
class KolektifDetailPenjualan(models.Model):
    _name = 'kolektif.detailpenjualan'
    _description = ''

    penjualan_id = fields.Many2one(comodel_name='kolektif.penjualan', 
                                   string='Penjualan')
    menu_id = fields.Many2one(comodel_name='kolektif.menu', 
                                string='Nama Barang')
    harga_satuan = fields.Integer(string='Harga Satuan')
    qty = fields.Integer(string='Quantity')
    subtotal = fields.Integer(compute='_compute_subtotal', 
                              string='Sub Total')
    
    @api.depends('harga_satuan','qty')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.harga_satuan * rec.qty
 
    @api.onchange('menu_id')
    def _onchange_barang(self):
        self.harga_satuan = self.menu_id.harga

    @api.constrains('qty')
    def _checkQuantity(self):
        for record in self:
            if record.qty < 1:
                raise ValidationError('Masa mau beli {} cuma {} pcs'.format(record.menu_id.nama_menu,
                                                                            record.qty))
            elif record.qty > record.menu_id.stock:
                raise ValidationError('Jumlah Barang Beli Melebihi Stock yang ada. Jumlah Stock {} {} pcs'.format(record.menu_id.nama_menu,record.menu_id.stock))
    @api.model
    def create(self, vals):
        record = super(KolektifDetailPenjualan, self).create(vals)
        if record.qty:
            # Update stock based on composition and quantity
            for bahanbaku in record.menu_id.bahanbaku_ids:
                bahanbaku_qty = bahanbaku.komposisi * record.qty
                bahanbaku.stock -= bahanbaku_qty

        return record        
    # @api.model
    # def create(self,vals):
    #     record = super(KolektifDetailPenjualan, self).create(vals)
    #     if record.qty:
    #         self.env['kolektif.menu'].search([('id', '=', record.menu_id.id)]).write({'stock' : record.menu_id.stock-record.qty})
    #     return record

