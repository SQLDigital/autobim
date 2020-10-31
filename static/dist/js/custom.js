$(document).ready(function () {
    //Select2
    $('.searchable').select2();

    // clicked row
    $(".clicked-row").click(function () {
        var pk = $(this).data("href")
        window.location = pk
      });

    /* $('#addCompany').on('submit', function (event) {
        event.preventDefault()
        $.ajax({
          type: "POST",
          url: "/tidp/company/create/",
          cache: false,
          data: $('form#addCompany').serialize(),
          success: function (response) {
            location.reload()
          },
          error: function (err) {
            var message = '<div class="alert alert-danger text-center">'
            $.each(err.responseJSON,function(key,value){
                message += '<p>'+value+'</p>'
            })
            message += '</div>'
            $('.messageCenter').html(message)
          }

        })
    }) */

    //when discipline is changed, get discipline category
    //$('#id_discipline_category option').remove()
    $('select#id_discipline').on('change', function (event) {
        url = "/tidp/get-disciplinecategory?pk="+this.value
        $.ajax({
          type: "GET",
          url: url,
          dataType: "json",
          success: function (response) {
            $('#id_discipline_category option').remove()
            $.each(response, function(key, val){
                $('#id_discipline_category').append($('<option>', {"value": val.key, "text": val.value}))
            })
          },
          error: function (err) {
            alert('Oops! Something unpleasant just happened. Kindly try again.')
          }

        })
    })

    $('select#id_task-discipline').on('change', function (event) {
      url = "/tidp/get-disciplinecategory?pk="+this.value
      $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        success: function (response) {
          $('#id_task-discipline_category option').remove()
          $.each(response, function(key, val){
              $('#id_task-discipline_category').append($('<option>', {"value": val.key, "text": val.value}))
          })
        },
        error: function (err) {
          alert('Oops! Something unpleasant just happened. Kindly try again.')
        }

      })
  })

  $('#id_company').on('change', function (event) {
    $.ajax({
      type: "GET",
      url: "/tidp/get-company/?pk="+this.value,
      success: function (response) {
        $('#id_contact_person').val(response.contact_person)
        $('#id_contact_email').val(response.contact_email)
      },
      error: function (err) {
      }
    })
  })

    /* $('#new-project').on('click', function(event){
        $( "#get-project-form" ).load( "/tidp/get-project-form/", function() {
            $.getScript( "/static/dist/js/custom.js" )
        });
    }) */

});

