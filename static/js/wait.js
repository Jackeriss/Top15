$(function() {
  var user_id = $('#user_id').val(),
    object_type = $('#object_type').val(),
    group_type = $('#group_type').val(),
    order_by = $('#order_by').val();
    tag = $('#tag').val();
  setTimeout(function () {
    $('.waiting').text('第一次生成需要一些时间，请耐心等待。');
  }, 10000);
  Loop_ajax();
  function Loop_ajax(){
    $.getJSON($SCRIPT_ROOT + '/check', {
        user_id: user_id,
        object_type: object_type,
        group_type: group_type,
        order_by: order_by,
        tag: tag
      }, function(data){
      if(data.result == '1'){
        window.location.reload();
      }
      else{
        setTimeout(function () {
          Loop_ajax();
        }, 1000);
      }
    });
  }
});
