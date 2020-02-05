
/*=============================================================
    Authour URI: www.binarytheme.com
    License: Commons Attribution 3.0

    http://creativecommons.org/licenses/by/3.0/

    100% To use For Personal And Commercial Use.
    IN EXCHANGE JUST GIVE US CREDITS AND TELL YOUR FRIENDS ABOUT US

    ========================================================  */


(function ($) {
    "use strict";
    var mainApp = {

        metisMenu: function () {

            /*====================================
            METIS MENU
            ======================================*/

            $('#main-menu').metisMenu();

        },


        loadMenu: function () {

            /*====================================
            LOAD APPROPRIATE MENU BAR
         ======================================*/

            $(window).bind("load resize", function () {
                if ($(this).width() < 768) {
                    $('div.sidebar-collapse').addClass('collapse')
                } else {
                    $('div.sidebar-collapse').removeClass('collapse')
                }
            });
        },
        slide_show: function () {

            /*====================================
           SLIDESHOW SCRIPTS
        ======================================*/

            $('#carousel-example').carousel({
                interval: 3000 // THIS TIME IS IN MILLI SECONDS
            })
        },
        reviews_fun: function () {
            /*====================================
         REWIEW SLIDE SCRIPTS
      ======================================*/
            $('#reviews').carousel({
                interval: 2000 //TIME IN MILLI SECONDS
            })
        },
        wizard_fun: function () {
            /*====================================
            //horizontal wizrd code section
             ======================================*/
            $(function () {
                $("#wizard").steps({
                    headerTag: "h2",
                    bodyTag: "section",
                    transitionEffect: "slideLeft"
                });
            });
            /*====================================
            //vertical wizrd  code section
            ======================================*/
            $(function () {
                $("#wizardV").steps({
                    headerTag: "h2",
                    bodyTag: "section",
                    transitionEffect: "slideLeft",
                    stepsOrientation: "vertical"
                });
            });
        },
        search_run: function () {
          $.fn.datepicker.defaults.language = 'zh-CN';
          $("#form-search").submit(function(e){
            e.preventDefault();
            // var frm = $("#form-search");
            $("#btn-search").button('loading');
            $.ajax({
              url: $(this).attr("action"),
              type: $(this).attr("method"),
              data: $(this).serialize(),
              success: function(result){
                window.location.href = result;
                $("#btn-search").button('reset');
              },
              error: function(){
                $("#btn-search").button('reset');
                alert("查询失败!");
              }
            });
          });
        },
        delrec_run: function () {
          $("#form-delrec").submit(function(e){
            e.preventDefault();
            $("#btn-delrec").button('loading');
            var formData = new FormData(this);
            $.ajax({
              url: $(this).attr("action"),
              type: $(this).attr("method"),
              dataType: "json",
              //data: $(this).serialize(),
              data: formData,
              cache: false,
              processData: false,
              contentType: false,
              success: function(result){
                $("#btn-delrec").button('reset');
                if(typeof result.err != 'undefined'){
                  alert(result.err);
                } else {
                  $("#panel-delrec-step1").hide();
                  $("#panel-delrec-step2").show();
                  $("#delrec-num").text(result.num);
                  $("#id").val(result.id);
                }
              },
              error: function(){
                $("#btn-delrec").button('reset');
                alert("提交失败!");
              }
            });
          });
          $("#btn-cancel").click(function(e){
            e.preventDefault();
            $("#panel-delrec-step2").hide();
            $("#panel-delrec-step1").show();
          });
          $("#form-confirm").submit(function(e){
            e.preventDefault();
            $("#btn-cancel").hide();
            $("#btn-confirm").button('loading');
            $.ajax({
              url: $(this).attr("action"),
              type: $(this).attr("method"),
              data: $(this).serialize(),
              success: function(result){
                alert(result);
                location.reload();
              },
              error: function(){
                alert("删除失败!");
                $("#btn-cancel").show();
                $("#btn-confirm").button('reset');
                $("#panel-delrec-step2").hide();
                $("#panel-delrec-step1").show();
              }
            });
          });
        },

    };
    $(document).ready(function () {
        mainApp.metisMenu();
        mainApp.loadMenu();
        mainApp.slide_show();
        mainApp.reviews_fun();
        mainApp.wizard_fun();
        mainApp.search_run();
        mainApp.delrec_run();
    });
}(jQuery));
