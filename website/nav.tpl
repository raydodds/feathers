<center>
<table>
	<tr>
		<td>
			{{name}}
		</td>
		<td>
		<table>
			% for subtaxa in taxa:
				<tr>
					<td>
						<a class='button' href='/{{name}}/{{subtaxa}}'>{{subtaxa}}</a>
					</td>
				</tr>
			% end
		</table>
		</td>
	</tr>
</table>
<center>
