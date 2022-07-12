window.onload = function(){
    $.ajax({
        url : "file",
        type : "GET",
        dataType : "json",
        success : function(data){
            $.each(data.file_name, function(index, item){
		//alert(typeof(item.name));
                $("#list").append(`<div style="padding:10px"><a href="/download_file?filename=${item.name}"><button style="font-size:30px"><b>${item.name}</b></button></a></div>`);
            })
        }
    });
}
