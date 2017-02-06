jQuery(document).ready(function() {
    $('.calculate').on('click', handleClick)
  });

    function handleClick()
    {
      var button_id = this.id.split("_")[0];
      var button_direction = this.id.split("_")[1];
      var button_topic = button_id.replace(/[0-9]/g, '');
      var thisQuestionCell = this.closest('.inner_topic_table');
      var row = parseInt(thisQuestionCell.id.split("_")[1]);

      var votesAbove = 0;
      $("#"+button_topic+"_"+(row-1).toString()).find('span').each(function(){
        votesAbove += Math.abs(parseInt($(this).text()));
      });

      var votesBelow = 0;
      $("#"+button_topic+"_"+(row+1).toString()).find('span').each(function(){
        votesBelow += Math.abs(parseInt($(this).text()));
      });

      if (row === 0) {votesAbove = '';}
      if (row === TFY.tableHeight) {votesBelow = '';}

      $.getJSON($SCRIPT_ROOT + '/_vote',
        {
          button_id: button_id,
          button_direction: button_direction,
          button_class: this.className,
          votes_above: votesAbove,
          votes_below: votesBelow
        },
          function(data) {
            /* newly_sorted_qs: questions passed back from server if a change
             in order is necessary */
            if(data['newly_sorted_qs']){
              for (var i = 0; i < data['newly_sorted_qs'][button_topic].length; i++){
                var question_info = data['newly_sorted_qs'][button_topic][i];
                if(question_info){
                  var q_id = question_info[0];
                  var q_text = question_info[1]['question'];
                  var upvotes = question_info[1]["upvotes"];
                  var downvotes = question_info[1]["downvotes"];


                  var tableHTML = TFY.createTable(q_id, q_text, upvotes, downvotes);
                }

                else{ // no question to display
                  var tableHTML = "<tbody><tr><td class='question'> Suggest a question! </td></tr></tbody>";
                }

                // rewrite that table's html
                $("#"+button_topic+"_"+i.toString()).html(tableHTML);
              } //end for loop over questions
            }
            else if (data['newly_sorted_qs'] == null){
              // find the table that this button is in & change its HTML
              var replacementHTML = TFY.createTable(data["id"], data["question"], data["upvotes"], data["downvotes"]);
              $(thisQuestionCell).html(replacementHTML);
            }
            // rebind all buttons after they've been remade in for loop
            $('.calculate').off('click');
            $('.calculate').on('click', handleClick);
        });
        return false;
    }
