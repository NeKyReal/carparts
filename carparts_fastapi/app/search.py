from database import Database


class PartSearch:
    def __init__(self, db: Database):
        self.db = db

    def search_parts(self, mark_name=None, mark_list=None, part_name=None, params=None, price_gte=None, price_lte=None, page=1):
        try:
            base_query = """
                SELECT parts_mark.id AS mark_id, parts_mark.name AS mark_name, parts_mark.producer_country_name, 
                parts_model.id AS model_id, parts_model.name AS model_name, parts_part.name AS part_name, 
                parts_part.json_data, parts_part.price 
                FROM parts_part
                JOIN parts_mark ON parts_part.mark_id = parts_mark.id
                JOIN parts_model ON parts_part.model_id = parts_model.id
                WHERE parts_part.is_visible = TRUE
            """
            conditions = []

            if mark_list:
                mark_list_str = ','.join(['%s'] * len(mark_list))
                conditions.append(f"parts_mark.id IN ({mark_list_str})")
            if mark_name:
                conditions.append("parts_mark.name ILIKE %s")
            if part_name:
                conditions.append("(parts_part.name ILIKE %s OR parts_part.name ILIKE %s)")
            if params:
                for key, value in params.items():
                    if key == 'is_new_part':
                        conditions.append(f"(parts_part.json_data ->> '{key}')::boolean = %s")
                    else:
                        conditions.append(f"parts_part.json_data ->> '{key}' = %s")
            if price_gte:
                conditions.append("parts_part.price >= %s")
            if price_lte:
                conditions.append("parts_part.price <= %s")
            conditions_str = ""
            if conditions:
                conditions_str = " AND ".join(conditions)
                base_query += " AND " + conditions_str

            count_query = f"""
                SELECT COUNT(*), SUM(parts_part.price)
                FROM parts_part
                JOIN parts_mark ON parts_part.mark_id = parts_mark.id
                JOIN parts_model ON parts_part.model_id = parts_model.id
                WHERE parts_part.is_visible = TRUE
                {"AND " + conditions_str if conditions else ''}
            """
            pagination_query = base_query + " LIMIT 10 OFFSET %s"
            offset = (page - 1) * 10
            query_params = []

            if mark_list:
                query_params.extend(mark_list)
            if mark_name:
                query_params.append(f"%{mark_name}%")
            if part_name:
                query_params.append(f"%{part_name}%")
                query_params.append(f"%{part_name.capitalize()}%")
            if params:
                for key, value in params.items():
                    query_params.append(value)
            if price_gte:
                query_params.append(price_gte)
            if price_lte:
                query_params.append(price_lte)

            pagination_query_params = query_params + [offset]
            count_result = self.db.execute_query(count_query, query_params)
            count = count_result[0][0] if count_result else 0
            summ = count_result[0][1] if count_result else 0
            parts_result = self.db.execute_query(pagination_query, pagination_query_params)

            return {
                "response": parts_result,
                "count": count,
                "summ": summ
            }

        except Exception as e:
            print(f"Error during search_parts execution: {str(e)}")
            raise e
