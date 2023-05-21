class Contraintes:
    def __init__(self, left: tuple, right: tuple, cursor) -> None:
        self.left = left
        self.right = right
        self.cursor = cursor
        self.applied_to = []
    
    def is_satisfied_by(self, table: str) -> bool:
        raise Exception("Not implemented")

    def is_head_satisfied_by(self, table: str) -> bool:
        raise Exception("Not implemented")

    def apply_to(self, table: str) -> None:
        self.applied_to.append(table)

    def is_applied_to(self, table: str) -> bool:
        return table in self.applied_to

class TGD(Contraintes):
    def is_satisfied_by(self, table: str) -> bool:
        if self.left[0] != table:
            return False
        command = f"SELECT {', '.join(x for x in self.left[1])} FROM {table};"
        self.cursor.execute(command)
        command_result = self.cursor.fetchall()
        return len(command_result) > 0

    def is_head_satisfied_by(self, table: str) -> bool:
        command = f"SELECT {', '.join(x for x in self.left[1])} FROM {table};"
        self.cursor.execute(command)
        command_result = self.cursor.fetchall()
        for t in command_result:
            conditions = " AND ".join(f"{x} {f'= {y}' if y else 'IS NOT NULL'}" for y, x in zip(t, self.left[1]))
            command = f"SELECT * FROM {self.right[0]} WHERE {conditions};"
            self.cursor.execute(command)
            command_result = self.cursor.fetchall()
            if len(command_result) == 0:
                return False
        return True

    def add_missing_tuples(self, table: str) -> None:
        command = f"SELECT {', '.join(x for x in self.left[1])} FROM {table};"
        self.cursor.execute(command)
        command_result = self.cursor.fetchall()
        for t in command_result:
            conditions = " AND ".join(f"{x} {f'= {y}' if y else 'IS NOT NULL'}" for y, x in zip(t, self.left[1]))
            command = f"SELECT * FROM {self.right[0]} WHERE {conditions};"
            self.cursor.execute(command)
            command_result = self.cursor.fetchall()
            if len(command_result) == 0:
                command = f"INSERT INTO {self.right[0]} ({', '.join(x for x in self.right[1])}) VALUES ({', '.join(str(x) for x in t)})"
                self.cursor.execute(command)
                conditions = " AND ".join(f"{x} = {y}" for x, y in zip(self.left[1], t))
                command = f"SELECT * FROM {self.right[0]} WHERE {conditions};"
                self.cursor.execute(command)
                command_result = self.cursor.fetchall()
                if len(command_result) == 0:
                    raise Exception("Something went wrong")

class EGD(Contraintes):
    def is_satisfied_by(self, table: str) -> bool:
        if not any(left[0] == table for left in self.left):
            return False
        command = f"SELECT {', '.join(attr for x in self.left for attr in x[1])} FROM {table};"
        self.cursor.execute(command)
        command_result = self.cursor.fetchall()
        return len(command_result) > 0

    def is_head_satisfied_by(self, table: str) -> bool:
        join = []
        for left in self.left:
            table_name = left[0]
            if table_name == table:
                continue
            join_text = ""
            join_text += f"JOIN {table_name} "
            for attr in left[1]:
                join_text += f"ON {table_name}.{attr} = {table}.{attr}"
            join.append(join_text)
        join = " ".join(join)
        
        condition = []
        for i, right in enumerate(self.right):
            for right2 in self.right[i + 1:]:
                for item1, item2 in zip(right[1], right2[1]):
                    condition_text = f"{right[0]}.{item1} != {right2[0]}.{item2}"
                    condition.append(condition_text)
        condition = " AND ".join(condition)

        command = f"SELECT * FROM {table} {join} WHERE {condition};"
        self.cursor.execute(command)
        command_result = self.cursor.fetchall()
        return len(command_result) == 0

    def equalize(self, table: str) -> None:
        join = []
        for left in self.left:
            table_name = left[0]
            if table_name == table:
                continue
            join_text = ""
            join_text += f"JOIN {table_name} "
            for attr in left[1]:
                join_text += f"ON {table_name}.{attr} = {table}.{attr}"
            join.append(join_text)
        join = " ".join(join)
        
        """ select = []
        condition = []
        for i, right in enumerate(self.right):
            for item in right[1]:
                select.append(f"{right[0]}.{item}")
            for right2 in self.right[i + 1:]:
                for item1, item2 in zip(right[1], right2[1]):
                    condition_text = f"{right[0]}.{item1} != {right2[0]}.{item2}"
                    condition.append(condition_text)
        select = ", ".join(select)
        condition = " AND ".join(condition)

        command = f"SELECT {select} FROM {table} {join} WHERE {condition};"
        self.cursor.execute(command)
        command_result = self.cursor.fetchall()
        for t in command_result:
            pass"""

        from_table = self.right[0][0]
        from_table_attrs = self.right[0][1]
        for right in self.right[1:]:
            set_value = []
            table = right[0]
            for from_attr, right_attr in zip(from_table_attrs, right[1]):
                set_value_text = f"{right_attr} = {from_table}.{from_attr}"
                set_value.append(set_value_text)
            set_value = ", ".join(set_value)
            
            where = []
            for left in self.left:
                table_name = left[0]
                if table_name == table:
                    continue
                where_text = ""
                for attr in left[1]:
                    where_text += f"{table_name}.{attr} = {table}.{attr}"
                where.append(where_text)
            where = " AND ".join(where)
            command = f"UPDATE {table} SET {set_value} FROM {from_table} WHERE {where};"
            self.cursor.execute(command)

def standard_chase(contraintes: list, tables: list) -> bool:
    found_new_solution = False
    while not found_new_solution:
        for contrainte in contraintes:
            for table in tables:
                if contrainte.is_satisfied_by(table) and not contrainte.is_head_satisfied_by(table) and not contrainte.is_applied_to(table):
                    if isinstance(contrainte, TGD):
                        contrainte.add_missing_tuples(table)
                    elif isinstance(contrainte, EGD):
                        contrainte.equalize(table)
                    else:
                        raise Exception("Unknown constraint type")
                    contrainte.apply_to(table)
                    found_new_solution = True
    
    return all(e.is_satisfied_by(table) for e in contraintes for table in tables)