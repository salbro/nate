window.onclick = function(event) {
  if (!event.target.matches('.dropbtn') && !event.target.matches('.dropdown-content')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

// GLOBAL TFY
var TFY =
{
  submitQuestion: function(e){
    e.preventDefault();
    e.stopPropagation();
    // alert("inside submit");
    var question = $("#suggest-question-input").val();
    alert('thanks!');
    $.getJSON($SCRIPT_ROOT + '/suggest_question',
      {
        q_text: question
      },
        /* the jsonified result */
      function(data) {
      });
      $('#suggest-submit').off('click');
      $('#suggest-submit').on('click', submitQuestion);
      return false;
  },


  createTable: function (q_id, q_text, upvotes, downvotes){
    q_id = q_id.toString()
    var tableHTML = "";
    tableHTML +=
    "<tbody><tr> \
      <td class='question'>" + q_text + "</td> \
      </tr> \
      <tr>\
        <td class='vote_cell'>\
          <table class='vote_cell_table'><tbody><tr> \
            <td class='vote_cell_thumbs_vote'>\
              <button id='q_" + q_id + "_upvote' href='#'' class='fa fa-thumbs-o-up fa-2x calculate'></button> \
              <span id='q_" + q_id + "_upvotes'>" + upvotes + "</span> \
            </td>\
            <td class='voting_meter_td'>";
    var colors = (upvotes >= downvotes) ? ["green", "lightgreen"] : ["red", "pink"];
    var fade_factor = 10;
    perc_upvotes = parseFloat((100*(upvotes) / (upvotes + downvotes)).toPrecision(2));
    if (perc_upvotes === 100.0 || perc_upvotes === 0.0){
      var style_tag = "background-color: " + colors[0] + ";";
    }
    else{
      lightly_colored_perc = perc_upvotes + fade_factor;
      var style_tag = "background-image: linear-gradient(90deg, " + colors[0] + " " + perc_upvotes.toString() +"%, " + colors[1] + " " + lightly_colored_perc.toString() + "%);";
    }
    tableHTML += "\
              <meter id='q_" + q_id + "_meter'>\
                <style>\
                  #q_"+q_id+"_meter { \
                    -webkit-appearance: none;" +
                    style_tag + "\
                  }\
                </style>\
              </meter> \
            </td>";

    tableHTML += "\
      <td class='vote_cell_thumbs_vote'> \
        <button id='q_"+q_id+"_downvote' href='#' class='fa fa-thumbs-o-down fa-2x calculate'> </button> \
        <span id='q_"+q_id+"_downvotes'>" + downvotes + "</span> \
      </td> \
      </tr></tbody></table>"; // end of class vote_cell_table

    tableHTML += "</td></tr></tbody></table>";
    return tableHTML;
  },

  dropdown: function(){
    document.getElementById("drop-down-menu").classList.toggle("show");
  }

};

jQuery(document).ready(function() {
    $('#suggest-form').on('submit', TFY.submitQuestion)
  });
