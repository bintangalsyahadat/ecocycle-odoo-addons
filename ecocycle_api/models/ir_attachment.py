from odoo import api, fields, models


class IrAttachment(models.Model):
    _name = 'ir.attachment'
    _inherit = ['ir.attachment', 'api.record']

    def _get_attachment(self, record, filename, datas, mimetype):
        attachment = self.env['ir.attachment'].search([
            ('res_model', '=', record._name),
            ('res_id', '=', record.id),
            ('mimetype', '=', mimetype),
        ])

        if not attachment and record:
            attachment = self.env['ir.attachment'].sudo().create({
                'name': filename,
                'type': 'binary',
                'datas': datas,
                'res_model': record._name,
                'res_id': record.id,
                'mimetype': mimetype,
            })
        return attachment

    def _remove_attachment(self, record, mimetype):
        self.env['ir.attachment'].search([
            ('res_model', '=', record._name),
            ('res_id', '=', record.id),
            ('mimetype', '=', mimetype),
        ]).unlink()
