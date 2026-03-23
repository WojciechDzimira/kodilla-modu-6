import pytest
from src.SQL_engine import DataBaseSQL



@pytest.fixture
def base():
    base = DataBaseSQL(":memory:")
    yield base  
    base.close() 

@pytest.fixture
def base_with_data():
    base = DataBaseSQL(":memory:")
    base.execute_script("sql_create.sql")
    sql1 = "INSERT INTO Stations (station,latitude,longitude,elevation,name,country,state)" \
            "VALUES (?, ?, ?, ?, ?, ?, ?)"
    test_data1 = ("TEST Station", 10.20, 20.30, 
                40.50, "TEST name", "TEST country", "TEST state")
    sql2 = "INSERT INTO Measurements (station, date, precip, tobs) VALUES (?, ?, ?, ?)"
    test_data2 = ("TEST Station", "2026-02-01", 20.5, 30.5)
    
    base.execute_sql(sql1, test_data1)
    base.execute_sql(sql2, test_data2)
    yield base
    base.close() 



@pytest.fixture
def sql_script_test_file(tmp_path):
    """Tworzy tymczasowy plik SQL z polskimi znakami."""
    path = tmp_path / "test_folder" 
    path.mkdir()
    test_file_path = path / "SQL_test_script.sql"
    content = "CREATE TABLE TestTable (name TEXT); INSERT INTO TestTable VALUES ('Łódź');"
    test_file_path.write_text(content, encoding="utf-8")
    return str(test_file_path) 



def test_create_connection(base):
    assert base.conn is not None

def test_create_connection_error():
    base = DataBaseSQL("wrong/path/")
    assert base.conn is None

def test_close_db_connection(base):
    base.close()
    assert base.conn is  None




def test_get_table_columns_wrong_column_name(base):
    result = base.get_table_columns("WRONG TABLE NAME")
    assert result == []

def test_get_table_columns(base_with_data):
    result = base_with_data.get_table_columns("Stations")
    assert result != []
    
def test_get_table_columns_returning_columns_names(base_with_data):
    result = base_with_data.get_table_columns("Stations")
    assert "station" in result
    assert "latitude" in result
    assert "longitude" in result
    assert "elevation" in result
    assert "name" in result
    assert "country" in result
    assert "state" in result
    result = base_with_data.get_table_columns("Measurements")
    assert "station" in result
    assert "date" in result
    assert "precip" in result
    assert "tobs" in result

def test_execute_script_no_file(base):
    result = base.execute_script("no_script_file")
    assert result == False

def test_execute_script(base, sql_script_test_file):
    result = base.execute_script(sql_script_test_file)
    assert result == True


def test_select_all_table_name(base):
    result = base.select_all("NiebezpiecznaTabela")
    assert result == []

def test_update_table_name(base):
    result = base.update("drop table Measurements", "id", "1", 1)
    assert result == []
