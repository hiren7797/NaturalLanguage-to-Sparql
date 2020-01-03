import self as self
import secrets
import string
from .constants import Color
class Prefix():
    def __init__(self):
        self.prefixs=[]
    def add_prefix(self,prefix,prefix_type):
        if [prefix,prefix_type] not in self.prefixs:
            self.prefixs.append([prefix,prefix_type])
    def get_prefix(self):
        return self.prefixs

    def get_just_prefix_name(self,prefix):
        if prefix != str(None):
            return prefix.rsplit('?', 1)[1]
        else:
            return prefix
columns=[]
conditions=[]
default=[]
junc=[]
class Select():

    def add_column(self, column, column_type):
        if [column, column_type] not in columns:
            columns.append([column, column_type])

    def get_just_column_name(self, column):
        if column != str(None):
            return str(column.rsplit(maxsplit=1))
        else:
            return str(column)

    def print_column(self, selection):
        global column
        column = selection[0]
        column_type = selection[1]
        if column is None:
            if column_type is not None:
                if 'COUNT' in column_type:
                    return Color.BOLD + 'COUNT(' + Color.END + '*' + Color.BOLD + ')' + Color.END
                else:
                    return '*'
            else:
                return '*'
        else:
            if 'DISTINCT' in column_type:
                if 'COUNT' in column_type:
                    return Color.BOLD + 'COUNT(DISTINCT ' + Color.END + str(column) + Color.BOLD + ')' + Color.END
                else:
                    return Color.BOLD + 'DISTINCT ' + Color.END + str(column)
            if 'COUNT' in column_type:
                return Color.BOLD +'('+ 'COUNT(' + Color.END + str(column) + Color.BOLD  +')'+ ' AS '+'?'+Select.random(self)+')'+Color.END
            elif 'AVG' in column_type:
                return Color.BOLD + '('+'AVG(' +Color.END +str(column) + Color.BOLD + ')'+' AS '+'?'+Select.random(self)+')'+Color.END
            elif 'SUM' in column_type:
                return Color.BOLD + '('+'SUM(' + Color.END + str(column) + Color.BOLD + ')'+' AS '+'?'+Select.random(self)+')'+Color.END
            elif 'MAX' in column_type:
                return Color.BOLD + '('+'MAX(' + Color.END + str(column) + Color.BOLD + ')'+' AS '+'?'+Select.random(self)+ ')'+Color.END
            elif 'MIN' in column_type:
                return Color.BOLD + '('+'MIN(' + Color.END + str(column) + Color.BOLD + ')'+' AS '+'?'+Select.random(self)+')'+Color.END
            else:
                return str(column)
    def random(self):
        N=5
        res = ''.join(secrets.choice(string.ascii_lowercase)
                  for i in range(N))
        return res

    def __str__(self):
        select_string = ''
        for i in range(0, len(columns)):
            if i == (len(columns) - 1):
                select_string = select_string +'?' + str(self.print_column(columns[i]))
            else:
                select_string = select_string +'?' + str(self.print_column(columns[i])) +' '

        return Color.BOLD +'PREFIX ab: <http://www.semanticweb.org/dell/ontologies/2019/11/untitled-ontology-10#> '+'\n'+'SELECT ' + Color.END + select_string

    def print_json(self, output):
        if len(columns) >= 1:
            if len(columns) == 1:
                output.write('\t"select": {\n')
                output.write('\t\t"column": "' + self.get_just_column_name(str(columns[0][0])) + '",\n')
                output.write('\t\t"type": "' + str(columns[0][1]) + '"\n')
                output.write('\t},\n')
            else:
                output.write('\t"select": {\n')
                output.write('\t\t"columns": [\n')
                for i in range(0, len(columns)):
                    if i == (len(columns) - 1):
                        output.write(
                            '\t\t\t{ "column": "' + self.get_just_column_name(str(columns[i][0])) + '",\n')
                        output.write('\t\t\t  "type": "' + str(columns[i][1]) + '"\n')
                        output.write('\t\t\t}\n')
                    else:
                        output.write(
                            '\t\t\t{ "column": "' + self.get_just_column_name(str(columns[i][0])) + '",\n')
                        output.write('\t\t\t  "type": "' + str(columns[i][1]) + '"\n')
                        output.write('\t\t\t},\n')
                output.write('\t\t]\n')
                output.write('\t},\n')
        else:
            output.write('\t"select": {\n')
            output.write('\t},\n')



