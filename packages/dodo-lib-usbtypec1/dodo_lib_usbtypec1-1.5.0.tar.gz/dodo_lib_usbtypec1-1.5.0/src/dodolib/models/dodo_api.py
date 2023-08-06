"""
- Statistics:
    - By tokens and unit UUIDs:
        - OrdersHandoverTimeStatistics
            - UnitOrdersHandoverTime
        - DeliverySpeedStatistics
            - UnitDeliverySpeed
    - By cookies, unit ids and unit names:
        - BeingLateCertificatesStatistics
            - UnitBeingLateCertificatesTodayAndWeekBefore
        - BonusSystemStatistics
            - UnitBonusSystem
    - By cookies and unit ids:
        - RevenueStatistics
            - UnitsRevenueMetadata
            - RevenueForTodayAndWeekBeforeStatistics
        - KitchenPerformanceStatistics
            - UnitKitchenPerformance
        - DeliveryPerformanceStatistics
            - UnitDeliveryPerformance
        - HeatedShelfStatistics
            - UnitHeatedShelf
        - CouriersStatistics
            - UnitCouriers
        - KitchenProductionStatistics
            - UnitKitchenProduction
        - HeatedShelfOrdersAndCouriersStatistics
            - UnitHeatedShelfOrdersAndCouriers

- Stop sales:
    - StopSale
        - StopSaleByToken
            - StopSaleByIngredients
            - StopSaleByProduct
            - StopSaleBySalesChannels
        - StopSaleBySectors
        - StopSaleByStreets


"""
import uuid
from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field

from .aliases import UnitIdAndName

__all__ = (
    'DeliverySpeedStatistics',
    'StockBalanceStatistics',
    'BonusSystemStatistics',
    'CouriersStatistics',
    'RevenueStatistics',
    'DeliveryPerformanceStatistics',
    'KitchenPerformanceStatistics',
    'KitchenProductionStatistics',
    'HeatedShelfOrdersAndCouriersStatistics',
    'OrdersHandoverTimeStatistics',
    'RevenueForTodayAndWeekBeforeStatistics',

    'UnitCouriers',
    'UnitIdAndName',
    'UnitBonusSystem',
    'UnitOrdersHandoverTime',
    'UnitDeliverySpeed',
    'UnitsRevenueMetadata',
    'UnitHeatedShelfStatistics',
    'UnitKitchenProduction',
    'UnitDeliveryPerformance',
    'UnitKitchenPerformance',
    'UnitBeingLateCertificates',
    'UnitHeatedShelfOrdersAndCouriers',
    'UnitProductivityBalanceStatistics',
    'UnitDeliveryProductivityStatistics',
    'UnitRestaurantCookingTimeStatistics',

    'StopSale',
    'StopSaleByToken',
    'StopSaleByIngredients',
    'StopSaleBySalesChannels',
    'StopSaleBySectors',
    'StopSaleByStreets',
    'SalesChannel',

    'OrderByUUID',
    'CheatedOrders',
    'CheatedOrder',
    'StockBalance',
    'KitchenPartialStatisticsReport',
    'DeliveryPartialStatisticsReport',
    'UnitDeliveryPartialStatistics',
    'UnitKitchenPartialStatistics',
)


# Statistics
# Models by tokens and unit UUIDs

class SalesChannel(Enum):
    DINE_IN = 'Dine-in'
    TAKEAWAY = 'Takeaway'
    DELIVERY = 'Delivery'


class UnitDeliveryProductivityStatistics(BaseModel):
    unit_uuid: uuid.UUID
    orders_per_courier_labour_hour_today: float
    orders_per_courier_labour_hour_week_before: float
    from_week_before_in_percents: int


class UnitOrdersHandoverTime(BaseModel):
    unit_uuid: UUID
    unit_name: str
    average_tracking_pending_time: int
    average_cooking_time: int
    average_heated_shelf_time: int
    sales_channels: list[SalesChannel]


class OrdersHandoverTimeStatistics(BaseModel):
    units: list[UnitOrdersHandoverTime]
    error_unit_uuids: list[UUID]


class UnitDeliverySpeed(BaseModel):
    unit_uuid: UUID
    average_cooking_time: int
    average_delivery_order_fulfillment_time: int
    average_heated_shelf_time: int
    average_order_trip_time: int


class DeliverySpeedStatistics(BaseModel):
    units: list[UnitDeliverySpeed]
    error_unit_uuids: list[UUID]


class UnitBeingLateCertificates(BaseModel):
    unit_uuid: uuid.UUID
    certificates_count_today: int
    certificates_count_week_before: int


# Models by cookies, unit ids and names

class UnitBonusSystem(BaseModel):
    unit_id: str
    orders_with_phone_numbers_count: int
    orders_with_phone_numbers_percent: int
    total_orders_count: int


