$(function() {
  function getCookie(name) {
    var r = document.cookie.match('\\b' + name + '=([^;]*)\\b')
    return r ? r[1] : undefined
  }
  var user_id = $('#user_id').val(),
    object_type = $('#object_type').val(),
    group_type = $('#group_type').val(),
    order_by = $('#order_by').val(),
    tag = $('#tag').val(),
    _xsrf = getCookie('_xsrf');
  console.log(_xsrf);
  setTimeout(function() {
    $('.waiting').text('第一次生成需要一些时间，请耐心等待。');
  }, 10000);
  Loop_ajax();

  function Loop_ajax() {
    $.ajax({
      type: 'post',
      url: '/spider',
      data: {
        _xsrf: _xsrf,
        user_id: user_id,
        object_type: object_type,
        group_type: group_type,
        order_by: order_by,
        tag: tag
      },
      dataType: 'json',
      success: function(data) {
        if (data == '404') {
          $('.page').hide();
          $('.spinner').hide();
          $('.waiting').hide();
          $('.noMatch').show();
        } else {
          if (data == 'wait') {
            $('.page').hide();
            $('.noMatch').hide();
            $('.spinner').show();
            $('.waiting').show();
            setTimeout(function() {
              Loop_ajax();
            }, 1000);
          } else {
            $('.noMatch').hide();
            $('.spinner').hide();
            $('.waiting').hide();
            $('.page').show();
            var resultStr = '<ul>',
              starStr = ''
            for (var i = 1; i < data.length; i++) {
              var rating = parseInt(parseFloat(data[i].rating) + 0.5),
                coverStr = 'page-list-cover'
              if (object_type === 2) {
                coverStr = 'page-list-cover music-cover'
              }
              if (rating >= 9) {
                starStr = '<span class="page-list-star page-list-star-full"></span><span class="page-list-star page-list-star-full"></span><span class="page-list-star page-list-star-full"></span><span class="page-list-star page-list-star-full"></span><span class="page-list-star page-list-star-full"></span>'
              } else if (rating >= 7) {
                starStr = '<span class="page-list-star page-list-star-full"></span><span class="page-list-star page-list-star-full"></span><span class="page-list-star page-list-star-full"></span><span class="page-list-star page-list-star-full"></span><span class="page-list-star page-list-star-gray"></span>'
              } else if (rating >= 5) {
                starStr = '<span class="page-list-star page-list-star-full"></span><span class="page-list-star page-list-star-full"></span><span class="page-list-star page-list-star-full"></span><span class="page-list-star page-list-star-gray"></span><span class="page-list-star page-list-star-gray"></span>'
              } else if (rating >= 3) {
                starStr = '<span class="page-list-star page-list-star-full"></span><span class="page-list-star page-list-star-full"></span><span class="page-list-star page-list-star-gray"></span><span class="page-list-star page-list-star-gray"></span><span class="page-list-star page-list-star-gray"></span>'
              } else {
                starStr = '<span class="page-list-star page-list-star-gray"></span><span class="page-list-star page-list-star-gray"></span><span class="page-list-star page-list-star-gray"></span><span class="page-list-star page-list-star-gray"></span><span class="page-list-star page-list-star-gray"></span>'
              }
              resultStr += ('<li><a href="' + data[i].link + '"><div class="' + coverStr + '"><img src="' + data[i].image +
                '" class="display:block"></div></a><div class="page-list-info"><h3>' + data[i].title +
                '</h3><p class="page-list-rank"><span class="page-list-stars">' + starStr + '</span><span>' + data[i].rating + '</span></p></div></li>');
            }
            resultStr += '</ul>';
            $('.page').html(resultStr);
          }
        }
      }
    });
  }
});
