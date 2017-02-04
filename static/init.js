
// GLOBAL TFY
var TFY =
{
  createTable: function (q_id, q_text, upvotes, downvotes){
    var tableHTML = "";
    tableHTML +=
    "<tbody><tr> \
      <td class='question'>" + q_text + "</td> \
      </tr> \
      <tr>\
        <td class='vote_cell'>\
          <table class='vote_cell_table'><tbody><tr> \
            <td class='vote_cell_thumbs_vote'>\
              <button id='" + q_id + "_upvote' href='#'' class='fa fa-thumbs-o-up fa-2x calculate'></button> \
              <span id='" + q_id + "_upvotes' style='color:blue;'>" + upvotes + "</span> \
            </td>\
            <td class='voting_meter_td'>";
    var fade_factor = 15;
    if (upvotes > downvotes){
      var green_perc = 100*upvotes / (upvotes + downvotes);
      var lightgreen_perc = Math.round(green_perc + fade_factor).toString();
      green_perc = Math.round(green_perc).toString();
      var style_tag = "background-image: linear-gradient(90deg, green " + green_perc.slice(0,2) +"%, lightgreen " + lightgreen_perc.slice(0,2) +"%);";
    }
    else if (downvotes > upvotes){
      var red_perc = 100*downvotes / (upvotes + downvotes);
      var pink_perc = Math.round(red_perc - fade_factor).toString();
      red_perc = Math.round(red_perc).toString();
      var style_tag = "background-image: linear-gradient(90deg, pink " + pink_perc.slice(0,2) +"%, red " + red_perc.slice(0,2) +"%);";
    }
    else{
      var style_tag = "background-image: linear-gradient(90deg, green 50%, red 50%);";
    }
    tableHTML += "\
              <meter id='" + q_id + "_meter'>\
                <style>\
                  #"+id+"_meter { \
                    -webkit-appearance: none; \
                    style_tag \
                  }\
                </style>\
              </meter> \
            </td>";

    tableHTML += "\
      <td class='vote_cell_thumbs_vote'> \
        <button id='"+q_id+"_downvote' href='#' class='fa fa-thumbs-o-down fa-2x calculate'> </button> \
        <span id='"+q_id+"_downvotes' style='color:blue;'>" + downvotes + "</span> \
      </td> \
      </tr></tbody></table>"; // end of class vote_cell_table

    tableHTML += "</td></tr></tbody></table>";

    return tableHTML;
  }
};
