$(function() {
  var user_id = -1,
    object_type = -1,
    group_type = -1,
    order_by = -1;
    submit_down = -1
  $('#submit_button').attr("disabled",true);
  $('.one_line').on('change', function() {
    user_id = $(this).val();
    if (user_id != -1 && object_type != -1 && group_type != -1 && order_by != -1) {
      $('#submit_button').attr("disabled", false);
		}
		else {
			$('#submit_button').attr("disabled", true);
		}
  });
  $('.regular-radio').on('change', function() {
    if ($(this).attr("name") == 'radio-1-set') {
      object_type = $(this).attr("id").split('-')[2];
    }
    else if ($(this).attr("name") == 'radio-2-set'){
      group_type = $(this).attr("id").split('-')[2];
    }
    else if ($(this).attr("name") == 'radio-3-set'){
      order_by = $(this).attr("id").split('-')[2];
    }
    if (user_id != -1 && object_type != -1 && group_type != -1 && order_by != -1) {
      $('#submit_button').attr("disabled", false);
		}
		else {
			$('#submit_button').attr("disabled", true);
		}
  });
  $('.js_button').on('click', function() {
    if ($(this).attr("id") == 'submit_button') {
      submit_down = 0
      window.open('/iframe?user_id=' + user_id + '&object_type=' + object_type + '&group_type=' + group_type + '&order_by=' + order_by);
    }
    else{
      $('.j_button').removeClass("active");
      $(this).addClass("active");
    }
    if (submit_down == 0){
    $('.many_lines').text('<!-- Top15 JavaScript版 -->\n\
<!-- 在要展示的位置插入如下代码： -->\n\
<script type="text/javascript">\n\
  function reinitIframe(){\n\
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
  window.setInterval("reinitIframe()", 200);\n\
</script>\n\
<iframe id="top15_iframe" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" width="100%" src="http://top15.jackeriss.com/iframe?user_id=' + user_id + '&object_type=' + object_type + '&group_type=' + group_type + '&order_by=' + order_by + '"></iframe>');
    }
  });
  $('.jq_button').on('click', function() {
    $('.j_button').removeClass("active");
    $(this).addClass("active");
    if (submit_down == 0){
    $('.many_lines').text('<!-- Top15 JQuery版 -->\n\
<!-- 在要展示的位置插入如下代码： -->\n\
<script type="text/javascript">\n\
  $(function () {\n\
    var iframe = document.getElementById("top15_iframe");\n\
    function reinitIframe(){\n\
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
    iframe.onload = reinitIframe();\n\
    $(window).resize(function () {\n\
      reinitIframe();\n\
    });\n\
  });\n\
</script>\n\
<iframe id="top15_iframe" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" width="100%" src="http://top15.jackeriss.com/iframe?user_id=' + user_id + '&object_type=' + object_type + '&group_type=' + group_type + '&order_by=' + order_by + '"></iframe>');
    }
  });
});
