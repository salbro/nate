jQuery(document).ready(function() {
    $('.calculate').on('click', handleClick)
  });

    function handleClick()

    {
      var button_id = this.id.split("_")[0]
      var button_direction = this.id.split("_")[1]
      var button_topic = button_id.replace(/[0-9]/g, '');
      var row = parseInt(this.closest('table').id.split("_")[1]);
      var votesAbove = $("#"+button_topic+"_"+(row-1).toString()).find('span').text();
      var votesBelow = $("#"+button_topic+"_"+(row+1).toString()).find('span').text();
      // the website can get to here.
      $.getJSON($SCRIPT_ROOT + '/_vote',
        {
          button_id_direction: this.id,
          button_class: this.className,
          votes_above: votesAbove,
          votes_below: votesBelow
        },
          function(data) {
            /* newly_sorted_qs: questions passed back from server if a change
             in order is necessary */
            if(data['newly_sorted_qs']){
              for (var i = 0; i < data['newly_sorted_qs'].length; i++){
                var question_info = data['newly_sorted_qs'][i];
                if(question_info){
                  var q_id = question_info[0];
                  var q_text = question_info[1][0];
                  var q_votecount = question_info[1][1];

                  if (i === 0){var top = " top";}
                  else{var top = "";}
                  var tableHTML = "<tbody><tr><td class='question'>" + q_text + "</td> \
                    <td class='vote_cell'> \
                        <button id ='" + q_id + "_up' href='#' class='fa fa-chevron-up calculate'></button> \
                        <span id='" + q_id + "_votecount' style='color:blue;'>" + q_votecount + "</span> \
                        <button id='" + q_id + "_down' href='#' class='fa fa-chevron-down calculate "+top+"'></button> \
                    </td></tr></tbody>";
                }

                else{ // no question to display
                  var tableHTML = "<td>Suggest a question!</td>";
                }

                // rewrite that table's html
                $("#"+button_topic+"_"+i.toString()).html(tableHTML);
              } //end for loop over questions

              // rebind all buttons after they've been remade in for loop
              $('.calculate').off('click');
              $('.calculate').on('click', handleClick);
            }

            else{ // no change in order necessary. just update votecount
              $("#"+data['id']+"_votecount").text(data['votecount']);
            }
        });
        return false;
    }
