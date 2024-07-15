from sqlmesh import macro
  
@macro()
def snow_only(evaluator):
    if evaluator.gateway == 'snow':
        return True
    else:
        return False
    
@macro()
def duckdb_only(evaluator):
    if 'duckdb' in str(evaluator.gateway):
        return True
    else:
        return False