/*
A naive way of dealing with the issue of hasn't-loaded-yet
window.onload is a problem if it takes webpage forever to load

Another way is to infuse javascript into html exactly where you want it
to load. 


*/
window.onload = function() {
  /* var clickMeButton = document.getElementById('clickMe');
  clickMeButton.onclick = runTheExample; */ // better is:
  document.getElementById('clickMe').onclick = runTheExample;
}


function runTheExample() {
  // imagine putting anything in here
  alert('running the example');
}


function runTheExample() {

  var myElement = document.getElementById('second');

  // what kind of HTML element is it? ask for its "nodeName"
  var myNodeName = myElement.nodeName;
  //alert(myNodeName); // you alert strings

  if (myElement != null)
  {
    alert(myElement.innerHTML);
  }
  /* you can actually SET things with innerHTML!!! */
  document.getElementById('second').innerHTML = "See how I set the text here?";

  // you can grab arrays of elements: all elements of type paragraph
  var listOfParagraphs = document.getElementsByTagName('p');

  //alert(listOfParagraphs.length);

  var secondParagraph = listOfParagraphs[1];

  alert(secondParagraph.innerHTML);


  // you can navigate the DOM with attributes like those below
  myElement = document.getElementById('second');
  alert(myElement.parentNode.nodeName);

  myElement.childNodes[0];
  myElement.firstChild;
  myElement.lastChild;

  myElement.nextSibling;
  myElement.previousSibling; // you can do this too
  /* <p> previous sibling </p>
  <p> next sibling </p> */



  var anchor = document.getElementById('myAnchor');
  var anchorDestination = anchor.href;
  alert(anchorDestination);

  anchor.href = "http://www.learnvisualstudio.net";

  anchor.setAttribute('href', 'http://www.learnvisualstudio.net');
  anchor.getAttribute('href');
}
