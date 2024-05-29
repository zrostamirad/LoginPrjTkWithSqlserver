import pyodbc

try:
    connection = pyodbc.connect(
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=DESKTOP-S5PAQ60;"
        "Database=prj116;"
        "TrustServerCertificate=yes;"
        "Trusted_Connection=yes;")
    print("Connection successful!")
except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    if sqlstate == '08001':
        print("SSL Provider: The certificate chain was issued by an authority that is not trusted.")
    else:
        print("An error occurred:", ex)

