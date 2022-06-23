function display_sales_list(sales){
    $("#salespeople").empty()
    $("#clients").empty()
    $("#reamnumber").empty()
    $("#deletebuttons").empty()
    $.each(sales, function(index, jsonObject){
        let salesp = $("<div>")
        salesp.addClass("listitem");
        salesp.text(jsonObject['salesperson'])
        let clientname = $("<div>")
        clientname.text(jsonObject['client'])
        clientname.addClass("listitem");
        let reams = $("<div>")
        reams.text(jsonObject['reams'])
        reams.addClass("listitem");
        let button = '<input type="button" id='+'"'+jsonObject['id']+'"'+' class="btn btn-warning deletebutton smallmargin" value="X"/>'
        $("#clients").append(clientname)
        $("#reamnumber").append(reams)
        $("#salespeople").append(salesp)
        $("#clients").append(clientname)
        $("#reamnumber").append(reams)
        $("#deletebuttons").append(button)
        $("#deletebuttons").append("<br>")

    });
}