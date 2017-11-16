$(function() {
  var user_id = $('#user_id').val(),
    object_type = $('#object_type').val(),
    group_type = $('#group_type').val(),
    order_by = $('#order_by').val(),
    tag = $('#tag').val();
  setTimeout(function() {
    $('.waiting').text('第一次生成需要一些时间，请耐心等待。');
  }, 10000);
  Loop_ajax();

  function Loop_ajax() {
    $.ajax({
      type: 'post',
      url: '/spider',
      data: {
        user_id: user_id,
        object_type: object_type,
        group_type: group_type,
        order_by: order_by,
        tag: tag
      },
      dataType: 'json',
      success: function(data) {
        if (data == '404') {
          $('.page').addClass('dn');
          $('.spinner').addClass('dn');
          $('.waiting').addClass('dn');
          $('.noMatch').removeClass('dn');
        } else {
          if (data == 'wait') {
            $('.page').addClass('dn');
            $('.noMatch').addClass('dn');
            $('.spinner').removeClass('dn');
            $('.waiting').removeClass('dn');
            setTimeout(function() {
              Loop_ajax();
            }, 1000);
          } else {
            $('.noMatch').addClass('dn');
            $('.spinner').addClass('dn');
            $('.waiting').addClass('dn');
            var resultStr = '<ul>',
              starStr = ''
            for (var i = 1; i < data.length; i++) {
              var rating = parseInt(parseFloat(data[i].rating) + 0.5),
                coverStr = 'page-list-cover'
              if (object_type == 2) {
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
              resultStr += ('<li><a href="' + data[i].link + '">' + ReferrerKiller.imageHtml(data[i].image, {
                  'class': coverStr
                }) +
                '</a><div class="page-list-info"><h3>' + data[i].title +
                '</h3><p class="page-list-rank"><span class="page-list-stars">' + starStr + '</span><span>' + data[i].rating + '</span></p></div></li>');
            }
            resultStr += '</ul>';
            $('.page').html(resultStr);
            setTimeout(function() {
              $('.page').removeClass('dn');
            }, 500);
          }
        }
      }
    });
  }
});
