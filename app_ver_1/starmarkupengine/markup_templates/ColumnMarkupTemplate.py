from string import Template

class ColumnMarkupTemplate:
	def __init__(self, column_json_value):
		self.align = column_json_value["align"] if "align" in column_json_value else "left"
		self.indent = column_json_value["value"]["indent"] if "indent" in column_json_value["value"] else None
		self.columns = column_json_value["value"]["columns"]

	def rowTemplate(self, column):
		col_left = column["left"].strip()
		col_right = column["right"].strip()
		col_short = column["short"].strip() if "short" in column.keys() else ""	
  
		left = Template("left $left; ").substitute(left = col_left) if bool(col_left) is True else ""
		short = Template("short $short; ").substitute(short = col_short) if bool(col_short) is True and bool(left) is True else ""
		right = Template("right $right").substitute(right = col_right) if bool(col_right) is True else ""	
		
		col = left + short + right

		return "[column: " + col + "]"
		
	def getColumnMarkup(self):
		align = Template("[align: $align]").substitute(align = self.align)
		indent = Template("[col: indent $indent]").substitute(indent = self.indent) if bool(self.indent) else ""
		rows = ""
		i = 0
		for column in self.columns:
			i += 1
			rows += self.rowTemplate(column) + "\n"
			if "sub" in column:	
				for sub in column['sub']:
					rows += "[mag: w 1; h 1][col: indent 5mm]" + self.rowTemplate(sub) + f"[col: indent {self.indent}][mag]" + "\n"
				
			rows += "\n" if i < len(self.columns) else "[col: indent 0mm]\n"

		return align + indent + rows
