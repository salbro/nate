
// GLOBAL TFY
var TFY =
{
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
              <span id='q_" + q_id + "_upvotes' style='color:blue;'>" + upvotes + "</span> \
            </td>\
            <td class='voting_meter_td'>";
    var fade_factor = 10;
    perc_upvotes = parseFloat((100*(upvotes) / (upvotes + downvotes)).toPrecision(2));
    lightly_colored_perc = perc_upvotes + fade_factor;
    var colors = (upvotes >= downvotes) ? ["green", "lightgreen"] : ["red", "pink"];
    var style_tag = "background-image: linear-gradient(90deg, " + colors[0] + " " + perc_upvotes.toString() +"%, " + colors[1] + " " + lightly_colored_perc.toString() + "%);";
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
        <span id='q_"+q_id+"_downvotes' style='color:blue;'>" + downvotes + "</span> \
      </td> \
      </tr></tbody></table>"; // end of class vote_cell_table

    tableHTML += "</td></tr></tbody></table>";
    return tableHTML;
  }
};
