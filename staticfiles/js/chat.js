/**
 * Array with Names of all months
 */
 const monthNames = ["Jan.","Feb.","Mar.","Apr.","May.","Jun.","Jul.","Aug.","Sep.","Oct.","Nov.","Dec."];

  async function sendMessage() {

    let fd = new FormData(); //FormData-Objekt generieren das im Body mitgesendet wird
    let token = '{{ csrf_token }}'; //Token generieren
    fd.append('textmessage', messageField.value); //FormData-Objekt enthält die Variable textmessage
    fd.append('csrfmiddlewaretoken', token); //Token muss auch mitgesendet werden
    let messageContainerSaved = messageContainer.innerHTML;
    let dateOfPost = giveActualDate(); //Get actual Date

    //POST-Request an URL chat; Body: Form-Data; Wir müssen warten, deswegen await
    try {
      
      document.getElementById('spinner').classList.remove('d-none'); //Show Spinner

      //FAKE-POSTING
      messageContainer.innerHTML=`
      <div id="deleteMessage">
        <span class="color-gray">${dateOfPost}</span> {{ request.username }}: <i class="color-gray">${messageField.value}</i>
      </div>`+messageContainerSaved;

      //POST TO SERVER AND AWAITING ANSWER
      let response = await fetch('/chat/', {
        method: 'POST',
        body: fd
      });
      
      let json = await response.json();
      let jsonparsed = JSON.parse(json); //Now we have a real JSON

      console.log('Response is ',response);
      console.log('Json is ',json);
      console.log('JsonParsed is ',jsonparsed);
      console.log('JsonParsed is ',jsonparsed.fields.text);
      console.log('JsonParsed is ',jsonparsed.fields.created_at);
      console.log('JsonParsed is ',transformDateIntoGermanFormat(jsonparsed.fields.created_at));
      console.log('JsonParsed is ',jsonparsed.fields.author['0']);

      document.getElementById('deleteMessage').remove(); //Remove FAKE-POSTING
      messageField.value =''; //Empty Input-Field
      document.getElementById('spinner').classList.add('d-none'); //Hide Spinner
      
      //REAL-POSTING
      messageContainer.innerHTML=`
      <div>
        <span class="color-gray">[${transformDateIntoGermanFormat(jsonparsed.fields.created_at)}]</span> ${jsonparsed.fields.author['0']}: <i>${jsonparsed.fields.text}</i>
      </div>`+ messageContainerSaved;
      console.log('Success!');
    }
    catch (e) { 
      //console.log('Error occurred!', e);
      messageContainer.innerHTML=`
      <div id="deleteMessage">
        <span class="color-red">${dateOfPost}</span> {{ request.username }}: <i class="color-red">${messageField.value}</i>
      </div>`+messageContainerSaved;
    }
  }

  
function giveActualDate(){
var currentdate = new Date();  /* Erzeugt eine Datums-Variable mit aktuellem Datum */ 
var datetime =  "[" + currentdate.toLocaleString('default', { month: 'short' }) + ". "
                + currentdate.getDate() + ", "   /* Month */
                + currentdate.getFullYear() + "]";  /* Year */  
                return datetime;
}

/**
 * Receives a string-variable in the format "2010-10-30" and converts it into string "Oct. 10, 2010"
 * @param {string} datetotransform The received string-variable
 * @returns string-variable datumZusGesetzt
 */
 function transformDateIntoGermanFormat(datetotransform) {
	let datum = datetotransform;
	let ersterstrich = datum.indexOf("-");
	let zweiterstrich = datum.lastIndexOf("-");
	let jahr = datum.slice(0, ersterstrich);
	let monat = datum.slice(ersterstrich + 1, zweiterstrich);
  if (monat.length == 2 && monat.slice(0,0) == '0') {
		monat = monat.slice(1,1);
	}
  monat=monthNames[monat-1];
	let tag = datum.slice(zweiterstrich + 1, datum.length);
  if (tag.length == 2 && tag.slice(0,1) == '0') {
		tag = tag.slice(-1);
	}
	let datumZusGesetzt = monat + " " + tag + ", " + jahr;
	return datumZusGesetzt;
}