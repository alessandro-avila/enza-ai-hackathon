import logging
import azure.functions as func
import pyodbc
import json
import os
import time
import re
from typing import List, Dict, Any, Optional

# Configure the function app
app = func.FunctionApp()

# Get connection string from environment variables
SQL_CONNECTION_STRING = os.environ.get("SQL_CONNECTION_STRING")


def run_query(query, params=None):
    results = []
    with pyodbc.connect(SQL_CONNECTION_STRING) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params or [])
            columns = [c[0] for c in cursor.description]
            for row in cursor.fetchall():
                # Convert row to dict
                results.append(dict(zip(columns, row)))
    return results


@app.route(route="sql/sales/regions", auth_level=func.AuthLevel.ANONYMOUS)
def get_sales_by_region(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing request to get sales data by region.")

    try:
        # Parse request body JSON
        data = req.get_json()
        region = data.get("region_name")

        # Use stored procedure for sales by region
        if region:
            # If region provided, pass as parameter
            query = "EXEC GetSalesByRegion @RegionName=?"
            params = [region]
        else:
            # All regions
            query = "EXEC GetSalesByRegion"
            params = []

        results = run_query(query, params)

        return func.HttpResponse(
            json.dumps({"results": results}),
            status_code=200,
            mimetype="application/json",
        )

    except Exception as e:
        logging.error(f"Error getting sales by region: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Error getting sales by region", "details": str(e)}),
            status_code=500,
            mimetype="application/json",
        )
