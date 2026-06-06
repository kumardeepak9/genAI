import os
from dotenv import load_dotenv
from snowflake.snowpark import Session

def get_session() -> Session:
    """
    Retrieves a Snowflake Snowpark Session.
    
    1. First, attempts to get an active session from the current context.
       This is used when running inside Streamlit in Snowflake (SiS) or Snowflake Notebooks.
    2. If that fails, attempts to build a local session using environment variables
       loaded from a .env file.
       
    Returns:
        Session: Active Snowflake Snowpark session.
        
    Raises:
        RuntimeError: If no session can be obtained or created.
    """
    # 1. Attempt to obtain session from Snowflake context (SiS / Snowflake Notebooks)
    try:
        from snowflake.snowpark.context import get_active_session
        session = get_active_session()
        # Verify the session is valid
        if session is not None:
            return session
    except (ImportError, Exception):
        pass

    # 2. Fall back to local configuration
    # Load .env file if it exists in the current directory or parents
    load_dotenv()

    connection_parameters = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "user": os.getenv("SNOWFLAKE_USER"),
        "password": os.getenv("SNOWFLAKE_PASSWORD"),
        "role": os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
        "database": os.getenv("SNOWFLAKE_DATABASE"),
        "schema": os.getenv("SNOWFLAKE_SCHEMA"),
    }

    # Filter out None values to prevent API validation errors
    connection_parameters = {k: v for k, v in connection_parameters.items() if v is not None}

    # Verify minimum required parameters for a local connection
    required_keys = ["account", "user", "password"]
    missing_keys = [k for k in required_keys if k not in connection_parameters]
    if missing_keys:
        raise RuntimeError(
            f"Failed to connect to Snowflake.\n"
            f"No active session found in context, and missing local connection parameters: {', '.join(missing_keys)}.\n"
            f"Please verify your local setup by creating a '.env' file from '.env.template'."
        )

    try:
        session = Session.builder.configs(connection_parameters).create()
        return session
    except Exception as e:
        raise RuntimeError(f"Failed to create Snowflake local session: {str(e)}")
