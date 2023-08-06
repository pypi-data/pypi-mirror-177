# coding: utf-8
class ChangeTariffTicketConfiguration:
    process_id = "Process-f91240baa6e0146aecc70a9c97d6f84f"
    activity_id = "Activity-7117b19116339f88dc43767cd477f2be"
    type = "Sin Clasificar"
    queue = "Oficina Virtual::Canvi Tarifa mòbil::Rebut"
    state = "new"
    priority = "3 normal"

    def __init__(self, otrs_configuration=None):
        if otrs_configuration:
            self.process_id = otrs_configuration.adsl_process_id
            self.activity_id = otrs_configuration.adsl_activity_id
            self.type = otrs_configuration.adsl_ticket_type
            self.queue = otrs_configuration.adsl_ticket_queue
            self.state = otrs_configuration.adsl_ticket_state
            # We need to mantain this typo because is in a Tryton model field.
            self.priority = otrs_configuration.adsl_ticket_proprity