class From():
    table = ''

    def __init__(self, table=None):
        if table is not None:
            self.table = table
        else:
            self.table = ''

    def set_table(self, table):
        self.table = table

    def get_table(self):
        return self.table


    def __str__(self):
        str_string=''
        string=''
        count=0
        count1=len(columns)
        for i in columns:
            count=count+1
            if count==1 and count==len(columns):
             str_string = str_string + '?' + From.random1(self) + ' ' + 'ab:' + str(i[0]) + ' ?' + str(i[0]) + '.' + '\n'
            elif count ==1:
             str_string = str_string + '?'+From.random1(self) +' '+ 'ab:'+ str(i[0]) +' ?' +str(i[0])+';'+'\n'
            elif count ==len(columns):
             str_string=str_string+' '+'ab:'+str(i[0])+' ?'+str(i[0])+'.'+'\n'
            else:
             str_string=str_string+' '+'ab:'+str(i[0])+' ?'+str(i[0])+';'+'\n'
        if len(conditions)>=1:
            for i in range(0,len(conditions)):
                str_string=str_string+'?'+From.random1(self)+' '+'ab:'+str(default[i]) + ' '+str(default[i])+'.'+'\n'
        if len(conditions)>=1:

            if len(conditions) >1:
                for i in range(0, len(conditions)-1):
                        string += '\n' + Color.BOLD + 'Filter' + '(' + str(conditions[i][1]) +' ' +str(junc[i]) +' '+str(conditions[i+1][1]) +')'
            elif len(conditions)==1:
                        string += '\n' + Color.BOLD+ 'Filter' +'(' +str(conditions[i][1])+')'

            str_string='\n' + Color.BOLD + 'WHERE '+'{ ' + str_string + string +'\n' +'}'
            return str_string

        else:
            str_string='\n' + Color.BOLD+'WHERE '+'{ ' + str_string + '\n' +'}'
            return str_string



    def random(self):
        N=5
        res = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                  for i in range(N))
        return res

    def random1(self):
        N=1
        res = ''.join(secrets.choice(string.ascii_lowercase)
                  for i in range(N))
        return res
    def print_json(self, output):
        if self.table != '':
            output.write('\t"from": {\n')
            output.write('\t\t"table": "' + str(self.table) + '"\n')
            output.write('\t},\n')
        else:
            output.write('\t"from": {\n')
            output.write('\t},\n')


class Join():
    tables = []
    links = []

    def __init__(self):
        self.tables = []
        self.links = []

    def add_table(self, table):
        if table not in self.tables:
            self.tables.append(table)

    def set_links(self, links):
        self.links = links

    def get_tables(self):
        return self.tables

    def get_links(self):
        return self.links

    def __str__(self):
        if len(self.links) >= 1:
            string = ''
            for i in range(0, len(self.links)):
                string += '\n' + Color.BOLD + 'INNER JOIN ' + Color.END + str(
                    self.links[i][1][0]) + '\n' + Color.BOLD + 'ON ' + Color.END + str(self.links[i][0][0]) + '.' + str(
                    self.links[i][0][1]) + ' = ' + str(self.links[i][1][0]) + '.' + str(self.links[i][1][1])
            return string
        elif len(self.tables) >= 1:
            if len(self.tables) == 1:
                return '\n' + Color.BOLD + 'NATURAL JOIN ' + Color.END + self.tables[0]
            else:
                string = '\n' + Color.BOLD + 'NATURAL JOIN ' + Color.END
                for i in range(0, len(self.tables)):
                    if i == (len(self.tables) - 1):
                        string += str(self.tables[i])
                    else:
                        string += str(self.tables[i]) + ', '
                return string
        else:
            return ''

    def print_json(self, output):
        if len(self.tables) >= 1:
            if len(self.tables) == 1:
                output.write('\t"join": {\n')
                output.write('\t\t"table": "' + str(self.tables[0]) + '"\n')
                output.write('\t},\n')
            else:
                output.write('\t"join": {\n')
                output.write('\t\t"tables": [')
                for i in range(0, len(self.tables)):
                    if i == (len(self.tables) - 1):
                        output.write('"' + str(self.tables[i]) + '"')
                    else:
                        output.write('"' + str(self.tables[i]) + '", ')
                output.write(']\n')
                output.write('\t},\n')
        else:
            output.write('\t"join": {\n')
            output.write('\t},\n')


