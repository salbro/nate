/* What is jQuery? It is a Javascript library.
It's concernes are primarily DOM, Ajax, events, and effects.

The jQuery function takes a context (in this case document)
when we call the ready method, we're asking jQuery to evaluate when
the context is ready, and run the passed-in "handler code"

There is a short-cut to typing in "jQuery":> The dollar sign ($)

$ = jQuery

All such information can be found in the jQuery API reference.
jQuery function takes elements, ids, classes, etc.

You might also see stuff like
$('.importantText');
$('#myFirstParagraph');
$('p').fadeOut();
$('p').fadeOut().fadeIn(500);
All such things return an *object of type jQuery*.

A jQuery object is a collection of DOM elements that match the selector of the input parameter.  Some people talk about "the jQuery object". Whether this refers to the object returned or the function itself depends on the context.

This "ready" function provides a really nice way of telling you exactly when the DOM has been loaded.  It removes the issue of the GAP after the page has been rendered but before the javascript code has been loaded. Most developers use this as a place where they register their event handlers.

*/
jQuery(document).ready(function(){
  // start up code goes here
  alert("this works!");
})

/*
creating html on the fly
*/
jQuery('<div id="badge"><img src="badge.gif" alt="Badge earned for achievement"</div>');

// using jQuery's namespace so they don't pollute the global namespace!!
$myCustomMethod = function() {alert('hi');};

// If you see a period after jQuery (or the dollar sign) you can reference the jQuery object itself.
$.listBox = {
  show: function() {},
  hide: function() {},
  position: function () {},
  initiate: function () {}
}

/* jQuery KNOWS that since you passed in a function, you want the $ to be a shortcut for the 'ready' method */
$(function() {
  // start up code goes here
  alert("this works!");

  $("#title").text("Yay, I can now get at the H1 immediately!");

  // THIS IS CRUCIAL: modifying html
  // $("#first").html("<h2>Great quotes</h2>");

  // append and prepend work INSIDE the given selection
  $("#first").prepend("<h2>Great quotes</h2>");
  $("#first").append("<h3>... for your to ponder ... </h3>");

  // before, after, insertBefore, insertAfter work OUTSIDE
  // the given selection.

  // changing the attribute
  $("#myAnchor").attr("href", "http://channel9.msdn.com");

  // applying CSS dynamically
  $("#title").addClass("standout");

});
