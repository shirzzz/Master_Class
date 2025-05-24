function create_search_result(id, name){
    let li_element = document.createElement("li");
    li_element.classList.add("user-item");
    let name_span = document.createElement("span");
    name_span.innerText = name;
    name_span.classList.add("user-name");
    li_element.appendChild(name_span);
    let add_button = document.createElement("button");
    add_button.innerText = "+";
    add_button.classList.add("user-action-button");
    add_button.classList.add("add");
    add_button.onclick = () => add_friend_listener(li_element, id, name);
    li_element.appendChild(add_button);
    return li_element;
}

function create_friend(id, name){
    let li_element = document.createElement("li");
    li_element.classList.add("user-item");
    let name_span = document.createElement("span");
    name_span.innerText = name;
    name_span.classList.add("user-name");
    li_element.appendChild(name_span);
    let add_button = document.createElement("button");
    add_button.innerText = "-";
    add_button.classList.add("user-action-button");
    add_button.classList.add("remove");
    li_element.appendChild(add_button);
    return li_element;
}


async function search_students(query_string, callback){
    let params = new URLSearchParams({
        query_string: query_string
    });
    let response = await fetch(`/api/search_students_by_name?${params}`);
    let data = await response.json();
    callback(data.results);
}


function update_search_results(results){
    let ul = document.querySelector("#search-results");
    ul.replaceChildren([]);
    results.forEach((item) => {ul.appendChild(create_search_result(item.id, item.name));});
}


function search_listener(e) {
    search_students(e.target.value, update_search_results);
}

async function add_friend_listener(li_element, id, name){
    let params = new FormData();
    params.append("friend_id", id);
    let response = await fetch(`/api/add_friend?`, {
        method: "POST",
        body: params
    });
    let data = await response.json();
    li_element.remove();
    let ul = document.querySelector("#user-list");
    console.log(ul)
    ul.appendChild(create_friend(id, name))

}

setTimeout(() => {
    document.querySelector("#student-search-box").addEventListener("input", search_listener)
}, 1000);