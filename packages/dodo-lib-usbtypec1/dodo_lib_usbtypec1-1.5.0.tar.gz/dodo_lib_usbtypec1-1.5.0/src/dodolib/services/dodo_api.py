import datetime
import uuid
from typing import Iterable
from uuid import UUID

from pydantic import parse_obj_as

from .base import BaseHTTPService
from .. import models
from ..utils import exceptions

__all__ = (
    'DodoAPIClient',
)


class DodoAPIClient(BaseHTTPService):
    service_name = 'DODO_API'

    async def get_partial_delivery_statistics(
            self,
            cookies: dict,
            unit_ids: Iterable[int],
    ) -> models.DeliveryPartialStatisticsReport:
        url = '/v1/reports/awaiting-orders'
        body = {'cookies': cookies, 'unit_ids': tuple(unit_ids)}
        response = await self._client.post(url, json=body)
        return models.DeliveryPartialStatisticsReport.parse_obj(response.json())

    async def get_partial_kitchen_statistics(
            self,
            cookies: dict,
            unit_ids: Iterable[int],
    ) -> models.KitchenPartialStatisticsReport:
        url = '/v1/reports/kitchen-productivity'
        body = {'cookies': cookies, 'unit_ids': tuple(unit_ids)}
        response = await self._client.post(url, json=body)
        return models.KitchenPartialStatisticsReport.parse_obj(response.json())

    async def _get_stop_sales_by_token(
            self,
            url: str,
            token: str,
            unit_uuids: Iterable[UUID],
    ) -> dict | list:
        params = {'token': token, 'unit_uuids': unit_uuids}
        response = await self._client.get(url, params=params)
        if response.is_server_error:
            raise exceptions.DodoAPIError
        return response.json()

    async def _get_stop_sales_by_cookies(
            self,
            url: str,
            cookies: models.Cookies,
            unit_ids: Iterable[int],
            start: datetime.datetime,
            end: datetime.datetime,
    ) -> dict | list:
        body = {'cookies': cookies, 'unit_ids': unit_ids, 'start': start.isoformat(), 'end': end.isoformat()}
        response = await self._client.post(url, json=body)
        if response.is_server_error:
            raise exceptions.DodoAPIError
        return response.json()

    async def get_stop_sales_by_ingredients(
            self,
            token: str,
            unit_uuids: Iterable[UUID],
    ) -> list[models.StopSaleByIngredients]:
        url = '/v2/stop-sales/ingredients'
        response_json = await self._get_stop_sales_by_token(url, token, unit_uuids)
        return parse_obj_as(list[models.StopSaleByIngredients], response_json)

    async def get_stop_sales_by_sales_channels(
            self,
            token: str,
            unit_uuids: Iterable[UUID],
    ) -> list[models.StopSaleBySalesChannels]:
        url = '/v2/stop-sales/channels'
        response_json = await self._get_stop_sales_by_token(url, token, unit_uuids)
        return parse_obj_as(list[models.StopSaleBySalesChannels], response_json)

    async def get_stop_sales_by_sectors(
            self,
            cookies: models.Cookies,
            unit_ids: Iterable[int],
            start: datetime.datetime,
            end: datetime.datetime,
    ) -> list[models.StopSaleBySectors]:
        url = '/v1/stop-sales/sectors'
        response_json = await self._get_stop_sales_by_cookies(url, cookies, unit_ids, start, end)
        return parse_obj_as(list[models.StopSaleBySectors], response_json)

    async def get_stop_sales_by_streets(
            self,
            cookies: models.Cookies,
            unit_ids: Iterable[int],
            start: datetime.datetime,
            end: datetime.datetime,
    ) -> list[models.StopSaleByStreets]:
        url = '/v1/stop-sales/streets'
        response_json = await self._get_stop_sales_by_cookies(url, cookies, unit_ids, start, end)
        return parse_obj_as(list[models.StopSaleByStreets], response_json)

    async def get_stocks_balance(
            self,
            cookies: models.Cookies,
            unit_ids: Iterable[int],
            days_left_threshold: int,
    ) -> models.StockBalanceStatistics:
        body = {
            'cookies': cookies,
            'unit_ids': unit_ids,
            'days_left_threshold': days_left_threshold,
        }
        response = await self._client.post('/stocks/', json=body)
        if response.is_server_error:
            raise exceptions.DodoAPIError
        return models.StockBalanceStatistics.parse_obj(response.json())

    async def get_stop_sales_by_channels(
            self,
            token: str,
            unit_uuids: Iterable[UUID],
    ) -> list[models.StopSaleBySalesChannels]:
        params = {'token': token, 'unit_uuids': unit_uuids}
        response = await self._client.get('/v2/stop-sales/channels', params=params)
        if response.is_server_error:
            raise exceptions.DodoAPIError
        return parse_obj_as(list[models.StopSaleBySalesChannels], response.json())

    async def get_cheated_orders(
            self,
            cookies: models.Cookies,
            unit_ids_and_names: Iterable[models.UnitIdAndName],
            repeated_phones_count_threshold: int,
    ) -> list[models.CheatedOrders]:
        body = {
            'cookies': cookies,
            'units': unit_ids_and_names,
            'repeated_phone_number_count_threshold': repeated_phones_count_threshold,
        }
        response = await self._client.post('/v1/cheated-orders', json=body)
        if response.is_server_error:
            raise exceptions.DodoAPIError
        return parse_obj_as(list[models.CheatedOrders], response.json())

    async def get_canceled_orders(
            self,
            cookies: models.Cookies,
    ):
        body = {'cookies': cookies}
        response = await self._client.post('/v1/canceled-orders', json=body)
        if response.is_server_error:
            raise exceptions.DodoAPIError
        return parse_obj_as(list[models.OrderByUUID], response.json())

    async def get_delivery_speed_statistics(
            self,
            token: str,
            country_code: str,
            unit_uuids: Iterable[UUID],
    ) -> list[models.UnitDeliverySpeed]:
        url = f'/v2/{country_code}/reports/delivery-speed'
        params = {'unit_uuids': tuple(unit_uuids)}
        headers = {'Authorization': f'Bearer {token}'}
        response = await self._client.get(url, params=params, headers=headers)
        if response.is_server_error:
            raise exceptions.DodoAPIError
        return parse_obj_as(list[models.UnitDeliverySpeed], response.json())

    async def get_orders_handover_time_statistics(
            self,
            token: str,
            unit_uuids: Iterable[UUID],
            sales_channels: Iterable[models.SalesChannel | str],
    ) -> list[models.UnitOrdersHandoverTime]:
        url = '/v2/statistics/production/handover-time'
        params = {'token': token, 'unit_uuids': tuple(unit_uuids),
                  'sales_channels': [sales_channel.value for sales_channel in sales_channels]}
        response = await self._client.get(url, params=params)
        if response.is_server_error:
            raise exceptions.DodoAPIError
        return parse_obj_as(list[models.UnitOrdersHandoverTime], response.json())

    async def get_revenue_statistics(
            self,
            country_code: str,
            unit_ids: Iterable[int],
    ) -> models.RevenueStatistics:
        url = f'/v1/{country_code}/reports/revenue'
        params = {'unit_ids': tuple(unit_ids)}
        response = await self._client.get(url, params=params)
        if response.is_server_error:
            raise exceptions.DodoAPIError
        return models.RevenueStatistics.parse_obj(response.json())

    async def get_kitchen_production_statistics(
            self,
            cookies: models.Cookies,
            unit_ids: Iterable[int],
    ) -> models.KitchenProductionStatistics:
        url = '/v1/statistics/production/kitchen'
        body = {'cookies': cookies, 'unit_ids': tuple(unit_ids)}
        response = await self._client.post(url, json=body)
        if response.is_server_error:
            raise exceptions.DodoAPIError
        return models.KitchenProductionStatistics.parse_obj(response.json())

    async def get_kitchen_performance_statistics(
            self,
            cookies: models.Cookies,
            unit_ids: Iterable[int],
    ) -> models.KitchenPerformanceStatistics:
        url = '/v1/statistics/kitchen/performance'
        body = {'cookies': cookies, 'unit_ids': tuple(unit_ids)}
        response = await self._client.post(url, json=body)
        if response.is_server_error:
            raise exceptions.DodoAPIError
        return models.KitchenPerformanceStatistics.parse_obj(response.json())

    async def get_delivery_productivity_statistics(
            self,
            token: str,
            country_code: str,
            unit_uuids: Iterable[uuid.UUID]
    ) -> list[models.UnitDeliveryProductivityStatistics]:
        url = f'/v2/{country_code}/reports/delivery-productivity'
        params = {'unit_uuids': tuple(unit_uuids)}
        headers = {'Authorization': f'Bearer {token}'}
        response = await self._client.get(url, params=params, headers=headers)
        if response.is_server_error:
            raise exceptions.DodoAPIError
        return parse_obj_as(list[models.UnitDeliveryProductivityStatistics], response.json())

    async def get_heated_shelf_time_statistics(
            self,
            token: str,
            country_code: str,
            unit_uuids: Iterable[uuid.UUID],
    ) -> list[models.UnitHeatedShelfStatistics]:
        url = f'/v2/{country_code}/reports/heated-shelf-time'
        params = {'unit_uuids': tuple(unit_uuids)}
        headers = {'Authorization': f'Bearer {token}'}
        response = await self._client.get(url, params=params, headers=headers)
        if response.is_server_error:
            raise exceptions.DodoAPIError
        return parse_obj_as(list[models.UnitHeatedShelfStatistics], response.json())

    async def get_restaurant_cooking_time_statistics(
            self,
            token: str,
            country_code: str,
            unit_uuids: Iterable[uuid.UUID],
    ) -> list[models.UnitRestaurantCookingTimeStatistics]:
        url = f'/v2/{country_code}/reports/restaurant-cooking-time'
        params = {'unit_uuids': tuple(unit_uuids)}
        headers = {'Authorization': f'Bearer {token}'}
        response = await self._client.get(url, params=params, headers=headers)
        if response.is_server_error:
            raise exceptions.DodoAPIError
        return parse_obj_as(list[models.UnitRestaurantCookingTimeStatistics], response.json())

    async def get_couriers_statistics(
            self,
            cookies: models.Cookies,
            unit_ids: Iterable[int],
    ) -> models.CouriersStatistics:
        url = '/v1/statistics/delivery/couriers'
        body = {'cookies': cookies, 'unit_ids': tuple(unit_ids)}
        response = await self._client.post(url, json=body)
        if response.is_server_error:
            raise exceptions.DodoAPIError
        return models.CouriersStatistics.parse_obj(response.json())

    async def get_bonus_system_statistics(
            self,
            cookies: models.Cookies,
            unit_ids_and_names: Iterable[models.UnitIdAndName],
    ) -> list[models.UnitBonusSystem]:
        url = '/v1/reports/bonus-system'
        body = {'cookies': cookies, 'units': tuple(unit_ids_and_names)}
        response = await self._client.post(url, json=body)
        if response.is_server_error:
            raise exceptions.DodoAPIError
        return parse_obj_as(list[models.UnitBonusSystem], response.json())

    async def get_being_late_certificates_statistics(
            self,
            token: str,
            country_code: str,
            unit_uuids: Iterable[uuid.UUID]
    ) -> list[models.UnitBeingLateCertificates]:
        url = f'/v2/{country_code}/reports/being-late-certificates'
        headers = {'Authorization': f'Bearer {token}'}
        params = {'unit_uuids': unit_uuids}
        response = await self._client.get(url, params=params, headers=headers)
        if response.is_server_error:
            raise exceptions.DodoAPIError
        return parse_obj_as(list[models.UnitBeingLateCertificates], response.json())

    async def get_productivity_balance_statistics(
            self,
            token: str,
            country_code: str,
            unit_uuids: Iterable[uuid.UUID],
    ) -> list[models.UnitProductivityBalanceStatistics]:
        url = f'/v2/{country_code}/reports/productivity-balance'
        headers = {'Authorization': f'Bearer {token}'}
        params = {'unit_uuids': tuple(unit_uuids)}
        response = await self._client.get(url, params=params, headers=headers)
        if response.is_server_error:
            raise exceptions.DodoAPIError
        return parse_obj_as(list[models.UnitProductivityBalanceStatistics], response.json())
