import json
from odoo import http
from odoo.http import request, Response


class XenditCallbackController(http.Controller):

    @http.route('/payment/xendit/callback', type='http', auth='public', csrf=False)
    def xendit_callback(self, **kw):
        raw_body = request.httprequest.get_data()

        # parse JSON body
        try:
            data = json.loads(raw_body.decode("utf-8"))
        except Exception as e:
            return Response(
                json.dumps({"success": False, "error": "Invalid JSON", "details": str(e)}),
                content_type='application/json;charset=utf-8',
                status=400
            )

        external_id = data.get("external_id")
        status = data.get("status")

        if not external_id:
            return Response(
                json.dumps({"success": False, "error": "Missing external_id"}),
                content_type='application/json;charset=utf-8',
                status=400
            )

        # example: "invoice-15" → ambil 15
        try:
            payment_transaction_id = int(external_id.split("-")[-1])
        except:
            return Response(
                json.dumps({"success": False, "error": "Invalid external_id format"}),
                content_type='application/json;charset=utf-8',
                status=400
            )

        payment_transaction = request.env["payment.transaction"].sudo().browse(payment_transaction_id)

        if payment_transaction.exists():
            payment_transaction.sudo().action_update_xendit_status(status)

        return Response(
            json.dumps({"success": True}),
            content_type='application/json;charset=utf-8'
        )
