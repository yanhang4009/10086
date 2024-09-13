// var data = []
// var token = ""
// var questions
// var answers
//
// jQuery(document).ready(function () {
//     $(document).on('click', '#btn_file', function (e) {
//         $.ajax({
//             url: '/process',
//             type: "post",
//             contentType: "application/json",
//             dataType: "json",
//             data: JSON.stringify({
//                 "input_file": $('#file_name').val()
//             }),
//             beforeSend: function () {
//                 $('.overlay').show()
//             },
//             complete: function () {
//                 $('.overlay').hide()
//             }
//         }).done(function (jsondata, textStatus, jqXHR) {
//             cls = jsondata['class']
//             origin = jsondata['origin']
//             modify = jsondata['modify']
//
//             $('#output-text').val(cls)
//             $('#origin-items').val(origin)
//             $('#modify-items').val(modify)
//         }).fail(function (jsondata, textStatus, jqXHR) {
//             console.log(jsondata)
//         });
//     })
// })