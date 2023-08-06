from .base_ticket import BaseTicket


class BaseCustomerTicket(BaseTicket):
    def _get_process_management_dynamic_fields(self):
        result = {
            "ProcessManagementProcessID": self.configuration.process_id,
            "ProcessManagementActivityID": self.configuration.activity_id,
        }

        for k, v in dict(result).items():
            if v is None:
                del result[k]

        return result
