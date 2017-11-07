$(function() {
  var user_id = -1,
    object_type = -1,
    group_type = -1,
    order_by = -1,
    tag = 0,
    submit_down = -1;
  $('#submit_button').attr("disabled", true);
  $('.one_line').on('change', function() {
    user_id = $('#user_id').val();
    tag = $('#tag').val();
    if (tag == '') {
      tag = 0;
    }
    if (user_id != -1 && object_type != -1 && group_type != -1 && order_by != -1) {
      $('#submit_button').attr("disabled", false);
    } else {
      $('#submit_button').attr("disabled", true);
    }
  });
  $('.regular-radio').on('change', function() {
    if ($(this).attr("name") == 'radio-1-set') {
      object_type = $(this).attr("id").split('-')[2];
    } else if ($(this).attr("name") == 'radio-2-set') {
      group_type = $(this).attr("id").split('-')[2];
    } else if ($(this).attr("name") == 'radio-3-set') {
      order_by = $(this).attr("id").split('-')[2];
    }
    if (user_id != -1 && object_type != -1 && group_type != -1 && order_by != -1) {
      $('#submit_button').attr("disabled", false);
    } else {
      $('#submit_button').attr("disabled", true);
    }
  });
  $('#submit_button').on('click', function() {
    window.open('/iframe?user_id=' + user_id + '&object_type=' + object_type + '&group_type=' + group_type + '&order_by=' + order_by + '&tag=' + tag);
    $('.many_lines').text('<!-- [Top15]在要展示的位置插入如下代码： -->\n\
<script type="text/javascript">\n\
  function initIframe(){\n\
    var iframe = document.getElementById("top15_iframe");\n\
    try {\n\
      if (iframe.offsetWidth < 768) {\n\
        iframe.height = (iframe.offsetWidth * 0.3 * 1.47 + 65) * 5;\n\
      }\n\
      else {\n\
        iframe.height = (iframe.offsetWidth * 0.16 * 1.47 + 65) * 3;\n\
      }\n\
    }\n\
    catch (ex){}\n\
  }\n\
  reinitIframe();\n\
</script>\n\
<iframe onload="initIframe();" id="top15_iframe" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" width="100%" src="https://top15.jackeriss.com/iframe?user_id=' + user_id + '&object_type=' + object_type + '&group_type=' + group_type + '&order_by=' + order_by + '&tag=' + tag + '"></iframe>');
  });
});
