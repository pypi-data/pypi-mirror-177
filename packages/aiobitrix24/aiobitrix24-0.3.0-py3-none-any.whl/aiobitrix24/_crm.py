from __future__ import annotations

from dataclasses import dataclass

from aiobitrix24 import methods
from aiobitrix24._bitrix24 import bx24
from aiobitrix24._builders import MAX_BATCH_SIZE, BatchQuery, build_chunks
from aiobitrix24.exceptions import BadBitrixResponseError


@dataclass
class CRMItem:
    """Item in bitrix crm smart process."""

    fields: dict
    name: str | None = None

    @classmethod
    async def select(cls, process_id: int, filters: dict) -> list[CRMItem]:
        """Select all items from process satisfying filters.

        :param process_id: smart process id in bitrix
        :param filters: filters like in crm docs
        :raises BadBitrixResponseError: No result in response from bitrix
        :return: list of selected smart process items
        """
        query_params = {
            "start": 0,
            "entityTypeId": process_id,
            "select": ["*"],
            "filter": filters,
        }
        response = await bx24.request(
            methods.CRM_ITEM_LIST,
            query_params,
            is_query_complex=True,
        )
        response_result = response.json()
        if "result" not in response_result:
            raise BadBitrixResponseError("No result in response")
        crm_items = [CRMItem(fields) for fields in response_result["result"]["items"]]
        for page in range(MAX_BATCH_SIZE, response_result["total"], MAX_BATCH_SIZE):
            query_params["start"] = page
            response = await bx24.request(
                methods.CRM_ITEM_LIST,
                query_params,
                is_query_complex=True,
            )
            response_result = response.json()
            page_items = [
                CRMItem(fields) for fields in response_result["result"]["items"]
            ]
            crm_items.extend(page_items)
        return crm_items

    @classmethod
    async def batch_update(cls, crm_items: list[CRMItem]) -> None:
        """Update crm items by batch requests.

        :param crm_items: list of crm items for update
        """
        queries = []
        for crm_item in crm_items:
            query_params = {
                "entityTypeId": crm_item.fields["entityTypeId"],
                "id": crm_item.fields["id"],
            }
            fields = dict(crm_item.fields)
            fields.pop("id")
            query_params["fields"] = fields
            queries.append(
                BatchQuery(
                    crm_item.fields["id"],
                    methods.CRM_ITEM_UPDATE,
                    query_params,
                ),
            )
        for chunk in build_chunks(queries):
            await bx24.batch_request(chunk)
