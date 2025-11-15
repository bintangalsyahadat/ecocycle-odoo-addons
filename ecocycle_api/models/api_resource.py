# -*- coding: utf-8 -*-
import logging
import uuid
from typing import Optional

from pydantic import BaseModel
from odoo import models, fields, api, _
from odoo.osv.expression import AND
from odoo.exceptions import UserError, ValidationError

from ..utils.records import find_record

_logger = logging.getLogger(__name__)


class APIResource(models.AbstractModel):
    """Base abstract model for API-related operations."""
    _name = "api.resource"
    _description = "API Resource"

    api_id = fields.Char(
        string="API Reference",
        compute="_generate_api_id",
        store=True,
        precompute=True,
        copy=False,
        index=True,
    )

    # ------------------------------------------------------------
    # Compute Methods
    # ------------------------------------------------------------
    def _generate_api_id(self):
        """Assign a unique identifier to the record if not set."""
        for rec in self:
            if not rec.api_id:
                rec.api_id = uuid.uuid4().hex

    # ------------------------------------------------------------
    # API Methods
    # ------------------------------------------------------------
    @api.model
    def _fetch_api_records(self, **kwargs):
        """
        Retrieve records based on domain and search parameters.

        Args:
            kwargs: Optional dictionary containing:
                - base_domain: base search domain
                - search_params: dict of search args (domain, limit, etc)

        Returns:
            Tuple of (recordset, total_count)
        """
        base_domain = kwargs.get("base_domain", [])
        search_params = dict(kwargs.get("search_params", {}))

        # Merge base domain with provided domain
        user_domain = search_params.get("domain", None)
        if isinstance(user_domain, list):
            search_params["domain"] = AND([base_domain, user_domain])
        else:
            search_params["domain"] = base_domain

        recs = self.search(**search_params)
        total = self.search_count(base_domain)
        return recs, total

    @api.model
    def _create_api_record(self, payload=None, values=None):
        """
        Create a new record using either a Pydantic body or a plain dict.
        """
        return self.create([self._prepare_api_values(payload, values)])

    @api.model
    def _update_api_record(self, api_id, payload=None, values=None):
        """
        Update an existing record by its unique API reference.
        """
        rec = find_record(self.env, str(self._name), api_id)
        if rec:
            rec.write(self._prepare_api_values(payload, values))
        return rec

    @api.model
    def _prepare_api_values(self, payload: Optional[BaseModel] = None, values: Optional[dict] = None):
        """
        Convert a Pydantic body into a dict of values, or return values directly.
        """
        if payload:
            use_alias = self.env.context.get("use_alias", True)
            return payload.model_dump(by_alias=use_alias, exclude_none=True)
        return values or {}
