from pyotrs.lib import DynamicField

from .base_customer_ticket import BaseCustomerTicket

from otrs_somconnexio.otrs_models.configurations.changes.change_tariff import ChangeTariffTicketConfiguration


class ChangeTariffTicket(BaseCustomerTicket):
    def __init__(self, username, customer_code, fields_dict, override_ticket_ids=[], fallback_path="/tmp/tickets/"):
        super(ChangeTariffTicket, self).__init__(
            username,
            customer_code,
            fields_dict,
            override_ticket_ids,
            fallback_path)
        self.configuration = ChangeTariffTicketConfiguration()

    def get_search_args(self):
        return {
            "dynamic_fields": [
                DynamicField("ProcessManagementProcessID", self.configuration.process_id),
                DynamicField("ProcessManagementActivityID", self.configuration.activity_id),
            ],
            "Queues": [self.configuration.queue],
            "States": [self.configuration.state],
        }

    def _get_subject(self):
        return "Sol·licitud Canvi de tarifa oficina virtual"

    def _get_dynamic_fields(self):
        return {
            "renovaCanviTarifa": len(self.override_ticket_ids) > 0,
            "liniaMobil": self.fields["phone_number"],
            "productMobil": self.fields["new_product_code"],
            "tarifaAntiga": self.fields["current_product_code"],
            "dataExecucioCanviTarifa": self.fields["effective_date"],
            "correuElectronic": self.fields["subscription_email"],
        }
