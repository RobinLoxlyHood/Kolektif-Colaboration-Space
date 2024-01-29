from odoo import models, fields, api

class KolektifPembelian(models.Model):
    _name = 'kolektif.pembelian'
    _description = 'KolektifPembelian'
    _rec_name = 'referensi'


    # referensi = fields.Char(
    #     string="No. Reference",
    #     required=True, copy=False, readonly=True,
    #     default=lambda self: ('New'))
    referensi = fields.Char(string='Referensi')
    bahanbaku_id = fields.Many2one(comodel_name='kolektif.bahanbaku', string='Daftar Bahan Baku')
    supplier_id = fields.Many2one(comodel_name='kolektif.supplier', string='Daftar Supplier')
    tgl_transaksi = fields.Date(string='Tanggal Transaksi',
                                    default=fields.Date.today())
    modal = fields.Integer(compute='_compute_modal', string='Harga Modal')
    qty_bayar = fields.Integer(string='Quantity Beli')
    
    bayar = fields.Integer(compute='_compute_bayar', string='Total bayar')
    
    
    @api.depends('bahanbaku_id')
    def _compute_modal(self):
        for rec in self:
            rec.modal = rec.bahanbaku_id.harga

    @api.depends('bahanbaku_id', 'qty_bayar')
    def _compute_bayar(self):
        for rec in self:
            rec.bayar = rec.bahanbaku_id.harga * rec.qty_bayar
    @api.model
    def create(self, vals):
        # if vals.get('referensi', ("New")) == ("New"):                
        #     vals['referensi'] = self.env['ir.sequence'].next_by_code('referensi.pembelian') or _("New")
        record = super(KolektifPembelian, self).create(vals)
        if record.qty_bayar:
            # Update stock in doodex.barang model
            record.bahanbaku_id.stock += record.qty_bayar
        return record
    
    def unlink(self):
        for r in self:
            r.bahanbaku_id.stock -= r.qty_bayar
        record = super(KolektifPembelian, self).unlink()
    
    @api.onchange('bahanbaku_id')
    def _onchange_barang(self):
        id_supplier=self.bahanbaku_id.supplier_ids
        ids_supplier = []
        for i in id_supplier:
            ids_supplier.append(i.id)
        return {'domain':{'supplier_id':[('id','in',ids_supplier)]}}