class Condition():
    column = ''
    column_type = ''
    operator = ''
    value = ''

    def __init__(self, column, column_type, operator, value):
        self.column = column
        self.column_type = column_type
        self.operator = operator
        self.value = value

    def get_column(self):
        return self.column

    def get_column_type(self):
        return self.column_type

    def get_operator(self):
        return self.operator

    def get_value(self):
        return self.value

    def get_in_list(self):
        return [self.column, self.column_type, self.operator, self.value]

    def get_just_column_name(self, column):
        if column != str(None):
            return column.rsplit('?', 1)[1]
        else:
            return column

    def get_column_with_type_operation(self, column, column_type):
        if column_type is None:
            return self.column
        else:
            return Color.BOLD + str(column_type) + '(' + Color.END + self.column + Color.BOLD + ')' + Color.END

    def get_pretty_operator(self, operator):
        if operator == 'BETWEEN':
            return Color.BOLD + 'BETWEEN' + Color.END + ' OOV ' + Color.BOLD + 'AND' + Color.END
        else:
            return Color.BOLD + operator + Color.END

    def __str__(self):
        return str(self.get_column_with_type_operation(self.column, self.column_type)) + ' ' + str(
            self.get_pretty_operator(self.operator)) + ' ' + str(self.value)

    def print_json(self, output):

        output.write(
            '\t\t\t{ "column": "' + self.get_just_column_name(str(self.column)) + '",\n\t\t\t  "type": "' + str(
                self.column_type) + '",\n\t\t\t  "operator": "' + str(self.operator) + '",\n\t\t\t  "value": "' + str(
                self.value) + '"\n\t\t\t}')

class Where():

    def __init__(self, clause=None):
        if clause is not None:
            conditions.append([None, clause])

        else:
            conditions = []

    def add_condition(self, junction, clause,loc):
        conditions.append([junction, clause])
        default.append(loc)
        junc.append(junction)


    def __str__(self):
        string = ''

        if len(conditions) >= 1:
            for i in range(0, len(conditions)):
                if i == 0:
                    string += '\n' + Color.BOLD + 'Filter' +'('+ str(conditions[i][0])
                else:
                    string += '\n' + Color.BOLD + str(conditions[i][0]) + Color.END + ' ' + str(
                        conditions[i][1]) +')'

            return ''
        else:
            return ''

    def print_json(self, output):
        if len(conditions) >= 1:
            if len(conditions) == 1:
                output.write('\t"where": {\n')
                output.write('\t\t"condition": [\n')
                conditions[0][1].print_json(output)

                output.write('\n')
                output.write('\t\t]\n')
                output.write('\t},\n')
            else:
                output.write('\t"where": {\n')
                output.write('\t\t"conditions": [\n')
                for i in range(0, len(conditions)):
                    if i != 0:
                        output.write('\t\t\t{\n\t\t\t  "operator": "' + str(conditions[i][0]) + '"\n\t\t\t},\n')
                    conditions[i][1].print_json(output)
                    if i != (len(conditions) - 1):
                        output.write(',')
                    output.write('\n')
                output.write('\t\t]\n')
                output.write('\t},\n')
        else:
            output.write('\t"where": {\n')
            output.write('\t},\n')

