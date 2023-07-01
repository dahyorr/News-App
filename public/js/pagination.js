
//calling function with passing parameters and adding inside element which is ul tag
function createPagination(totalPages, page){
  let liTag = '';
  let active;
  let beforePage = page - 1;
  let afterPage = page + 1;
  if(page > 1){ //show the next button if the page value is greater than 1
    liTag += `<a><li class="btn prev" onclick="createPagination(totalPages, ${beforePage}); update_query_parameters('page', page-1)"><span><i class="fas fa-angle-left"></i> Prev</span></li></a>`;
  }

  if(page > 2){ //if page value is less than 2 then add 1 after the previous button
    liTag += `<a><li class="first numb" onclick="createPagination(totalPages, 1); update_query_parameters('page', 1)"><span>1</span></li></a>`;
    if(page > 3){ //if page value is greater than 3 then add this (...) after the first li or page
      liTag += `<li class="dots"><span>...</span></li>`;
    }
  }
  // how many pages or li show before the current li
  if (page === totalPages) {
    beforePage = beforePage - 2;
  } else if (page === totalPages - 1) {
    beforePage = beforePage - 1;
  }
  // how many pages or li show after the current li
  if (page === 1) {
    afterPage = afterPage + 2;
  } else if (page === 2) {
    afterPage  = afterPage + 1;
  }

  for (let paginationLength = beforePage; paginationLength <= afterPage; paginationLength++) {
    if (paginationLength > totalPages) { //if paginationLength is greater than totalPage length then continue
      continue;
    }
    if (paginationLength === 0) { //if paginationLength is 0 than add +1 in paginationLength value
      paginationLength = paginationLength + 1;
    }
    if(page === paginationLength){ //if page is equal to paginationLength than assign active string in the active variable
      active = "active";
    }else{ //else leave empty to the active variable
      active = "";
    }
    liTag += `<a onclick= ${active==='active'?"null":"update_query_parameters('page',"+paginationLength+")"}><li class="numb ${active}" onclick="createPagination(totalPages, ${paginationLength});"><span>${paginationLength}</span></li></a>`;
  }

  if(page < totalPages - 1){ //if page value is less than totalPage value by -1 then show the last li or page
    if(page < totalPages - 2){ //if page value is less than totalPage value by -2 then add this (...) before the last li or page
      liTag += `<li class="dots"><span>...</span></li>`;
    }
    liTag += `<a><li class="last numb" onclick="createPagination(totalPages, ${totalPages}); update_query_parameters('page', totalPages)"><span>${totalPages}</span></li></a>`;
  }

  if (page < totalPages) { //show the next button if the page value is less than totalPage(20)
    liTag += `<a><li class="btn next" onclick="createPagination(totalPages, ${page + 1}); update_query_parameters('page', ${page + 1})"><span>Next <i class="fas fa-angle-right"></i></span></li></a>`;
  }
  element.innerHTML = liTag; //add li tag inside ul tag
  return liTag; //return the li tag
}