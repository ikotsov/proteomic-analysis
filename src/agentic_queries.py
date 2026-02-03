from mcp.server.fastmcp import FastMCP
import psycopg
from psycopg.rows import dict_row

mcp = FastMCP("ProteinExplorer")

DB_PARAMS = {
    "dbname": "prot",
    "user": "postgres",
    "host": "localhost",
    "port": 5432
}


@mcp.tool()
def get_mouse_brain_map():
    """
    Fetches protein names, their associated brain regions, 
    and Gene Ontology (GO) functions from a database.
    """
    try:
        with psycopg.connect(**DB_PARAMS) as conn:
            # python will return a list of tuples after fetching from the db,
            # we are using dict_row to provide a list of dictionaries to the LLM instead
            # for easier parsing
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("""
                    SELECT 
                        p.entry_name, 
                        p.protein_names, 
                        rpm.regions_id AS region, 
                        g.name AS go_function
                    FROM proteins p
                    JOIN regions_proteins_map rpm ON p.entry = rpm.protein_id
                    JOIN protein_go_map pgm ON p.entry = pgm.protein_id
                    JOIN go g ON pgm.go_id = g.id
                    ORDER BY rpm.regions_id
                    LIMIT 5;
                """)
                return cur.fetchall()
    except Exception as e:
        return f"Database error: {str(e)}"


if __name__ == "__main__":
    mcp.run()
