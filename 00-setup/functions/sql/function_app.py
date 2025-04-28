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

## ODBC Driver settings
conn_string = f"{SQL_CONNECTION_STRING}Driver=ODBC Driver 18 for SQL Server"
# Condense the replacement of Encrypt=True/False with Encrypt=yes/no into one statement
conn_string = re.sub(r"Encrypt=True|Encrypt=False", lambda m: "Encrypt=yes" if m.group() == "Encrypt=True" else "Encrypt=no", conn_string)
# do the same for TrustServerCertificate
conn_string = re.sub(r"TrustServerCertificate=True|TrustServerCertificate=False", lambda m: "TrustServerCertificate=yes" if m.group() == "TrustServerCertificate=True" else "TrustServerCertificate=no", conn_string)
# replace ID with UID
conn_string = re.sub(r"(User ID=)", "UID=", conn_string)
conn_string = re.sub(r"(Password=)", "PWD=", conn_string)
# Initial catalog
conn_string = re.sub(r"(Initial Catalog=)", "Database=", conn_string)

def run_query(query, params=None):
    results = []
    logging.info(f"Connecting with: {conn_string.replace(';Password=', ';Password=*****')}")
    
    max_retries = 3
    retry_count = 0
    last_exception = None
    
    while retry_count < max_retries:
        try:
            with pyodbc.connect(conn_string, timeout=30) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params or [])
                    if cursor.description:  # Check if the query returns any results
                        columns = [c[0] for c in cursor.description]
                        for row in cursor.fetchall():
                            # Convert row to dict
                            results.append(dict(zip(columns, row)))
            return results
        except Exception as e:
            last_exception = e
            retry_count += 1
            logging.warning(f"Database connection attempt {retry_count} failed: {str(e)}")
            time.sleep(1)  # Wait before retrying
    
    # If we get here, all retries failed
    logging.error(f"Failed to connect to database after {max_retries} attempts. Last error: {str(last_exception)}")
    raise last_exception


@app.route(route="sql/sales/regions", auth_level=func.AuthLevel.ANONYMOUS)
def get_sales_by_region(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing request to get sales data by region.")

    try:
        logging.info("Request body: %s", req)
        logging.info("Request headers: %s", req.headers)
        logging.info("Request method: %s", req.method)
        logging.info("Request URL: %s", req.url)
        
        # Parse request body JSON
        body = req.get_body().decode()
        region = json.loads(body).get("region_name")
        logging.info("Region name from request: %s", region)

        # Use stored procedure for sales by region
        if region:
            # If region provided, pass as parameter
            query = """
            SELECT 
                r.RegionName,
                CAST(SUM(s.TotalAmount) as FLOAT) AS TotalSales,
                COUNT(DISTINCT s.SalesID) AS NumberOfTransactions,
                SUM(s.UnitsSold) AS TotalUnitsSold
            FROM 
                SalesData s
                JOIN Customers c ON s.CustomerID = c.CustomerID
                JOIN SalesRegions r ON c.RegionID = r.RegionID
            WHERE 
                r.RegionName = ?
            GROUP BY 
                r.RegionName
            """
            params = [region]
        else:
            # All regions
            query = """
            SELECT 
                r.RegionName,
                CAST(SUM(s.TotalAmount) as FLOAT) AS TotalSales,
                COUNT(DISTINCT s.SalesID) AS NumberOfTransactions,
                SUM(s.UnitsSold) AS TotalUnitsSold
            FROM 
                SalesData s
                JOIN Customers c ON s.CustomerID = c.CustomerID
                JOIN SalesRegions r ON c.RegionID = r.RegionID
            GROUP BY 
                r.RegionName
            ORDER BY 
                TotalSales DESC
            """
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
