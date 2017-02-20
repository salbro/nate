jQuery(document).ready(function() {
    $('.calculate').on('click', handleClick)
  });

    function handleClick()
    {
      var question_id = parseInt(this.id.split("_")[1]);
      var vote_direction = this.id.split("_")[2].split("vote")[0];
      var thisQuestionCell = this.closest('.inner_category_table');
      var row = parseInt(thisQuestionCell.id.split("_")[1]);
      var question_category = thisQuestionCell.id.split("_")[0];

      var votesAbove = 0;
      $("#"+question_category+"_"+(row-1).toString()).find('span').each(function(){
        votesAbove += Math.abs(parseInt($(this).text()));
      });

      var votesBelow = 0;
      $("#"+question_category+"_"+(row+1).toString()).find('span').each(function(){
        votesBelow += Math.abs(parseInt($(this).text()));
      });

      if (row === 0) {votesAbove = '';}
      if (row === TFY.tableHeight) {votesBelow = '';}

      $.getJSON($SCRIPT_ROOT + '/_vote',
        {
          question_id: question_id,
          vote_direction: vote_direction,
          votes_above: votesAbove,
          votes_below: votesBelow
        },
          /* the jsonified result */
          function(data) {
            /* newly_sorted_qs: questions passed back from server if a change
             in order is necessary */
            if(data['newly_sorted_qs']){

              for (var i = 0; i < data['newly_sorted_qs'][question_category].length; i++){
                var question_info = data['newly_sorted_qs'][question_category][i];
                if (question_info){
                  var q_id = question_info["q_id"];
                  var q_text = question_info["q_text"];
                  var upvotes = question_info["n_upvotes"];
                  var downvotes = question_info["n_downvotes"];
                  var tableHTML = TFY.createTable(q_id, q_text, upvotes, downvotes);
                }

                // else{ // no question to display
                //   var tableHTML = "<tbody><tr><td class='question'> Suggest a question! </td></tr></tbody>";
                // }
                // rewrite current table's html
                $("#"+question_category+"_"+i.toString()).html(tableHTML);
              } //end table-building loop
            }

            else if (data['newly_sorted_qs'] == null){
              // if no change in order, just change the button that was clicked
              var replacementHTML = TFY.createTable(data["question_id"], data["question_text"], data["upvotes"], data["downvotes"]);
              $(thisQuestionCell).html(replacementHTML);
            }
            // rebind all buttons after they've been remade in for loop
            $('.calculate').off('click');
            $('.calculate').on('click', handleClick);
        });
        return false;
    }
