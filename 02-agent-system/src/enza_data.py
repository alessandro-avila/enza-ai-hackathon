import json
import logging
import os
import aiohttp
import pandas as pd
import sys

from terminal_colors import TerminalColors as tc
from utilities import Utilities

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class EnzaData:
    """Class to interact with Enza Zaden's data via APIM."""


    def __init__(self, utilities: Utilities) -> None:
        """Initialize the EnzaData class."""
        self.utilities = utilities
        self.apim_gateway_url = os.getenv("APIM_GATEWAY_URL")
        self.apim_subscription_key = os.getenv("APIM_SUBSCRIPTION_KEY")

        # Validate essential environment variables
        if not self.apim_gateway_url or not self.apim_subscription_key:
            logger.error("APIM_GATEWAY_URL or APIM_SUBSCRIPTION_KEY environment variables not set")
        else:
            logger.debug("EnzaData initialized with APIM endpoint: %s", self.apim_gateway_url)

    async def close(self):
        """Cleanup resources if needed (placeholder for future resource management)."""
        pass

    async def get_database_info(self) -> str:
        """Get the database schema information."""
        # Provide the actual sales database schema
        schema = {
            "Tables": [
                {
                    "Name": "SalesRegions",
                    "Columns": [
                        "RegionID: INT",
                        "RegionName: NVARCHAR(50)",
                        "RegionManager: NVARCHAR(100)",
                        "HeadquartersLocation: NVARCHAR(100)",
                    ],
                },
                {
                    "Name": "Products",
                    "Columns": [
                        "ProductID: INT",
                        "ProductName: NVARCHAR(100)",
                        "ProductCategory: NVARCHAR(50)",
                        "UnitPrice: DECIMAL(10,2)",
                        "ProductLine: NVARCHAR(50)",
                        "LaunchDate: DATE",
                    ],
                },
                {
                    "Name": "Customers",
                    "Columns": [
                        "CustomerID: INT",
                        "CustomerName: NVARCHAR(100)",
                        "ContactName: NVARCHAR(100)",
                        "CustomerType: NVARCHAR(50)",
                        "RegionID: INT",
                        "Country: NVARCHAR(50)",
                        "City: NVARCHAR(50)",
                    ],
                },
                {
                    "Name": "SalesData",
                    "Columns": [
                        "SalesID: INT",
                        "ProductID: INT",
                        "CustomerID: INT",
                        "SalesDate: DATE",
                        "Quantity: INT",
                        "UnitsSold: INT",
                        "TotalAmount: DECIMAL(15,2)",
                        "DiscountApplied: DECIMAL(5,2)",
                        "SalesChannel: NVARCHAR(50)",
                        "PromotionID: INT",
                    ],
                },
            ],
            "Functions": [
                {
                    "Name": "get_sales_by_region",
                    "Description": "Get sales data grouped by region or for a specific region",
                    "Parameters": ["region_name (optional)"],
                },
                {"Name": "get_sales_by_category", "Description": "Get sales data grouped by product category"},
                {"Name": "get_sales_by_channel", "Description": "Get sales data grouped by sales channel"},
                {
                    "Name": "get_top_customers",
                    "Description": "Get top customers by total spend",
                    "Parameters": ["limit (optional, default: 10)"],
                },
                {"Name": "get_product_performance", "Description": "Get performance metrics for all products"},
            ],
        }

        # Format the schema as a string
        schema_string = json.dumps(schema, indent=2)
        return schema_string

    async def get_sales_by_region(
        self, region_name: str = None, *, description: str = "Get sales data grouped by region"
    ) -> str:
        """
        Get sales data grouped by region or for a specific region.

        Args:
            region_name: Optional name of the region to filter by.

        Returns:
            A JSON string containing the sales data.
        """
        try:
            request_id = self.utilities.generate_uuid()
            url = f"{self.apim_gateway_url}/sql/sales/regions"
            headers = {
                "api-key": self.apim_subscription_key,
                "Request-Id": request_id,
                "Content-Type": "application/json",
            }

            data = {}
            if region_name:
                data["region_name"] = region_name

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.text()
                        logger.debug("Retrieved sales data by region successfully")
                        return result
                    else:
                        error_msg = f"Error retrieving sales data: {response.status} - {await response.text()}"
                        logger.error(error_msg)
                        return json.dumps({"error": error_msg})

        except Exception as e:
            logger.exception("Exception retrieving sales data by region", exc_info=e)
            return json.dumps({"error": str(e)})

    async def get_sales_by_category(self, *, description: str = "Get sales data grouped by product category") -> str:
        """
        Get sales data grouped by product category.

        Returns:
            A JSON string containing the sales data by category.
        """
        try:
            request_id = self.utilities.generate_uuid()
            url = f"{self.apim_gateway_url}/sql/sales/by-category"
            headers = {
                "api-key": self.apim_subscription_key,
                "Request-Id": request_id,
                "Content-Type": "application/json",
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json={}) as response:
                    if response.status == 200:
                        result = await response.text()
                        logger.debug("Retrieved sales data by category successfully")
                        return result
                    else:
                        error_msg = f"Error retrieving sales data: {response.status} - {await response.text()}"
                        logger.error(error_msg)
                        return json.dumps({"error": error_msg})

        except Exception as e:
            logger.exception("Exception retrieving sales data by category", exc_info=e)
            return json.dumps({"error": str(e)})

    async def get_sales_by_channel(self, *, description: str = "Get sales data grouped by sales channel") -> str:
        """
        Get sales data grouped by sales channel.

        Returns:
            A JSON string containing the sales data by channel.
        """
        try:
            request_id = self.utilities.generate_uuid()
            url = f"{self.apim_gateway_url}/sql/sales/by-channel"
            headers = {
                "api-key": self.apim_subscription_key,
                "Request-Id": request_id,
                "Content-Type": "application/json",
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json={}) as response:
                    if response.status == 200:
                        result = await response.text()
                        logger.debug("Retrieved sales data by channel successfully")
                        return result
                    else:
                        error_msg = f"Error retrieving sales data: {response.status} - {await response.text()}"
                        logger.error(error_msg)
                        return json.dumps({"error": error_msg})
        except Exception as e:
            logger.exception("Exception retrieving sales data by channel", exc_info=e)
            return json.dumps({"error": str(e)})

    async def get_top_customers(self, limit: int = 10, *, description: str = "Get top customers by total spend") -> str:
        """
        Get top customers by total spend.

        Args:
            limit: Number of top customers to retrieve (default: 10).

        Returns:
            A JSON string containing the top customers data.
        """
        try:
            request_id = self.utilities.generate_uuid()
            url = f"{self.apim_gateway_url}/sql/customers/top"
            headers = {
                "api-key": self.apim_subscription_key,
                "Request-Id": request_id,
                "Content-Type": "application/json",
            }

            data = {"limit": limit}

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.text()
                        logger.debug("Retrieved top customers data successfully")
                        return result
                    else:
                        error_msg = f"Error retrieving customer data: {response.status} - {await response.text()}"
                        logger.error(error_msg)
                        return json.dumps({"error": error_msg})
        except Exception as e:
            logger.exception("Exception retrieving top customers data", exc_info=e)
            return json.dumps({"error": str(e)})

    async def get_product_performance(self, *, description: str = "Get performance metrics for all products") -> str:
        """
        Get performance metrics for all products.

        Returns:
            A JSON string containing the product performance data.
        """
        try:
            request_id = self.utilities.generate_uuid()
            url = f"{self.apim_gateway_url}/sql/products/performance"
            headers = {
                "api-key": self.apim_subscription_key,
                "Request-Id": request_id,
                "Content-Type": "application/json",
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json={}) as response:
                    if response.status == 200:
                        result = await response.text()
                        logger.debug("Retrieved product performance data successfully")
                        return result
                    else:
                        error_msg = f"Error retrieving product data: {response.status} - {await response.text()}"
                        logger.error(error_msg)
                        return json.dumps({"error": error_msg})
        except Exception as e:
            logger.exception("Exception retrieving product performance data", exc_info=e)
            return json.dumps({"error": str(e)})

    async def get_weather(
        self,
        location: str,
        unit: str,
        *,
        description: str = "Get current weather for a location",
        allowed_units: list[str] = ["celsius", "fahrenheit"],
    ) -> str:
        """
        Get current weather for a location via APIM.

        Args:
            location: The location to get weather for.
            unit: The temperature unit (celsius or fahrenheit).

        Returns:
            A JSON string containing the weather information.
        """
        try:
            request_id = self.utilities.generate_uuid()
            url = f"{self.apim_gateway_url}/weather"
            headers = {
                "api-key": self.apim_subscription_key,
                "Request-Id": request_id,
                "Content-Type": "application/json",
            }

            data = {"location": location, "unit": unit}

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.text()
                        logger.debug("Weather data retrieved successfully for %s", location)
                        return result
                    else:
                        error_msg = f"Error retrieving weather: {response.status} - {await response.text()}"
                        logger.error(error_msg)
                        return json.dumps({"error": error_msg})
        except Exception as e:
            logger.exception("Exception retrieving weather via APIM", exc_info=e)
            return json.dumps({"error": str(e)})
