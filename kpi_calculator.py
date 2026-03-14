import numpy as np

def calculate_channel_market_share(df):
    total_orders = df["MonthlyOrders"].sum()

    shares = {
        "InStore": df["InStoreOrders"].sum() / total_orders,
        "UberEats": df["UberEatsOrders"].sum() / total_orders,
        "DoorDash": df["DoorDashOrders"].sum() / total_orders,
        "SelfDelivery": df["SelfDeliveryOrders"].sum() / total_orders,
    }

    return shares


def calculate_dependency_index(df):
    df["AggregatorDependence"] = (
        df["UberEatsOrders"] +
        df["DoorDashOrders"]
    ) / df["MonthlyOrders"]

    return df


def calculate_diversification_score(df):
    channel_cols = [
        "InStoreShare",
        "UE_share",
        "DD_share",
        "SD_share"
    ]

    df["DiversificationScore"] = 1 - df[channel_cols].std(axis=1)

    return df