class BonusSystemStatistics(BaseModel):
    units: list[UnitBonusSystem]
    error_unit_ids_and_names: list[UnitIdAndName]


# Models by cookies and unit ids

class UnitsRevenueMetadata(BaseModel):
    total_revenue_today: int
    total_revenue_week_before: int
    delta_from_week_before: float


class RevenueForTodayAndWeekBeforeStatistics(BaseModel):
    unit_id: int
    today: int
    week_before: int
    delta_from_week_before: float


class UnitRevenueStatistics(BaseModel):
    unit_id: int
    today: int
    from_week_before_in_percents: int


class TotalRevenueStatistics(BaseModel):
    today: int
    from_week_before_in_percents: int


class UnitsRevenueStatistics(BaseModel):
    units: list[UnitRevenueStatistics]
    total: TotalRevenueStatistics


class RevenueStatistics(BaseModel):
    results: UnitsRevenueStatistics
    errors: list[int]


class UnitKitchenPerformance(BaseModel):
    unit_id: int
    revenue_per_hour: int
    revenue_delta_from_week_before: int


class KitchenPerformanceStatistics(BaseModel):
    units: list[UnitKitchenPerformance]
    error_unit_ids: list[int]


class UnitDeliveryPerformance(BaseModel):
    unit_id: int
    orders_for_courier_count_per_hour_today: float
    orders_for_courier_count_per_hour_week_before: float
    delta_from_week_before: int


class DeliveryPerformanceStatistics(BaseModel):
    units: list[UnitDeliveryPerformance]
    error_unit_ids: list[int]


class UnitHeatedShelfStatistics(BaseModel):
    unit_uuid: uuid.UUID
    average_heated_shelf_time: int


class UnitRestaurantCookingTimeStatistics(BaseModel):
    unit_uuid: uuid.UUID
    average_tracking_pending_and_cooking_time: int


class UnitCouriers(BaseModel):
    unit_id: int
    in_queue_count: int
    total_count: int


class CouriersStatistics(BaseModel):
    units: list[UnitCouriers]
    error_unit_ids: list[int]


class UnitKitchenProduction(BaseModel):
    unit_id: int
    average_cooking_time: int


class KitchenProductionStatistics(BaseModel):
    units: list[UnitKitchenProduction]
    error_unit_ids: list[int]


class UnitHeatedShelfOrdersAndCouriers(BaseModel):
    unit_id: int
    awaiting_orders_count: int
    in_queue_count: int
    total_count: int


class HeatedShelfOrdersAndCouriersStatistics(BaseModel):
    units: list[UnitHeatedShelfOrdersAndCouriers]
    error_unit_ids: list[int]


# Stop sales

class StopSale(BaseModel):
    unit_name: str
    started_at: datetime
    ended_at: datetime | None
    stopped_by_user_id: uuid.UUID = Field(alias='stoppedByUserId')
    resumed_by_user_id: uuid.UUID | None = Field(alias='resumedByUserId')


# New API
class StopSaleByToken(StopSale):
    unit_uuid: UUID = Field(alias='unit_id')
    reason: str


class StopSaleByIngredients(StopSaleByToken):
    ingredient_name: str


class StopSaleBySalesChannels(StopSaleByToken):
    sales_channel_name: str


# Old API (Dodo IS)
class StopSaleBySectors(StopSale):
    sector: str


class StopSaleByStreets(StopSale):
    sector: str
    street: str


class OrderByUUID(BaseModel):
    unit_name: str
    created_at: datetime
    receipt_printed_at: datetime | None
    number: str
    type: str
    price: int
    uuid: UUID


class CheatedOrder(BaseModel):
    created_at: datetime
    number: str


class CheatedOrders(BaseModel):
    unit_name: str
    phone_number: str
    orders: list[CheatedOrder]


class StockBalance(BaseModel):
    unit_id: int
    ingredient_name: str
    days_left: int
    stocks_count: float | int
    stocks_unit: str


class StockBalanceStatistics(BaseModel):
    error_unit_ids: list[int]
    units: list[StockBalance]


class UnitProductivityBalanceStatistics(BaseModel):
    unit_uuid: uuid.UUID
    sales_per_labor_hour: int
    orders_per_labor_hour: float
    stop_sale_duration_in_seconds: int


class UnitDeliveryPartialStatistics(BaseModel):
    unit_id: int
    heated_shelf_orders_count: int
    couriers_in_queue_count: int
    couriers_on_shift_count: int


class DeliveryPartialStatisticsReport(BaseModel):
    results: list[UnitDeliveryPartialStatistics]
    errors: list[int]


class UnitKitchenPartialStatistics(BaseModel):
    unit_id: int
    sales_per_labor_hour_today: int
    from_week_before_percent: int
    total_cooking_time: int


class KitchenPartialStatisticsReport(BaseModel):
    results: list[UnitKitchenPartialStatistics]
    errors: list[int]
