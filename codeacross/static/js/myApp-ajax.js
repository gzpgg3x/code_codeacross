$(document).ready(function() {


    $('#likes').click(function(){
            var catid;
            catid = $(this).attr("data-catid");
             $.get('/myApp/like_category/', {category_id: catid}, function(data){
                       $('#like_count').html(data);
                       $('#likes').hide();
                   });
        });

    $('#suggestion').keyup(function(){
		var query;
		query = $(this).val();
		$.get('/myApp/suggest_category/', {suggestion: query}, function(data){
                 $('#cats').html(data);
		});
	});


  //   $('#myApp-add').click(function(){
  //   var query;
  //   query = $(this).val();;
  //   $.get('/myApp/auto_add_page/', {result_list: query}, function(data){
  //                $('#result_list').html(data);
  //                $('#myApp-add').hide();
  //   });
  // });

  //   $('.myApp-add').click(function(){
  //   var catid = $(this).attr("data-catid");
  //   var url = $(this).attr("data-url");
  //   var title = $(this).attr("data-title");
  //   var me = $(this)
  //   $.get('/myApp/auto_add_page/', {category_id: catid, url: url, title: title}, function(data){
  //                $('#pages').html(data);
  //                me.hide();
  //   });
  // });

  $('.myApp-add').click(function(){
      var catid = $(this).attr("data-catid");
        var url = $(this).attr("data-url");
        var title = $(this).attr("data-title");
        var me = $(this)
      $.get('/myApp/auto_add_page/', {category_id: catid, url: url, title: title}, function(data){
                     $('#pages').html(data);
                     me.hide();
                 });
      });
});