jQuery(document).ready(function() {
    $('.calculate').bind('click', function()
    {
      button_id = this.id.split("_")[0]
      button_direction = this.id.split("_")[1]
      button_topic = button_id.replace(/[0-9]/g, '');
      // the website can get to here.
      $.getJSON($SCRIPT_ROOT + '/_vote',
        {
          button_id_direction: this.id
        },
          function(data) {
            if(data['newly_sorted_qs']){
              var question_display_num = 0;
              for (var i = 0; i < data['newly_sorted_qs'].length; i++){
                var question_info = data['newly_sorted_qs'][i];
                if(question_info){
                  var q_id = question_info[0];
                  var q_text = question_info[1][0];
                  var q_votecount = question_info[1][1];

                  var tableHTML = " \
                    <td>" + q_text + "</td> \
                    <td class='vote_cell'> \
                        <button id ='" + q_id + "_up' href='#' class='fa fa-chevron-up calculate'></button> \
                        <span id='" + q_id + "_votecount' style='color:blue;'>" + q_votecount + "</span> \
                        <button id='" + q_id + "_down' href='#' class='fa fa-chevron-down calculate'></button> \
                    </td> \
                    ";
                }

                else{ // no question to display
                  var tableHTML = "<td>Suggest a question!</td>";
                }

                var tableID = "#"+button_topic+"_"+question_display_num.toString();
                question_display_num += 1;

                var el = $(tableID);
                alert(tableHTML);
                $("#"+button_topic+"_"+question_display_num.toString()).text(tableHTML);
              }
            }
            else{
              $("#"+data['id']+"_votecount").text(data['votecount']);
            }
        });
        return false;
    });
  });
