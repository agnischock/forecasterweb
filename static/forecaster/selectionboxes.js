function removeOptions(selectbox)
{
    var i;
    for(i = selectbox.options.length - 1 ; i >= 0 ; i--)
    {
        selectbox.remove(i);
    }
}

$("#id_products_branch_item_level_1").change(function () {

    var url = $("#productForm").attr("load-branch-url");
    var productId = $(this).val();
    console.log(productId)
    $.ajax({
    url: url,
    data: {
        'product_id': productId
    },
    success: function (data) {
        $("#id_products_branch_item_level_2").html(data);
        $("#id_products_branch_item_level_2").show();
        var product_selection_level_3 =  document.getElementById("id_products_branch_item_level_3");
        removeOptions(product_selection_level_3);
        $("#id_products_branch_item_level_3").hide();
    }
    });
});
$("#id_products_branch_item_level_2").change(function () {
    var url = $("#productForm").attr("load-branch-url");
    var productId = $(this).val();
    console.log(productId)
    $.ajax({
    url: url,
    data: {
        'product_id': productId
    },
    success: function (data) {
        $("#id_products_branch_item_level_3").html(data);
        $("#id_products_branch_item_level_3").show();
    }
    });
});


$("#id_channels_branch_item_level_1").change(function () {
    var url = $("#channelForm").attr("load-branch-url");
    var channelId = $(this).val();
    console.log(channelId)
    $.ajax({
    url: url,
    data: {
        'channel_id': channelId
    },
    success: function (data) {
        $("#id_channels_branch_item_level_2").html(data);
        var channel_selection_level_3 =  document.getElementById("id_channels_branch_item_level_3");
        removeOptions(channel_selection_level_3);
        var channel_selection_level_4 =  document.getElementById("id_channels_branch_item_level_4");
        removeOptions(channel_selection_level_4);
    }
    });
});
$("#id_channels_branch_item_level_2").change(function () {
    var url = $("#channelForm").attr("load-branch-url");
    var channelId = $(this).val();
    console.log(channelId)
    $.ajax({
    url: url,
    data: {
        'channel_id': channelId
    },
    success: function (data) {
        $("#id_channels_branch_item_level_3").html(data);
        var channel_selection_level_4 =  document.getElementById("id_channels_branch_item_level_4");
        removeOptions(channel_selection_level_4);
    }
    });
});
$("#id_channels_branch_item_level_3").change(function () {
    var url = $("#channelForm").attr("load-branch-url");
    var channelId = $(this).val();
    console.log(channelId)
    $.ajax({
    url: url,
    data: {
        'channel_id': channelId
    },
    success: function (data) {
        $("#id_channels_branch_item_level_4").html(data);
    }
    });
});