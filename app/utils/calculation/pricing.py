from models.product_plan import ProductPlan
from models.voucher import Voucher


def calculate_pricing_in_euro(
    product_plan: ProductPlan, /, voucher: Voucher | None = None
) -> float:
    return calculate_full_pricing_in_euro(product_plan, voucher)[0]


def calculate_full_pricing_in_euro(
    product_plan: ProductPlan, /, voucher: Voucher | None = None
) -> tuple[float, float]:
    cost = float(product_plan.cost_euro)

    if not voucher:
        return (cost, cost)

    assert product_plan.uuid == voucher.product_plan_uuid

    if voucher.discount_percentage:
        cost *= voucher.discount_percentage / 100

    if voucher.discount_fixed_amount:
        cost -= voucher.discount_fixed_amount

    return (cost, product_plan.cost)
