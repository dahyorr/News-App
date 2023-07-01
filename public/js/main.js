function getQueryVariable(variable) {
    const query = window.location.search.substring(1);
    const vars = query.split('&');
    for (let i = 0; i < vars.length; i++) {
        const pair = vars[i].split('=');
        if (decodeURIComponent(pair[0]) === variable) {
            return decodeURIComponent(pair[1]);
        }
    }
    return null
}

function update_query_parameters(key, val) {
    return window.location.href =  window.location.href
       .replace(RegExp("([?&]" + key + "(?=[=&#]|$)[^#&]*|(?=#|$))"), "&" + key + "=" + encodeURIComponent(val))
       .replace(/^([^?&]+)&/, "$1?");
}

function removeQueryParam(key){
    const url = window.location.href
    let rtn = url.split("?")[0]
    let param, params_arr
    const queryString = (url.indexOf("?") !== -1) ? url.split("?")[1] : "";
    if (queryString !== "") {
        params_arr = queryString.split("&");
        for (let i = params_arr.length - 1; i >= 0; i -= 1) {
            param = params_arr[i].split("=")[0];
            if (param === key) {
                params_arr.splice(i, 1);
            }
        }
        if (params_arr.length) rtn = rtn + "?" + params_arr.join("&");
    }
    return window.location.href = rtn;
}

const job_tag = document.querySelector('#job')
const story_tag = document.querySelector('#story')
const remove_filter = document.querySelector('#remove-filter')
const filterQuery = getQueryVariable('filter')
if(filterQuery === 'job'){
    job_tag.className+='active'
}
else if(filterQuery === 'story'){
    story_tag.className+='active'
}
else{
    remove_filter.className+= 'hide'
}