from fastapi import FastAPI, HTTPException
from database import Database
from search import PartSearch
import uvicorn

app = FastAPI()
db = Database(user='carparts_owner', password='an0Huk9MyIAD', host='ep-noisy-meadow-a53mq97p.us-east-2.aws.neon.tech', port='', database='carparts')
part_search = PartSearch(db)


@app.post("/search/part/")
async def search_parts(request_body: dict):
    try:
        mark_name = request_body.get("mark_name")
        mark_list = request_body.get("mark_list")
        part_name = request_body.get("part_name")
        params = request_body.get("params")
        price_gte = request_body.get("price_gte")
        price_lte = request_body.get("price_lte")
        page = request_body.get("page", 1)
        result = part_search.search_parts(mark_name, mark_list, part_name, params, price_gte, price_lte, page)
        response = []

        for row in result["response"]:
            response.append({
                "mark": {
                    "id": row[0],
                    "name": row[1],
                    "producer_country_name": row[2]
                },
                "model": {
                    "id": row[3],
                    "name": row[4]
                },
                "name": row[5],
                "json_data": row[6],
                "price": row[7]
            })

        return {
            "response": response,
            "count": result["count"],
            "summ": result["summ"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
