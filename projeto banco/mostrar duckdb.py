import duckdb
con = duckdb.connect("./bancoProjeto.duckdb")
resultado = con.sql("SELECT * FROM client")
print(resultado)