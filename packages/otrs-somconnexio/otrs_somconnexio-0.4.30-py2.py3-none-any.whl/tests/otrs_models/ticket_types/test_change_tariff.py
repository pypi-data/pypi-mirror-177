import pytest

from pyotrs.lib import DynamicField

from otrs_somconnexio.otrs_models.ticket_types.change_tariff_ticket import ChangeTariffTicket
from otrs_somconnexio.otrs_models.configurations.changes.change_tariff import ChangeTariffTicketConfiguration


class TestCaseChangeTariffTicket:
    def test_create(self, mocker):
        username = "7456787G"
        customer_code = "1234"

        OTRSClientMock = mocker.patch("otrs_somconnexio.otrs_models.ticket_types.base_ticket.OTRSClient", return_value=mocker.Mock())
        TicketMock = mocker.patch("otrs_somconnexio.otrs_models.ticket_types.base_ticket.Ticket", return_value=mocker.Mock())
        ArticleMock = mocker.patch("otrs_somconnexio.otrs_models.ticket_types.base_ticket.Article", return_value=mocker.Mock())
        DynamicFieldMock = mocker.patch("otrs_somconnexio.otrs_models.ticket_types.base_ticket.DynamicField", return_value=mocker.Mock())

        expected_ticket_data = {
            "Title": "Sol·licitud Canvi de tarifa oficina virtual",
            "Queue": ChangeTariffTicketConfiguration.queue,
            "State": ChangeTariffTicketConfiguration.state,
            "Type": ChangeTariffTicketConfiguration.type,
            "Priority": ChangeTariffTicketConfiguration.priority,
            "CustomerUser": customer_code,
            "CustomerID": customer_code,
        }
        expected_article_data = {
            "Subject": "Sol·licitud Canvi de tarifa oficina virtual",
            "Body": "-"
        }

        fields_dict = {
            "phone_number": "666666666",
            "new_product_code": "NEW_PRODUCT_CODE",
            "current_product_code": "CURRENT_PRODUCT_CODE",
            "effective_date": "tomorrow",
            "subscription_email": "fakeemail@email.coop",
        }

        ChangeTariffTicket(username, customer_code, fields_dict).create()

        TicketMock.assert_called_once_with(expected_ticket_data)
        ArticleMock.assert_called_once_with(expected_article_data)
        calls = [
            mocker.call('ProcessManagementProcessID', 'Process-f91240baa6e0146aecc70a9c97d6f84f'),
            mocker.call('ProcessManagementActivityID', 'Activity-7117b19116339f88dc43767cd477f2be'),
            mocker.call('renovaCanviTarifa', False),
            mocker.call('liniaMobil', '666666666'),
            mocker.call('productMobil', 'NEW_PRODUCT_CODE'),
            mocker.call('tarifaAntiga', 'CURRENT_PRODUCT_CODE'),
            mocker.call('dataExecucioCanviTarifa', 'tomorrow'),
            mocker.call('correuElectronic', 'fakeemail@email.coop'),
        ]
        DynamicFieldMock.assert_has_calls(calls)
        OTRSClientMock.return_value.client.ticket_create.assert_called_once_with(  # noqa
            TicketMock.return_value,
            article=ArticleMock.return_value,
            dynamic_fields=[mocker.ANY for call in calls]
        )

    def test_create_with_override_tickets(self, mocker):
        username = "7456787G"
        customer_code = "1234"

        OTRSClientMock = mocker.patch("otrs_somconnexio.otrs_models.ticket_types.base_ticket.OTRSClient", return_value=mocker.Mock())
        TicketMock = mocker.patch("otrs_somconnexio.otrs_models.ticket_types.base_ticket.Ticket", return_value=mocker.Mock())
        ArticleMock = mocker.patch("otrs_somconnexio.otrs_models.ticket_types.base_ticket.Article", return_value=mocker.Mock())
        DynamicFieldMock = mocker.patch("otrs_somconnexio.otrs_models.ticket_types.base_ticket.DynamicField", return_value=mocker.Mock())

        expected_ticket_data = {
            "Title": "Sol·licitud Canvi de tarifa oficina virtual",
            "Queue": ChangeTariffTicketConfiguration.queue,
            "State": ChangeTariffTicketConfiguration.state,
            "Type": ChangeTariffTicketConfiguration.type,
            "Priority": ChangeTariffTicketConfiguration.priority,
            "CustomerUser": customer_code,
            "CustomerID": customer_code,
        }
        expected_article_data = {
            "Subject": "Sol·licitud Canvi de tarifa oficina virtual",
            "Body": "-"
        }

        fields_dict = {
            "phone_number": "666666666",
            "new_product_code": "NEW_PRODUCT_CODE",
            "current_product_code": "CURRENT_PRODUCT_CODE",
            "effective_date": "tomorrow",
            "subscription_email": "fakeemail@email.coop",
        }

        ChangeTariffTicket(username, customer_code, fields_dict, override_ticket_ids=[1,2]).create()

        TicketMock.assert_called_once_with(expected_ticket_data)
        ArticleMock.assert_called_once_with(expected_article_data)
        calls = [
            mocker.call('ProcessManagementProcessID', 'Process-f91240baa6e0146aecc70a9c97d6f84f'),
            mocker.call('ProcessManagementActivityID', 'Activity-7117b19116339f88dc43767cd477f2be'),
            mocker.call('renovaCanviTarifa', True),
            mocker.call('liniaMobil', '666666666'),
            mocker.call('productMobil', 'NEW_PRODUCT_CODE'),
            mocker.call('tarifaAntiga', 'CURRENT_PRODUCT_CODE'),
            mocker.call('dataExecucioCanviTarifa', 'tomorrow'),
            mocker.call('correuElectronic', 'fakeemail@email.coop'),
        ]
        DynamicFieldMock.assert_has_calls(calls)
        OTRSClientMock.return_value.client.ticket_create.assert_called_once_with(  # noqa
            TicketMock.return_value,
            article=ArticleMock.return_value,
            dynamic_fields=[mocker.ANY for call in calls]
        )

    def test_get_search_args(self):
        username = "7456787G"
        customer_code = "1234"

        search_args = ChangeTariffTicket(username, customer_code, fields_dict={}).get_search_args()
        assert search_args["dynamic_fields"][0].value == ChangeTariffTicketConfiguration.process_id
        assert search_args["dynamic_fields"][1].value == ChangeTariffTicketConfiguration.activity_id
        assert search_args["Queues"][0] == ChangeTariffTicketConfiguration.queue
        assert search_args["States"][0] == ChangeTariffTicketConfiguration.state
