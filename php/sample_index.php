<!DOCTYPE HTML>
<?php
$pythonScript = '../royalrumblepool.py';
?>
<html>
<head>
	<title>Royal Rumble Pool - Sample Page</title>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1" />
	<meta property="og:title" content="Royal Rumble Pool - Sample Page" />
	<meta property="og:description" content="A sample page for the Royal Rumble Pool" />
</head>
<body>
	<section>
		<h2>Enter the Rumble!</h2>
		<p>Enter your name and leave a comment to be assigned an entry number</p>
		<form id="entryForm" method="post" action="./sample_post_entry.php">
			<label for="name">Name</label>
			<input type="text" name="entry_name" id="entry_name" maxlength="20" placeholder="required" required />
			<label for="comment">Comment</label>
			<input type="text" name="entry_comment" id="entry_comment" maxlength="50" placeholder="optional" />
			<input type="submit" value="Get your Entry Number" />
		</form>
		<h2 id="entryAck" hidden />
	</section>
	<hr/>
	<section>
		<h2>Current Entries (Royal Rumble SAMPLE)</h2>
		<table id="entryTable">
			<thead>
				<tr>
					<th>Entrant Name</th>
					<th>Entrant Comment</th>
					<th>Entry Number</th>
				</tr>
			</thead>
			<tbody>
			<?php
			$cmd = 'python3 '.$pythonScript.' -d';
			$output = shell_exec($cmd);
			$data = json_decode($output, true)['data'];
			if(empty($data)) {
			?>
				<tr>
					<td>Be the first to enter!</td>
					<td>Be the first to enter!</td>
					<td>Be the first to enter!</td>
				</tr>
			<?php
			}
			foreach($data as $entrant) {
			?>
				<tr>
					<td><?php echo $entrant['name']; ?></td>
					<td><?php echo $entrant['comment']; ?></td>
					<td><?php echo $entrant['number']; ?></td>
				</tr>
			<?php
			}
			?>
			</tbody>
		</table>
	</section>
	<hr/>
	<section>
		<h2>Previous Winners</h2>
		<?php
		$cmd = 'python3 '.$pythonScript.' -winners';
		$output = shell_exec($cmd);
		$data = json_decode($output, true)['data'];
		foreach($data as $year_results) {
			$year = $year_results['year'];
			$winners = $year_results['winners'];
		?>
			<h3>Royal Rumble <?php echo $year; ?></h3>
			<table id="winnerTable">
				<thead>
					<tr>
						<th>Entrant Name</th>
						<th>Entrant Comment</th>
						<th>Entry Number</th>
					</tr>
				</thead>
				<tbody>
				<?php
				foreach($winners as $entrant) {
				?>
					<tr>
						<td><?php echo $entrant['name']; ?></td>
						<td><?php echo $entrant['comment']; ?></td>
						<td><?php echo $entrant['number']; ?></td>
					</tr>
				<?php
				}
				?>
				</tbody>
			</table>
		<?php
		}
		?>
	</section>
	<hr/>
	<footer>
		<ul>
			<li>This is a sample page for the <a href="https://github.com/FancyJesse/royal-rumble-pool">Royal Rumble Pool</a></li>
			<li>See a live and more decorated sample on <a href="http://royalrumblepool.fancyjesse.com">RoyalRumblePool.FancyJesse.com</a></li>
		</ul>
	</footer>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
	<script type="text/javascript">
		var ef = $('#entryForm');
		var audio = document.createElement('audio');
		audio.setAttribute('src', './audio/countdown.mp3');
		ef.submit(function (ev) {
			$.ajax({
				type: ef.attr('method'),
				url: ef.attr('action'),
				dataType: 'json',
				data: ef.serialize(),
				success: function (data) {
					if(data['success']){
						$('#entryForm :input').prop('readonly', true);
						$('input[type="submit"]').prop('disable', false);
						$('#entryForm').hide();
						var newRow =
							'<tr><td>' + $('#entry_name').val().trim() +
							'</td><td>' + $('#entry_comment').val().trim() +
							'</td><td>' + data['data'].substring(
								data['data'].lastIndexOf('#') + 1,
								data['data'].lastIndexOf('!')) +
							'</td></tr>';
						function countdown() {
							if (audio.readyState) {
								audio.play();
							}
							var count = 10;
							$('#entryAck').empty();
							$('#entryAck').append('<h1>' + count-- + '</h1>');
							var interval = window.setInterval(function () {
								$('#entryAck').empty();
								if(count == 0) {
									window.clearInterval(interval);
									$('#entryAck').append(data['data']);
									$('#entryTable').append(newRow);
								} else {
									$('#entryAck').append('<h1>' + count-- + '</h1>');
								}
							} , 1000);
						}
						countdown();
					} else {
						$('#entryAck').empty();
						$('#entryAck').append(data['data']);
					}
					$('#entryAck').show();
				}
			});
			ev.preventDefault();
		});
	</script>
</body>
</html>
