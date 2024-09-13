function getDirLevel() {
    var jsonData;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/dir-level', true);
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                jsonData = JSON.parse(xhr.responseText);
                console.log(jsonData);  // 打印返回的JSON数据
                dir.value = jsonData;
            } else {
                console.log("Error: " + xhr.status + " - " + xhr.responseText);
            }
        }
    };

    xhr.onerror = function() {
        console.log("Request failed.");
    };

    xhr.send();
    return jsonData;
}