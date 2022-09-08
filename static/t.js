function submit(){
    var title = $("#title").val();
    var content = $("#content").val();
    if(title == "" || content == "")
        alert("請填寫完整");
    else{
        $.ajax({
        url: "/upload",
        type: "POST",
        data:{"title":title, "content":content},
        success:function(data){
            $("#title").val("");
            $("#content").val("");
            $("#list").empty();
            $.each(JSON.parse(data), function(index, item){
		var type = "p";
		var typee = "p";
		if(item.content.indexOf("http://") >= 0 || item.content.indexOf("https://") >= 0){
			type = `a href="${item.content}" target="_blank"`;
		}
                $("#list").append(`<div class="block">
                <div>
                    <p class="chat_title">${item.title}</p>
                </div>
                <div class="chat_content">
			<${type}>${item.content}</${typee}>
                </div>
                <div style="text-align:right">
                    <button onclick="delete_chat(${item.id})">刪除</button>
                </div>
                </div>`);
            })
            $.growl.notice({"title" : "Success", "message" : "資料已送出"});
        },
        error:function(err){
            alert(err);
        }
        });
    }
}
window.onload=function(){
    $.ajax({
        url: "static/chat.txt",
        type: "GET",
        dataType:"json",
        success:function(data){
            chat_list(data);
        },
        error:function(err){
            alert(err);
        }
    });
}

function delete_chat(id){
    var answer = prompt('請輸入密碼')
    if(answer != null){
        $.ajax({
            url: "/delete",
            type: "POST",
            data:{"id": id, "answer": answer},
            success:function(data){
                $("#list").empty();
                $.ajax({
                    url: "static/chat.txt",
                    type: "GET",
                    dataType:"json",
                    success:function(data){
                        chat_list(data);
                    },
                    error:function(err){
                        alert(err);
                    }
                });
            },
            error:function(err){
                alert(err);
            }
        });
    }   
}

function chat_list(data){
    $.each((data), function(index, item){
        var type = "p";
        var typee = "p";
        if(item.content.indexOf("http://") >= 0 || item.content.indexOf("https://") >= 0){
            type = `a href="${item.content}" target="_blank"`;
            typee = "a";
        }
                    $("#list").append(`<div class="block">
                    <div>
                        <p class="chat_title">${item.title}</p>
                    </div>
                    <div class="chat_content">
                        <${type}>${item.content}</${typee}>
                    </div>
                    <div style="text-align:right">
                        <button onclick="delete_chat(${item.id})">刪除</button>
                    </div>
                    </div>`);
                })
}