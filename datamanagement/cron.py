import logging
from datamanagement.background_functions import working_days
from .strategy import *
from .background_functions import *
from .data_collection import run_strategy as collect_data
from .views import get_app_session_id

logger = logging.getLogger('dev_log')

def my_scheduled_job():

    logger.info("lets see if it comes")
    working_day_calculation(0)
    get_app_session_id()
    strat = collect_data(strategy)
    value=strat.run()
    if value!=None:
        return value

