document.addEventListener('DOMContentLoaded', function() {
	let cts = document.querySelectorAll('.fas');
	let ccss = document.querySelectorAll('.editPos')

	cts.forEach(cta => {
		cta.addEventListener('click', (movie) => {
			let movided = movie.target.getAttribute('value')
			let movId = movie.target.getAttribute('id')
			var likedId = movId + ',,';
			fetch(`/likes/${movId}`)
			.then(response => response.json())
			.then(message => {
				if(message.Liked){
					document.getElementById(movId).style.color = 'red';
					document.getElementById(likedId).innerText = message.totalLiked;
				}else{
					if (message.totalLiked !== 0 ){
						document.getElementById(likedId).innerText = message.totalLiked;
					}else {
						document.getElementById(likedId).innerText = '';
					}
					document.getElementById(movId).style.color = 'grey';
				}
			})
			
		})
	})
	ccss.forEach(cc => {
		cc.addEventListener('click', (cl) => {
			let data = cl.target.getAttribute('id')
			let daT = cl.target.getAttribute('value')
			var xxx = data.replace(",", "")
			var finaId = ',' + xxx
			var valueInner = document.getElementById(finaId).innerHTML
			val = `<textarea class="text" id="hi">${valueInner} </textarea>`
			document.getElementById(finaId).innerHTML = val;
			but = `<div class='save' id='ch' onclick="hello('${xxx}');"> Save </div>`
			var editVal = xxx + ','
			document.getElementById(editVal).innerHTML = but

		})
	})

});

function hello(y){
	var data = document.querySelector('.save')
	var edit = document.getElementById("hi").value
	fetch(`/updatepost/${y}`,{
		method: 'PUT',
		body: JSON.stringify({
			userBio: edit
		})
	})
	var finalCeck = "," + y
	setTimeout(function(){document.getElementById(finalCeck).innerHTML = edit;}, 50)
	setTimeout(function() {document.querySelector('.save').innerHTML='Edit';}, 100)
}

function test(x){
	//console.log(x)
}

