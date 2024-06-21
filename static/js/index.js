//========================>structure<=================================
function create_tr(titre, description, status) {
	let row = document.createElement("tr");
	row.innerHTML =
		`
        <td><input name="checkOne[]" type="checkbox" class="form-check-input" onclick=getRow() /></td>
        <td class="titre">` +
		titre +
		`</td>
        <td class="description">` +
		description +
		`</td>
        <td id="status" class="status text-warning">` +
		status +
		`</td>
        <td>
            <a href="#" id="param" class="btn btn-sm btn-secondary"><img src="../assets/images/update.png" alt=""></a>
            <a href="#" id="delete" onclick="handleDelete(event)" class="btn btn-sm btn-danger"><img src="../assets/images/delete.png" alt=""></a>
        </td>`;
	return row;
}

var fermer = document.getElementById("fermer");
var nouveau = document.getElementById("add-task-form");
var ajout = document.getElementById("ajout");
var del = document.getElementsByClassName("delete");

//========================>functions<=================================

function addToStruct(tr) {
	let tbody = document.getElementById("tbody");
	tbody.appendChild(tr);
}

function handleDelete(event) {
	event.preventDefault(); // Prevent default link behavior

	// Get the table row element containing the delete button
	const row = event.target.closest("tr");
	const status = row.find('td.status').text();
	console.log(status);
	// Remove the table row element from the DOM
	// row.remove();
}

function handleUpdate(event) {
	event.preventDefault();
	const row = event.target.closest("tr");
	if (row) {
		// Make all cells within the row editable
		const cells = row.querySelectorAll("td");
		cells.forEach((cell) => {
			cell.contentEditable = "true";
		});

		// Actions to perform after editing (consider using event listeners)
		cells.forEach((cell) => {
			cell.addEventListener("blur", () => {
				cell.contentEditable = "false"; // Disable editing after user finishes (e.g., on blur)
				// Capture changes here (e.g., cell.textContent)
				// Update UI or send data to server based on captured changes
			});
		});
	} else {
		console.log("no row selected");
	}
}

function delfromstruct(tr) {
	let tbody = document.getElementById("tbody");
	tbody.remove(tr);
}

let data = [];

function addRow() {
	let titre = document.getElementById("titre").value;
	let description = document.getElementById("description").value;
	let status = document.getElementById("status").value;
	let object = {'titre':titre,'description':description,'status':status};
	data.push(object);
	let tr = create_tr(titre, description, status);
	addToStruct(tr);
}

fermer.style.display = "none";
nouveau.style.display = "none";

function getRow() {
	var done_list = [];

	for (let i = 0; i < selectedlist.length; i++) {
		if (selectedlist[i].checked) {
			let row = selectedlist[i].parentNode.parentNode;
			done_list.append(row);
		}
	}
	console.log(done_list);
	return done_list;
}

//========================>listeners<=================================
ajout.addEventListener("click", function () {
	if (nouveau.style.display == "none") {
		nouveau.style.display = "inline-block";
		ajout.style.display = "none";
		fermer.style.display = "inline-block";
	} else {
		nouveau.style.display = "none";
		ajout.style.display = "inline-block";
		fermer.style.display = "none";
	}
});

fermer.addEventListener("click", function () {
	if (nouveau.style.display == "inline-block") {
		nouveau.style.display = "none";
		ajout.style.display = "inline-block";
		fermer.style.display = "none";
	} else {
		nouveau.style.display = "inline-block";
		ajout.style.display = "none";
		fermer.style.display = "inline-block";
	}
});

async function load(number){
	let url = "https://jsonplaceholder.typicode.com/todos";
	let todo_list = document.getElementById('tbody'); 
	try{
		const response = await fetch(url);
		const data = await response.json();
		// document.getElementById('task-list').innerHTML=""
		// alert("you're in load "+data);
		// console.log(data);
		
		// for (let i = 0; i < number; i++) {
		// 	let todo = data[i];
		// 	console.log(todo);
		// }
		$.ajax({
			url: '/process',
			type: 'POST',
			data: JSON.stringify({'data': data,'size':number}),
			contentType: 'application/json; charset=utf-8',
			dataType: 'json',
			beforeSend:function(){
				console.log("sending....")
			},
			success: function(response) {
				console.log("successfully treated",response);
			},
			error: function(error) {
				alert('Error: ' + error.message);
			},
			complete: function(){
				location.reload();
			}
		});
	}catch(error){
		console.error('Error:', error);
	}
}

// async function search(){
// 	let search_input = document.getElementById('search-input').value;
// 	search_input.forEach(letter => {
// 		if (l) {
			
// 		}
// 	});
// }

document.getElementById('load').addEventListener('click',function(event){
	event.preventDefault();
	let number = document.getElementById('loadby').value;
	console.log(number);
	load(parseInt(number));
	
});

// document.getElementById("addrow").addEventListener("click", function () {
// 	addRow();
// 	console.log(data);
// 	document.getElementById("titre").value = "";
// 	document.getElementById("description").value = "";
// });

// document.getElementById('select').addEventListener('click', function(){
//     donelist = getRow();
//     donelist.forEach(element => {
//         console.log(element);
//     });
// });
