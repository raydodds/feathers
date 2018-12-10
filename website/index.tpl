<!doctype html>
<html>
	<head>
		<title>
			Web Feathers
		</title>
		<!-- Required meta tags -->
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

		<!-- Bootstrap CSS -->
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
		<link rel="stylesheet" href="/style/style.css">



	</head>
	<body>
		<!-- Optional JavaScript -->
		<!-- jQuery first, then Popper.js, then Bootstrap JS -->
		<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
		<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
		
		
		
		<table>
		<tr id='opts'>
			<form  method='post'>
				<div class='table-responsive'>
				<table class='table'>
				<tbody>
					<tr>
					<td>
						Edge Filter:
						<br>
						<input type='radio' name='filter' value='c' checked>Canny
						<br>
						<input type='radio' name='filter' value='s'>Sobel
					</td>
					<td>
						Edge Sampling
					<br>
						Threshold:
						<input type='number' name='threshold' value='5' min='0' max='255'>
					<br>
						Sample Rate (%):
						<input type='number' name='sample_rate' value='25' min='0' max='100'>
					</td>
					<td>
						Number of Feathers:
						<input type='number' name='num_feath' value='2' min='1'>
						<br>
						<!--
						Border Size:
						<input type='number' name='border_width' value='0'>
						<br>
						Recolor:
						<input type='radio' name='color' value='True' checked>On
						<input type='radio' name='color' value='False'> Off
						-->
					</td>
					<td>
						<input type='submit' value='Apply'>
						<br>
						<input type='reset'>
						<br>
						<a class='button' href='/{{last_name}}'>Back</a>
					</td>
					</tr>
				</tbody>
				</table>
				</div>
			</form>
		</tr>
		<tr>
			% if '.' in name:
				<center>
				<td id="img_panel" width='50%'>
					<img src='{{img_name}}' >
				</td>
				<td id="vec_panel" width='50%'>
					{{!vec_file}}
				</td>
				</center>
			% else:
				% include('nav.tpl', name=name, taxa=taxa)
			% end
		</tr>
		</table>
	</body>

</html>
