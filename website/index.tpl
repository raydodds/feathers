<!doctype html>
<html>
	<head>
		<title>
			Web Feathers
		</title>
	</head>
	<body>
		<table>
		<tr>
			<td id="opts_panel" width='30%'>
				<form>
					<table>
						<tr>
							Edge Filter:
							<input type='radio' name='filter' value='canny' checked>Canny
							<input type='radio' name='filter' value='sobel'>Sobel
						</tr>
						<br>
						<tr>
							Edge Sampling
						<br>
							Threshold:
							<input type='number' name='threshold' value='5'>
						<br>
							Number:
							<input type='number' name='num_points' value='200'>
						</tr>
						<br>
						<tr>
							Number of Feathers:
							<input type='number' name'num_feath' value='10'>
						</tr>
						<br>
						<tr>
							<input type='submit' value='Apply'>
							<input type='reset'>
						</tr>
					</table>
				</form>
			</td>
		</tr>
		<tr>
			<td id="img_panel" width='50%'>
				<img src='{{img_name}}' >
			</td>
			<td id="vec_panel" width='50%'>
				{{!vec_file}}
			</td>
		</tr>
		</table>
	</body>

</html>
