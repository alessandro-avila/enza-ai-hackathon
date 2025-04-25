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
            
    async def connect(self) -> None:
        """Simulate connection - in our case, just validate the APIM endpoint."""
        try:
            # Just a placeholder - we'll check actual connectivity when making the first API call
            logger.debug("EnzaData ready to connect to APIM endpoint")
        except Exception as e:
            logger.exception("Error connecting to APIM endpoint", exc_info=e)
    
    async def close(self) -> None:
        """Close any open connections."""
        # Nothing to do here since we're using HTTP requests
        logger.debug("EnzaData connections closed")
    
    async def get_database_info(self) -> str:
        """Get the database schema information."""
        # For the hackathon, we'll provide a predefined schema description
        # that describes the tables available through our API
        schema = {
            "Tables": [
                {
                    "Name": "Plants",
                    "Columns": [
                        "plant_id: TEXT", 
                        "species: TEXT", 
                        "variety: TEXT", 
                        "planting_date: DATE", 
                        "location: TEXT"
                    ]
                },
                {
                    "Name": "GrowthData",
                    "Columns": [
                        "record_id: INTEGER", 
                        "plant_id: TEXT", 
                        "measurement_date: DATE", 
                        "height_cm: REAL", 
                        "leaf_count: INTEGER", 
                        "health_score: REAL"
                    ]
                },
                {
                    "Name": "YieldPredictions",
                    "Columns": [
                        "prediction_id: INTEGER", 
                        "plant_id: TEXT", 
                        "prediction_date: DATE", 
                        "predicted_yield: REAL", 
                        "confidence_score: REAL"
                    ]
                }
            ]
        }
        
        # Format the schema as a string
        schema_string = json.dumps(schema, indent=2)
        return schema_string
    
    async def async_fetch_plant_data_using_sql_query(self, query: str) -> str:
        """
        Execute a SQL query against the NextGB database via APIM.
        
        Args:
            query: The SQL query to execute.
            
        Returns:
            A JSON string containing the query results.
        """
        try:
            # Generate a request ID for tracing
            request_id = self.utilities.generate_uuid()
            
            # Prepare the request to the query endpoint via APIM
            url = f"{self.apim_gateway_url}/query"
            headers = {
                "api-key": self.apim_subscription_key,
                "Request-Id": request_id,
                "Content-Type": "application/json"
            }
            
            data = {
                "query": query,
                "database": "nextgb"
            }
            
            # Make the API call
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.text()
                        logger.debug("Query executed successfully: %s", query)
                        return result
                    else:
                        error_msg = f"Error executing query: {response.status} - {await response.text()}"
                        logger.error(error_msg)
                        return json.dumps({"error": error_msg})
        except Exception as e:
            logger.exception("Exception executing query via APIM", exc_info=e)
            return json.dumps({"error": str(e)})
    
    async def async_run_algorithm(self, plant_id: str, analysis_type: str, parameters: dict = None) -> str:
        """
        Run Enza Zaden's algorithm via APIM.
        
        Args:
            plant_id: The ID of the plant to analyze.
            analysis_type: The type of analysis to perform (growth, disease, yield).
            parameters: Additional parameters for the algorithm.
            
        Returns:
            A JSON string containing the algorithm results.
        """
        try:
            # Generate a request ID for tracing
            request_id = self.utilities.generate_uuid()
            
            # Prepare the request to the algorithm endpoint via APIM
            url = f"{self.apim_gateway_url}/algorithm"
            headers = {
                "api-key": self.apim_subscription_key,
                "Request-Id": request_id,
                "Content-Type": "application/json"
            }
            
            data = {
                "plant_id": plant_id,
                "analysis_type": analysis_type
            }
            
            # Add optional parameters if provided
            if parameters:
                data["parameters"] = parameters
            
            # Make the API call
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.text()
                        logger.debug("Algorithm executed successfully for plant %s", plant_id)
                        return result
                    else:
                        error_msg = f"Error executing algorithm: {response.status} - {await response.text()}"
                        logger.error(error_msg)
                        return json.dumps({"error": error_msg})
        except Exception as e:
            logger.exception("Exception running algorithm via APIM", exc_info=e)
            return json.dumps({"error": str(e)})
    
    async def async_get_weather(self, location: str, unit: str) -> str:
        """
        Get current weather for a location via APIM.
        
        Args:
            location: The location to get weather for.
            unit: The temperature unit (celsius or fahrenheit).
            
        Returns:
            A JSON string containing the weather information.
        """
        try:
            # Generate a request ID for tracing
            request_id = self.utilities.generate_uuid()
            
            # Prepare the request to the weather endpoint via APIM
            url = f"{self.apim_gateway_url}/weather"
            headers = {
                "api-key": self.apim_subscription_key,
                "Request-Id": request_id,
                "Content-Type": "application/json"
            }
            
            data = {
                "location": location,
                "unit": unit
            }
            
            # Make the API call
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
