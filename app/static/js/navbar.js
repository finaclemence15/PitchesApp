$(window).scroll(function() {
    if($(this).scrollTop() > 50)  /*height in pixels when the navbar becomes non opaque*/
    {
        $('.opaque-navbar').addClass('opaque');
        $('.brand').addClass('opaque');
    } else {
        $('.opaque-navbar').removeClass('opaque');
        $('.brand').removeClass('opaque');
    }
  });