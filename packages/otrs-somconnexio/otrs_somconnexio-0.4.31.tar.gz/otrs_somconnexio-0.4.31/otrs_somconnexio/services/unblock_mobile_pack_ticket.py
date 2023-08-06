# coding: utf-8
from pyotrs.lib import DynamicField

from otrs_somconnexio.client import OTRSClient


class UnblockMobilePackTicket:
    """
    Unblock the mobile pack tickets.

    Once the fiber provisioning is closed, we can start with the mobile provisioning to complete
    the pack products.
    Unblock is to change the DynamicField_recuperarProvisio to 1
    """

    def __init__(self, ticket_number, introduced_date):
        self.ticket_number = ticket_number
        self.introduced_date = introduced_date

    def run(self):
        otrs_client = OTRSClient()
        ticket = otrs_client.get_ticket_by_number(
            self.ticket_number, dynamic_fields=True
        )

        otrs_client.update_ticket(
            ticket.tid,
            article=None,
            dynamic_fields=self._prepare_dynamic_fields(ticket),
        )

    def _prepare_dynamic_fields(self, ticket):
        dynamic_fields = [
            DynamicField(name='recuperarProvisio', value=1),
        ]
        if bool(ticket.dynamic_field_get("SIMrebuda").value):
            dynamic_fields.append(
                DynamicField(name="dataIntroPlataforma", value=self.introduced_date),
            )
        return dynamic_fields
