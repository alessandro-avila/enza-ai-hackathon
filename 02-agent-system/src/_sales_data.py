import os
import json
import logging
import requests
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class SQLData:
    """Class to interact with sales data through the SQL API."""

    def __init__(self, utilities=None):
        """Initialize the SQLData class."""
        self.utilities = utilities
        self.apim_gateway_url = os.getenv("APIM_GATEWAY_URL")
        self.apim_subscription_key = os.getenv("APIM_SUBSCRIPTION_KEY")
        
        # Check if the required environment variables are set
        if not self.apim_gateway_url or not self.apim_subscription_key:
            logger.warning("APIM_GATEWAY_URL or APIM_SUBSCRIPTION_KEY not set. SQL query functionality will not work.")

    async def execute_sql_query(self, query: str, parameters: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Execute a SQL query against the database.
        
        Args:
            query: The SQL query to execute
            parameters: Optional parameters for the SQL query
            
        Returns:
            A dictionary with the query results
        """
        if self.utilities:
            self.utilities.append_log("Executing SQL query: " + query)
        
        if not self.apim_gateway_url or not self.apim_subscription_key:
            error_msg = "Cannot execute SQL query: APIM_GATEWAY_URL or APIM_SUBSCRIPTION_KEY not set."
            logger.error(error_msg)
            return {"error": error_msg}
        
        # Prepare the request
        url = f"{self.apim_gateway_url}/sql/query"
        headers = {
            "api-key": self.apim_subscription_key,
            "Content-Type": "application/json"
        }
        
        # Create request payload
        payload = {
            "query": query
        }
        
        if parameters:
            payload["parameters"] = parameters
        
        try:
            # Make the request
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for non-2xx status codes
            
            # Parse and return the response
            result = response.json()
            
            if self.utilities:
                self.utilities.append_log(f"SQL query executed successfully. Returned {len(result.get('results', []))} records.")
            
            return result
        except requests.exceptions.RequestException as e:
            error_msg = f"Error executing SQL query: {str(e)}"
            if self.utilities:
                self.utilities.append_log(error_msg)
            logger.error(error_msg)
            
            # Try to parse error response if available
            try:
                error_details = response.json()
                return {"error": error_msg, "details": error_details}
            except:
                return {"error": error_msg}

    async def get_sales_by_region(self, region_name: Optional[str] = None) -> Dict[str, Any]:
        """Get sales data by region.
        
        Args:
            region_name: Optional name of the region to filter by
            
        Returns:
            Sales data for the specified region or all regions if not specified
        """
        if self.utilities:
            self.utilities.append_log(f"Getting sales data for region: {region_name if region_name else 'all regions'}")
        
        if not self.apim_gateway_url or not self.apim_subscription_key:
            error_msg = "Cannot execute SQL query: APIM_GATEWAY_URL or APIM_SUBSCRIPTION_KEY not set."
            logger.error(error_msg)
            return {"error": error_msg}
        
        # Prepare the request
        url = f"{self.apim_gateway_url}/sql/sales/regions"
        headers = {
            "api-key": self.apim_subscription_key,
            "Content-Type": "application/json"
        }
        
        # Create request payload
        payload = {}
        if region_name:
            payload["region_name"] = region_name
        
        try:
            # Make the request
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            # Parse and return the response
            result = response.json()
            
            if self.utilities:
                self.utilities.append_log(f"Retrieved sales data for {region_name if region_name else 'all regions'}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error getting sales by region: {str(e)}"
            if self.utilities:
                self.utilities.append_log(error_msg)
            logger.error(error_msg)
            return {"error": error_msg}
    
    async def get_product_sales(self, product_category: Optional[str] = None) -> Dict[str, Any]:
        """Get sales data by product category.
        
        Args:
            product_category: Optional product category to filter by
            
        Returns:
            Sales data for the specified product category or all categories if not specified
        """
        if self.utilities:
            self.utilities.append_log(f"Getting sales data for product category: {product_category if product_category else 'all categories'}")
        
        if not self.apim_gateway_url or not self.apim_subscription_key:
            error_msg = "Cannot execute SQL query: APIM_GATEWAY_URL or APIM_SUBSCRIPTION_KEY not set."
            logger.error(error_msg)
            return {"error": error_msg}
        
        # Prepare the request
        url = f"{self.apim_gateway_url}/sql/sales/products"
        headers = {
            "api-key": self.apim_subscription_key,
            "Content-Type": "application/json"
        }
        
        # Create request payload
        payload = {}
        if product_category:
            payload["product_category"] = product_category
        
        try:
            # Make the request
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            # Parse and return the response
            result = response.json()
            
            if self.utilities:
                self.utilities.append_log(f"Retrieved product sales data for {product_category if product_category else 'all categories'}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error getting product sales: {str(e)}"
            if self.utilities:
                self.utilities.append_log(error_msg)
            logger.error(error_msg)
            return {"error": error_msg}
    
    async def get_customer_sales(self, customer_type: Optional[str] = None) -> Dict[str, Any]:
        """Get sales data by customer type.
        
        Args:
            customer_type: Optional customer type to filter by
            
        Returns:
            Sales data for the specified customer type or all types if not specified
        """
        if self.utilities:
            self.utilities.append_log(f"Getting sales data for customer type: {customer_type if customer_type else 'all types'}")
        
        if not self.apim_gateway_url or not self.apim_subscription_key:
            error_msg = "Cannot execute SQL query: APIM_GATEWAY_URL or APIM_SUBSCRIPTION_KEY not set."
            logger.error(error_msg)
            return {"error": error_msg}
        
        # Prepare the request
        url = f"{self.apim_gateway_url}/sql/sales/customers"
        headers = {
            "api-key": self.apim_subscription_key,
            "Content-Type": "application/json"
        }
        
        # Create request payload
        payload = {}
        if customer_type:
            payload["customer_type"] = customer_type
        
        try:
            # Make the request
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            # Parse and return the response
            result = response.json()
            
            if self.utilities:
                self.utilities.append_log(f"Retrieved customer sales data for {customer_type if customer_type else 'all types'}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error getting customer sales: {str(e)}"
            if self.utilities:
                self.utilities.append_log(error_msg)
            logger.error(error_msg)
            return {"error": error_msg}
        
    async def get_sales_over_time(self, period_type: str = "month") -> Dict[str, Any]:
        """Get sales data over time.
        
        Args:
            period_type: The time period to group by ('month' or 'quarter')
            
        Returns:
            Sales data grouped by the specified time period
        """
        if self.utilities:
            self.utilities.append_log(f"Getting sales data over time by {period_type}")
        
        if not self.apim_gateway_url or not self.apim_subscription_key:
            error_msg = "Cannot execute SQL query: APIM_GATEWAY_URL or APIM_SUBSCRIPTION_KEY not set."
            logger.error(error_msg)
            return {"error": error_msg}
        
        # Prepare the request
        url = f"{self.apim_gateway_url}/sql/sales/time-series"
        headers = {
            "api-key": self.apim_subscription_key,
            "Content-Type": "application/json"
        }
        
        # Create request payload
        payload = {"period_type": period_type}
        
        try:
            # Make the request
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            # Parse and return the response
            result = response.json()
            
            if self.utilities:
                self.utilities.append_log(f"Retrieved sales time series data by {period_type}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error getting sales over time: {str(e)}"
            if self.utilities:
                self.utilities.append_log(error_msg)
            logger.error(error_msg)
            return {"error": error_msg}
        
    async def run_custom_query(self, query: str, parameters: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Run a custom SQL query.
        
        Args:
            query: The SQL query to execute
            parameters: Optional parameters for the SQL query
            
        Returns:
            The query results
        """
        return await self.execute_sql_query(query, parameters)
