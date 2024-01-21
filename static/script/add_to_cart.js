$('#add-to-cart-btn').click(function (e){
    e.preventDefault();
    let food_id = $(this).closest('.food-data').find('.food_id').val();
    let token = $('input[name=csrfmiddlewaretoken]').val();
    let quantity = $('#inputQuantity').val()
    $.ajax({
        method:"POST",
        url:"/order/add-to-cart/",
        data:{
            'food_id' : food_id,
            'quantity': quantity,
            csrfmiddlewaretoken: token
        },
        dataType: 'dataType',
        success: function(response){
            console.log(response);
            location.reload();
        }
    })
})