class GroupBy():
    column = None

    def __init__(self, column=None):
        if column is not None:
            self.column = column
        else:
            self.column = None

    def set_column(self, column):
        self.column = column

    def get_column(self):
        return self.column

    def get_just_column_name(self, column):
        if column != str(None):
            return column.rsplit('?', 1)[1]
        else:
            return column

    def __str__(self):
        if self.column is not None:
            return '\n' + Color.BOLD + 'GROUP BY ' + Color.END + str(self.column)
        else:
            return ''

    def print_json(self, output):
        if self.column is not None:
            output.write('\t"group_by": {\n')
            output.write('\t\t"column": "' + self.get_just_column_name(str(self.column)) + '"\n')
            output.write('\t},\n')
        else:
            output.write('\t"group_by": {\n')
            output.write('\t},\n')


class OrderBy():
    columns = []

    def __init__(self):
        self.columns = []

    def add_column(self, column, order):
        if [column, order] not in self.columns:
            self.columns.append([column, order])

    def get_columns(self):
        return self.columns

    def __str__(self):
        if self.columns != []:
            string = Color.BOLD + 'ORDER BY '+ Color.END
            for i in range(0, len(self.columns)):
                loc=self.columns[i][1]
                if i == (len(self.columns) - 1):
                    string +=  loc +'(' + self.columns[i][0] +')'
                else:
                    string += loc + '('+ self.columns[i][0] + ')'
            return '\n' + string
        else:
            return ''

    def print_json(self, output):
        if len(self.columns) >= 1:
            if len(self.columns) == 1:
                output.write('\t"select": {\n')
                output.write('\t\t"column": "' + str(self.columns[0][0]) + '",\n')
                output.write('\t\t"order": "' + str(self.columns[0][1]) + '"\n')
                output.write('\t},\n')
            else:
                output.write('\t"select": {\n')
                output.write('\t\t"columns": [\n')
                for i in range(0, len(self.columns)):
                    if i == (len(self.columns) - 1):
                        output.write('\t\t\t{ "column": "' + str(self.columns[i][0]) + '",\n')
                        output.write('\t\t\t  "order": "' + str(self.columns[i][1]) + '"\n')
                        output.write('\t\t\t}\n')
                    else:
                        output.write('\t\t\t{ "column": "' + str(self.columns[i][0]) + '",\n')
                        output.write('\t\t\t  "order": "' + str(self.columns[i][1]) + '"\n')
                        output.write('\t\t\t},\n')
                output.write('\t\t]\n')
                output.write('\t},\n')
        else:
            output.write('\t"select": {\n')
            output.write('\t},\n')


class Query():
    select = None
    _from = None
    join = None
    where = None
    group_by = None
    order_by = None

    def __init__(self, select=None, _from=None, join=None, where=None, group_by=None, order_by=None):
        if select is not None:
            self.select = select
        else:
            self.select = None
        if _from is not None:
            self._from = _from
        else:
            self._from = None
        if join is not None:
            self.join = join
        else:
            self.join = None
        if where is not None:
            self.where = where
        else:
            self.where = None
        if group_by is not None:
            self.group_by = group_by
        else:
            self.group_by = None
        if order_by is not None:
            self.order_by = order_by
        else:
            self.order_by = None

    def set_select(self, select):
        self.select = select

    def get_select(self):
        return self.select

    def set_from(self, _from):
        self._from = _from

    def get_from(self):
        return self._from

    def set_join(self, join):
        self.join = join

    def get_join(self):
        return self.join

    def set_where(self, where):
        self.where = where

    def get_where(self):
        return self.where

    def set_group_by(self, group_by):
        self.group_by = group_by

    def get_group_by(self):
        return self.group_by

    def set_order_by(self, order_by):
        self.order_by = order_by

    def get_order_by(self):
        return self.order_by

    def __str__(self):
        return '\n' + str(self.select) + str(self._from) + str(self.join) + str(self.where) + str(self.group_by) + str(
            self.order_by) + '\n'

    def print_json(self, filename="output.json"):
        output = open(filename, 'a')
        output.write('{\n')
        self.select.print_json(output)
        self._from.print_json(output)
        self.join.print_json(output)
        self.where.print_json(output)
        self.group_by.print_json(output)
        self.order_by.print_json(output)
        output.write('}\n')
        output.close()
