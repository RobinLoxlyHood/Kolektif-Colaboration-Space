from odoo import models, fields, api

class KolektifMenu(models.Model):
    _name = 'kolektif.menu'
    _description = 'KolektifMenu'
    _rec_name = 'nama_menu'

    kode = fields.Char(string='Kode Menu')
    nama_menu = fields.Char(string='Nama Menu')
    deskripsi = fields.Char(string='Deskripsi Barang')
    jenis = fields.Many2one(comodel_name='kolektif.jenismenu', 
                            string='Kelompok Menu')
    stock = fields.Integer(string='Stock Menu'
                            #,readonly=True
                           )
    harga = fields.Integer(string='Harga Menu')
    harga_modal = fields.Integer(string='Harga Modal Menu')
    bahanbaku_ids = fields.One2many(comodel_name='kolektif.bahanbaku', inverse_name='menu_id', string='Daftar Bahan Baku', store=True)


