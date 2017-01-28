jQuery(document).ready(function() {
    $('.calculate').on('click', handleClick)
  });

    function handleClick()

    {
      var button_id = this.id.split("_")[0]
      var button_direction = this.id.split("_")[1]
      var button_topic = button_id.replace(/[0-9]/g, '');
      var row = parseInt(this.closest('table').id.split("_")[1]);
      // not sure this thing works
      // #################################################3
      var votesAbove = 0;
      $("#"+button_topic+"_"+(row-1).toString()).find('span').each(function(){
        votesAbove += Math.abs(parseInt($(this).text()));
      });

      var votesBelow = 0;
      $("#"+button_topic+"_"+(row+1).toString()).find('span').each(function(){
        votesBelow += Math.abs(parseInt($(this).text()));
      });

      if (row === 0){
        votesAbove = '';
      }
      if (row === TFY.tableHeight){
        votesBelow = '';
      }


      // #################################################3

      // var votesBelow = $("#"+button_topic+"_"+(row+1).toString()).find('span').text();
      // the website can get to here.
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


                  var tableHTML = "<tbody><tr><td class='question'>" + q_text + "</td></tr><tr> \
                    <td class='vote_cell'> \
                    <div><button id ='" + q_id + "_upvote' href='#' class='fa fa-thumbs-o-up calculate'></button> \
                    <span id='" + q_id + "_upvotes' style='color:blue;'>" + upvotes + "</span></div> \
                    <div> INSERT BAR </div> \
                    <div><button id='" + q_id + "_downvote' href='#' class='fa fa-thumbs-o-down calculate'></button> \
                    <span id='" + q_id + "_downvotes' style='color:blue;'>" + "-" + downvotes + "</span></div></tr></tbody>";
                }

                else{ // no question to display
                  var tableHTML = "<tbody><tr><td class='question'> Suggest a question! </td></tr></tbody>";
                }

                // rewrite that table's html
                $("#"+button_topic+"_"+i.toString()).html(tableHTML);

              } //end for loop over questions

              // rebind all buttons after they've been remade in for loop
              $('.calculate').off('click');
              $('.calculate').on('click', handleClick);
            }

            else{ // no change in order necessary. just update votecount
              var txt = data[button_direction+"s"];
              if (button_direction === "downvote"){
                txt = "-" + txt;
              }
              $("#"+data['id']+"_"+button_direction+"s").text(txt);
            }
        });
        return false;
    }
